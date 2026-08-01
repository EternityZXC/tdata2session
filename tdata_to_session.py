import asyncio
from pathlib import Path

from opentele.td import TDesktop
from opentele.api import UseCurrentSession

# Folder that CONTAINS one subfolder per account, each subfolder being a
# full tdata folder on its own, e.g.:
#   tdata_accounts/
#     acc1/  (tdata files directly inside)
#     acc2/
#     acc3/
TDATA_ROOT = Path(r".\tdata_accounts")

SESSIONS_DIR = Path("sessions")
DELAY_BETWEEN_ACCOUNTS = 5  # seconds of pacing between conversions


async def convert_one(tdata_path: Path) -> None:
    tdesk = TDesktop(str(tdata_path))

    if not tdesk.isLoaded():
        print(f"[{tdata_path.name}] Failed to load tdata - skipping")
        return

    # We don't know the account's username until after connecting, so
    # convert into a temp filename first and rename it once we know.
    temp_session = SESSIONS_DIR / f"_tmp_{tdata_path.name}"

    try:
        client = await tdesk.ToTelethon(session=str(temp_session), flag=UseCurrentSession)
    except Exception as e:
        print(f"[{tdata_path.name}] Conversion failed: {e}")
        return

    try:
        await client.connect()

        if not await client.is_user_authorized():
            print(f"[{tdata_path.name}] Not authorized (login may have expired) - skipping")
            return

        me = await client.get_me()
        username = me.username or f"id{me.id}"
        final_path = SESSIONS_DIR / f"account_(@{username}).session"

        # disconnect before moving the file so nothing has it open/locked
        await client.disconnect()

        temp_file = temp_session.with_suffix(".session")
        temp_file.replace(final_path)

        print(f"[{tdata_path.name}] Success: {me.first_name} (@{username}) -> {final_path.name}")

    except Exception as e:
        print(f"[{tdata_path.name}] Failed after connecting: {e}")
        if client.is_connected():
            await client.disconnect()
        temp_session.with_suffix(".session").unlink(missing_ok=True)


async def main():
    if not TDATA_ROOT.is_dir():
        print(f"'{TDATA_ROOT}' is not a folder. Point TDATA_ROOT at the "
              f"directory that CONTAINS your individual tdata folders.")
        return

    SESSIONS_DIR.mkdir(exist_ok=True)

    tdata_folders = sorted(p for p in TDATA_ROOT.iterdir() if p.is_dir())

    if not tdata_folders:
        print(f"No subfolders found in '{TDATA_ROOT}'")
        return

    print(f"Found {len(tdata_folders)} tdata folder(s)\n")

    for i, folder in enumerate(tdata_folders):
        await convert_one(folder)
        if i < len(tdata_folders) - 1:
            await asyncio.sleep(DELAY_BETWEEN_ACCOUNTS)


if __name__ == "__main__":
    asyncio.run(main())
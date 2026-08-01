import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

from telethon import TelegramClient
from telethon.errors import (
    UserPrivacyRestrictedError,
    PeerFloodError,
    FloodWaitError,
    UsernameNotOccupiedError,
)

# === SAME API DATA ===
# Get real values from https://my.telegram.org -> API development tools.
load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

SESSIONS_DIR = Path("sessions")


async def check_one(session_path: Path) -> None:
    client = TelegramClient(str(session_path.with_suffix("")), API_ID, API_HASH)

    await client.connect()

    if not await client.is_user_authorized():
        print(f"[{session_path.name}] NOT authorized")
        await client.disconnect()
        return

    try:
        me = await client.get_me()
        print(f"[{session_path.name}] OK - {me.first_name} (@{me.username})")
    except Exception as e:
        print(f"[{session_path.name}] Connected but get_me() failed: {e}")
    finally:
        await client.disconnect()


async def send_test_message(session_path: Path, target_username: str) -> None:
    """Kept for reference / manual use only - not called from check_all_sessions()."""
    client = TelegramClient(str(session_path.with_suffix("")), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print(f"[{session_path.name}] Session is NOT authorized!")
        await client.disconnect()
        return

    me = await client.get_me()
    print(f"[{session_path.name}] Authorized as: {me.first_name} (@{me.username})")

    try:
        await client.send_message(target_username, "Test message from Telethon session")
        print(f"[{session_path.name}] Message sent successfully!")
    except UsernameNotOccupiedError:
        print(f"[{session_path.name}] Failed: no user with username @{target_username} exists.")
    except UserPrivacyRestrictedError:
        print(f"[{session_path.name}] Failed: that user's privacy settings block messages from you.")
    except (PeerFloodError, FloodWaitError) as e:
        print(f"[{session_path.name}] Failed: rate-limited by Telegram ({e}).")
    except Exception as e:
        print(f"[{session_path.name}] Failed to send message: {e}")
    finally:
        await client.disconnect()


async def check_all_sessions() -> None:
    if not SESSIONS_DIR.is_dir():
        print(f"'{SESSIONS_DIR}' folder not found - run the tdata->session converter first")
        return

    session_files = sorted(SESSIONS_DIR.glob("*.session"))

    if not session_files:
        print(f"No .session files found in '{SESSIONS_DIR}'")
        return

    print(f"Found {len(session_files)} session(s)\n")

    for session_path in session_files:
        await check_one(session_path)


if __name__ == "__main__":
    asyncio.run(check_all_sessions())
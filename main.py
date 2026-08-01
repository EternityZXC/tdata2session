import asyncio

from tdata_to_session import main as create_sessions_from_tdata
from verify_session import check_all_sessions


MENU = """
1) Create sessions from tdata folders (tdata_accounts/ -> sessions/)
2) Check all sessions in sessions/
0) Exit
"""


async def run() -> None:
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            await create_sessions_from_tdata()
        elif choice == "2":
            await check_all_sessions()
        elif choice == "0":
            break
        else:
            print("Not a valid option, try again.")


if __name__ == "__main__":
    asyncio.run(run())
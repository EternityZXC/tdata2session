# tdata2session

Batch-convert Telegram Desktop `tdata` folders into Telethon `.session` files.

Drop one or more `tdata` account folders into `tdata_accounts/`, run the
converter, and get out a `.session` file per account, named
`account_(@username).session`.

## Requirements

- Python **3.11** (opentele's dependencies, notably PyQt5, are not reliably
  installable on newer Python versions such as 3.13/3.14 as of writing)

## Install

```bash
py -3.11 -m venv .venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your own API credentials from
[my.telegram.org](https://my.telegram.org):

```
API_ID=your_api_id_here
API_HASH=your_api_hash_here
```

## Usage

1. Put each account's `tdata` folder inside `tdata_accounts/`, one
   subfolder per account:

   ```
   tdata_accounts/
     acc1/
     acc2/
     acc3/
   ```

2. Run the menu:

   ```bash
   python main.py
   ```

   - **Option 1** - convert all folders in `tdata_accounts/` into `.session`
     files saved in `sessions/`
   - **Option 2** - check every `.session` file in `sessions/` (confirms it's
     still authorized and logs the account's name)

## Notes

- `.env`, `tdata_accounts/`, and `sessions/` are all git-ignored - session
  files and API credentials should never be committed.
- Message-sending is intentionally not exposed through the menu.
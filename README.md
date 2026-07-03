# Telegram personal agent scaffold

This project logs in to a Telegram user account via GramJS and stores the session locally so you do not need to authenticate every run.

## Setup

1. Get `TG_API_ID` and `TG_API_HASH` from [my.telegram.org/apps](https://my.telegram.org/apps).
2. Copy `.env.example` to `.env` and fill in the values.
3. Install dependencies:

```bash
npm install
```

4. Log in for the first time:

```bash
npm run login
```

The saved session is written to `.data/telegram.session` by default.

If Russian text looks broken in Windows Terminal or PowerShell, run the CLI from this project entrypoint:

```bash
npm run agent
```

The app now switches the Windows console to UTF-8 at startup as a best-effort fix.

## Commands

```bash
npm run whoami
npm run dialogs -- 10
npm run archive -- 200 200 private
npm run sync-archive
npm run brief
npm run send -- me "hello"
npm run send -- me file=.tmp/message.txt
npm run broadcast -- peers=.tmp/peers.txt file=.tmp/message.txt
npm run broadcast -- peers=.tmp/peers.txt file=.tmp/message.txt apply
npm run bottest -- /start
npm run bottest -- ARM_PAMM_bot "/start"
npm run botlog -- ARM_PAMM_bot 10
npm run agent
npm run site
```

## Site

- The personal site for `R Systems` lives in [`index.html`](index.html).
- Run `npm run site` and open `http://127.0.0.1:4173`.
- Or run `npm run docker:up` and open `http://127.0.0.1:8888`.
- The current site uses your Telegram handle `@Alexandr_Ryzhkov` and phone number as the contact CTA.
- This root-level static site is ready to connect to GitHub and Vercel without a framework rewrite.

## Notes

- Do not commit your `.env` or session file.
- The API hash is secret.
- The `agent` command is a local CLI base that can be extended with your own task logic.
- `send file=message.txt` reads message text from a UTF-8 file so PowerShell encoding does not corrupt Cyrillic content.
- `broadcast` is dry-run by default. Add `apply` to actually send, and keep the recipients in a newline-separated file.
- `bottest` sends a message to your target bot and waits for the first reply.

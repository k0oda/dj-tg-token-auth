# DJ-TG-TOKEN-AUTH

This is a project, containing solution for test case at ANGRY company.
Project consists of two parts:
- Django application
- Aiogram bot

## Django Application

1. Implements `TelegramBackend` authentication backend, providing method for users authentication using new `AuthToken` model.
2. Add `AuthToken` model, which stores current `token`, `session_key`, `created_at` and `expires_at`, also providing static method for new AuthTokens' objects creation.
3. Implements `telegram_login` API endpoint for accepting data from aiogram bot.

## Aiogram Bot

1. Accepts `token`, pasted into start command URL, gets data about currently logged in user and send it to `telegram_login` endpoint.

## Tech Stack

- Python 3.12.3
- Django 5.1.3
- Aiogram 3.15.0
- Aiohttp 3.10.11

## Installation
Put `.env` file into the `dj_tg_auth` folder via:
```bash
cp dj_tg_auth/.env.ci dj_tg_auth/.env
```
Modify it for your needs
Then run containers using:
```bash
make run
```
And then run installation script:
```bash
make install
```
For linting use:
```bash
make lint
```

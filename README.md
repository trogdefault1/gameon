# GameOn Gatekeeper Token Generator with CapMonster Cloud Integration

[![CapMonster Cloud](https://img.shields.io/badge/Powered%20by-CapMonster%20Cloud-blue)](https://capmonster.cloud)

A Python solution for bypassing GameOn's Turnstile captcha protection using [CapMonster Cloud](https://capmonster.cloud) automated captcha solving service.

## What This Does

This script generates fingerprint IDs and solves Turnstile captchas for GameOn's gatekeeper API. It creates session data (fingerprint + solved token) that can be used for further API calls.

## Setup

1. **Install dependencies:**
   ```bash
   pip install tls-client colorama requests
   ```

2. **Configure API key:**
   Edit `gameon_simplified.py` and update:
   ```python
   CAPMONSTER_CLOUD_API_KEY = "your_actual_api_key_here"
   ```

## Usage

```bash
python gameon_simplified.py
```

## How It Works

1. **Fingerprint Generation**: Creates fingerprint IDs using JavaScript logic:
   ```javascript
   'fp_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now()
   ```

2. **Turnstile Solving**: Uses CapMonster Cloud API to solve Turnstile captchas

3. **Session Data**: Combines fingerprint and solved token for API use

## Output

The script generates `session_data.json` with:
```json
{
    "fingerprint": "fp_4f5j3k2l1_1761051819236",
    "turnstile_token": "solved_turnstile_token",
    "website_url": "https://www.gameon.games/",
    "website_key": "0x4AAAAAABww3o50PYtmz9wv",
    "generated_at": 1761051819236
}
```

## Troubleshooting

- **Invalid API Key**: Edit `CAPMONSTER_CLOUD_API_KEY` in the script
- **Task Timeout**: Check CapMonster Cloud service status and balance
- **Connection Failed**: Check internet connection

---

**Powered by [CapMonster Cloud](https://capmonster.cloud)**

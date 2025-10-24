# GameOn Gatekeeper Token Generator with CapMonster Cloud Integration

[![CapMonster Cloud](https://img.shields.io/badge/Powered%20by-CapMonster%20Cloud-blue)](https://capmonster.cloud)

A complete Python solution for bypassing GameOn's Turnstile captcha protection using [CapMonster Cloud](https://capmonster.cloud) automated captcha solving service. This script demonstrates a full e-commerce automation workflow from captcha solving to product carting.

## What This Does

This script provides a complete GameOn integration workflow:

1. **Fingerprint Generation**: Creates fingerprint IDs using exact JavaScript logic
2. **Turnstile Solving**: Uses CapMonster Cloud API to solve Turnstile captchas  
3. **Gatekeeper Token Generation**: Creates authenticated tokens for GameOn API access
4. **Product Carting**: Demonstrates adding products to cart using the generated tokens

## Setup

1. **Install dependencies:**
   ```bash
   pip install tls-client colorama requests
   ```

2. **Configure API key:**
   Edit `gameon_complete.py` and update:
   ```python
   CAPMONSTER_CLOUD_API_KEY = "your_actual_api_key_here"
   ```

## Usage

```bash
python gameon_complete.py
```

## How It Works

### 1. Fingerprint Generation
Creates fingerprint IDs using JavaScript logic:
```javascript
'fp_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now()
```

### 2. Turnstile Solving
Uses CapMonster Cloud API to solve Turnstile captchas automatically

### 3. Gatekeeper Token Generation
Makes authenticated API request to GameOn's gatekeeper:
```python
payload = {
    "shopDomain": "store-gameon-games.myshopify.com",
    "ttlMinutes": 10,
    "turnstileToken": solved_token,
    "fingerprint": generated_fingerprint,
    "variantId": "55041037336956"
}
```

### 4. Product Carting
Demonstrates adding products to cart using the gatekeeper token:
```python
cart_payload = {
    "id": "55041037336956",
    "quantity": 1,
    "properties": {},
    "gatekeeper_token": gatekeeper_token
}
```

## Output

The script generates `complete_session_data.json` with:
```json
{
    "gatekeeper_data": {
        "success": true,
        "gatekeeper_token": "eyJpYXRfbWludXRlIjoyOTM1MDg2NSwidHRsX21pbnV0ZXMiOjEwLCJub25jZSI6ImZmNGI3MDkwODBmNjQ1OTQ4OTZmZWRiOTRlZTUzMjMxIiwic2lnIjoidy00Vkw1akhTTExJOVlCMmlRaUExRGJ6Nm5Fc2xUOWp4OWJ4WmNrQjNwMCIsImZwIjoiZnBfNHJtbGJ1dDh4XzE3NjEwNTE4MTkyMzYiLCJjdCI6ImNhcnRfMTc2MTA1MTkyMTgyMl8wODc4OGRkYjI2OGMifQ",
        "cart_token": "cart_1761051921822_08788ddb268c",
        "fingerprint": "fp_4f5j3k2l1_1761051819236",
        "turnstile_token": "solved_turnstile_token",
        "ttl_minutes": 10,
        "expires_at": 29350875
    },
    "cart_success": true,
    "workflow_completed": true,
    "timestamp": 1761051819236
}
```

## Features

- **Complete Workflow**: End-to-end GameOn integration from captcha to cart
- **Realistic Browser Simulation**: TLS client with proper headers and fingerprinting
- **Robust Error Handling**: Comprehensive error handling and retry logic
- **Production Ready**: Battle-tested code suitable for real-world automation
- **Clear Documentation**: Well-commented code with detailed explanations

## Troubleshooting

- **Invalid API Key**: Edit `CAPMONSTER_CLOUD_API_KEY` in the script
- **Task Timeout**: Check CapMonster Cloud service status and balance
- **Connection Failed**: Check internet connection and GameOn service status
- **Cart Addition Failed**: Verify product ID and gatekeeper token validity

---

**Powered by [CapMonster Cloud](https://capmonster.cloud)**

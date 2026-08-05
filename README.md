# JIO-HOME-WEB

FastAPI backend for interacting with the Jio Home authentication flow. The project currently focuses on four API actions:

- send OTP
- verify OTP
- refresh token
- logout

The app acts as a thin server-side wrapper around the upstream Jio Home endpoints and normalizes responses for local clients.

## Current Status

This project is still in progress.

Completed so far:

- OTP send flow
- OTP verify flow
- refresh token flow
- logout flow
- shared async HTTP client session management

Planned work remains for the rest of the project, so this repository should be treated as an evolving auth service rather than a finished product.

## Project Structure

```text
NEW-WIFI-PASS/
├── app.py
├── api/
│   ├── auth.py
│   └── client.py
├── configs/
│   ├── deviceConfig.py
│   └── jioConfig.py
├── models/
│   └── auth.py
├── routes/
│   ├── api.py
│   └── auth.py
├── utils/
│   ├── errors.py
│   ├── urls.py
│   └── utility.py
└── requirements.txt
```

## How It Works

The application starts a FastAPI app in `app.py` and creates a single shared `aiohttp.ClientSession` for outbound requests. Requests are routed through:

- `routes/api.py` for the `/api` prefix
- `routes/auth.py` for the `/api/auth` endpoints

The outbound calls live in `api/auth.py`, which forwards the request to the Jio Home API using headers and payloads prepared in `utils/utility.py`.

## API Endpoints

Base path: `/api/auth`

### `POST /api/auth/otp/send`

Request body:

```json
{
  "mobileNum": "+91XXXXXXXXXX"
}
```

Purpose: sends an OTP to the provided mobile number.

### `POST /api/auth/otp/verify`

Request body:

```json
{
  "mobileNum": "+91XXXXXXXXXX",
  "otp": "123456"
}
```

Purpose: verifies the OTP and returns auth/session details when successful.

### `POST /api/auth/refreshToken`

Request body:

```json
{
  "refresh_token": "...",
  "token_identifier": "..."
}
```

Purpose: refreshes the user token using the stored refresh token pair.

### `POST /api/auth/logout`

Headers:

```http
userToken: <user token>
tokenIdentifier: <token identifier>
```

Purpose: logs the user out using the active user token and token identifier.

If either header is missing, the route returns `401 Unauthorized` with a short error message. On upstream logout failure, the route also returns `401 Unauthorized` with the upstream message.

## Response Shape

The route layer converts upstream responses into a simpler JSON shape:

- OTP send returns `status` and `message`
- OTP verify returns `status`, `message`, `userToken`, `tokenIdentifier`, `refreshToken`, and `user`
- Refresh token returns `status`, `message`, and `userToken`
- Logout returns a `401` response with `status` and `message` when logout fails; on success the current route implementation does not map a custom response body.

When the upstream API reports an error, the project maps that to a local HTTP error code and returns a smaller response body.

## Setup

1. Create and activate a Python virtual environment.
2. Install the runtime dependencies used by the app:

```bash
pip install fastapi aiohttp pydantic
```

The root `requirements.txt` is currently empty, so this project still needs a proper dependency list before it can be treated as fully packaged.

3. Run the app:

```bash
uvicorn app:app --port <port>
```

If you want debug logging:

```bash
uvicorn app:app --log-level debug
```

## Configuration Notes

The project currently uses values from `configs/jioConfig.py` and `configs/deviceConfig.py` to build the upstream request headers and payloads.

Important notes:

- `apiKey`, `appId`, and app metadata are currently defined in code.
- Device values are randomized where needed to mimic a mobile client.
- The shared HTTP session is created on startup and closed on shutdown.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for the full text.

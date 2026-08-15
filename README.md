# JIO-HOME-WEB

FastAPI backend for interacting with the Jio Home authentication flow and device management. The project provides comprehensive API actions for:

**Authentication:**

- Send OTP to mobile number
- Verify OTP and retrieve auth tokens
- Refresh authentication tokens
- Logout from the system

**Dashboard/Device Management:**

- Retrieve user connection details
- Get network nodes information
- Fetch WiFi network details
- List connected devices
- Retrieve user profiles

The app acts as a thin server-side wrapper around the upstream Jio Home endpoints and normalizes responses for local clients.

## Current Status

✅ **Completed:**

- OTP send flow
- OTP verify flow
- Refresh token flow
- Logout flow
- User connection details endpoint
- Nodes management endpoint
- WiFi network details endpoint
- Devices listing endpoint
- User profiles endpoint
- Shared async HTTP client session management
- Request/response transformation filters
- Authentication middleware for protected routes
- Error handling with try-catch blocks on all endpoints
- Enhanced input validation (phone numbers, OTP, IDs)
- Custom exception classes for error scenarios
- HTTP status codes and error messages
- Health check endpoint (/health)

## Project Structure

```text
JIO-HOME-WEB/
├── app.py                          # Main FastAPI application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── LICENSE                         # Project license
│
├── api/                            # External API integrations
│   ├── auth.py                     # Authentication API calls to Jio Home
│   ├── client.py                   # Shared aiohttp client session
│   └── dashboard.py                # Dashboard/device management API calls
│
├── configs/                        # Configuration files
│   ├── deviceConfig.py             # Device configuration constants
│   └── jioConfig.py                # Jio Home API configuration
│
├── models/                         # Pydantic request/response models
│   ├── auth.py                     # Authentication models
│   └── dashboard.py                # Dashboard models
│
├── routes/                         # API endpoint routes
│   ├── api.py                      # Main API router
│   ├── auth.py                     # Authentication endpoints
│   └── dashboard.py                # Dashboard endpoints
│
├── transformers/                   # Response transformation & filtering
│   ├── auth_request_mapper.py      # Map auth requests
│   ├── auth_response_filter.py     # Filter/normalize auth responses
│   └── dashboard_response_filter.py # Filter/normalize dashboard responses
│
├── utils/                          # Utility functions & middleware
│   ├── errors.py                   # Custom exceptions
│   ├── urls.py                     # API endpoint URLs
│   └── utility.py                  # Helper functions & auth middleware
│
├── public/                         # Static assets
│   ├── CSS/                        # Stylesheets
│   └── JS/                         # JavaScript files
│
└── templates/                      # HTML templates
    └── 404.html                    # 404 error page

```

## How It Works

The application starts a FastAPI app in `app.py` and creates a single shared `aiohttp.ClientSession` for outbound requests. This ensures connection pooling and efficient resource management.

Requests are routed through:

- `routes/api.py` - Main router that includes all sub-routers
- `routes/auth.py` - Authentication endpoints (`/api/auth/*`)
- `routes/dashboard.py` - Dashboard endpoints (`/api/dashboard/*`)

The outbound calls are handled by:

- `api/auth.py` - Forwards requests to Jio Home Auth API
- `api/dashboard.py` - Forwards requests to Jio Home Dashboard API

Response transformation is done by:

- `transformers/auth_response_filter.py` - Normalizes auth responses
- `transformers/dashboard_response_filter.py` - Normalizes dashboard responses

## Features

### Error Handling

- All endpoints have try-catch error handling
- Proper HTTP status codes (400, 401, 404, 422, 500)
- Meaningful error messages returned to clients
- Exception handling for validation and runtime errors

### Input Validation

- Mobile number validation: Must start with +91 and be 13 characters
- OTP validation: Must be exactly 6 digits
- Customer ID and Location ID validation: Non-empty strings
- All validation errors return 422 status code with details

### Security

- Protected routes with authentication headers (userToken, tokenIdentifier)
- Header validation middleware
- Custom exception classes for different error scenarios

## API Endpoints

### Authentication Endpoints

Base path: `/api/auth`

#### `POST /api/auth/otp/send`

Sends an OTP to the provided mobile number.

**Request:**

```json
{
  "mobileNum": "+91XXXXXXXXXX"
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "OTP sent successfully",
  "data": {
    "requestId": "...",
    "mobileNum": "+91XXXXXXXXXX"
  }
}
```

**Status Codes:**

- `200 OK` - OTP sent successfully
- `400 Bad Request` - Invalid mobile number format
- `500 Internal Server Error` - Server error

---

#### `POST /api/auth/otp/verify`

Verifies the OTP and returns authentication tokens.

**Request:**

```json
{
  "mobileNum": "+91XXXXXXXXXX",
  "otp": "123456"
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "OTP verified successfully",
  "data": {
    "userToken": "...",
    "tokenIdentifier": "...",
    "refreshToken": "...",
    "userId": "...",
    "mobileNum": "+91XXXXXXXXXX"
  }
}
```

**Status Codes:**

- `200 OK` - OTP verified successfully
- `401 Unauthorized` - Invalid OTP
- `400 Bad Request` - Invalid request format
- `500 Internal Server Error` - Server error

---

#### `POST /api/auth/refreshToken`

Refreshes the user authentication token using the refresh token.

**Request:**

```json
{
  "refresh_token": "...",
  "token_identifier": "..."
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "userToken": "...",
    "tokenIdentifier": "...",
    "refreshToken": "..."
  }
}
```

**Status Codes:**

- `200 OK` - Token refreshed successfully
- `401 Unauthorized` - Invalid refresh token
- `400 Bad Request` - Invalid request format
- `500 Internal Server Error` - Server error

---

#### `POST /api/auth/logout` ⚠️ _Protected_

Logs out the user and invalidates their session.

**Headers (Required):**

```
userToken: <token>
tokenIdentifier: <identifier>
```

**Request:**

```json
{}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

**Status Codes:**

- `200 OK` - Logged out successfully
- `401 Unauthorized` - Missing or invalid auth headers
- `500 Internal Server Error` - Server error

---

### Dashboard Endpoints ⚠️ _All Protected_

Base path: `/api/dashboard`

**All dashboard endpoints require the following headers:**

```
userToken: <authentication_token>
tokenIdentifier: <token_identifier>
```

These headers are obtained from the `/api/auth/otp/verify` response.

---

#### `POST /api/dashboard/user`

Retrieves the user's connection details and account information.

**Headers (Required):**

```
userToken: <token>
tokenIdentifier: <identifier>
```

**Request:**

```json
{}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "User details retrieved successfully",
  "data": {
    "customerId": "...",
    "mobileNum": "+91XXXXXXXXXX",
    "accountStatus": "active",
    "connection": {
      "status": "active",
      "type": "broadband"
    }
  }
}
```

**Status Codes:**

- `200 OK` - User details retrieved
- `401 Unauthorized` - Invalid or missing auth headers
- `500 Internal Server Error` - Server error

---

#### `POST /api/dashboard/nodes`

Retrieves network nodes information for a specific customer location.

**Headers (Required):**

```
userToken: <token>
tokenIdentifier: <identifier>
```

**Request:**

```json
{
  "customerId": "...",
  "locationId": "..."
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "Nodes retrieved successfully",
  "data": {
    "nodes": [
      {
        "nodeId": "...",
        "nodeName": "...",
        "status": "online",
        "signal": "strong"
      }
    ]
  }
}
```

**Status Codes:**

- `200 OK` - Nodes retrieved
- `401 Unauthorized` - Invalid or missing auth headers
- `400 Bad Request` - Invalid customerId or locationId
- `500 Internal Server Error` - Server error

---

#### `POST /api/dashboard/wifi`

Retrieves WiFi network details for a specific customer location.

**Headers (Required):**

```
userToken: <token>
tokenIdentifier: <identifier>
```

**Request:**

```json
{
  "customerId": "...",
  "locationId": "..."
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "WiFi networks retrieved successfully",
  "data": {
    "networks": [
      {
        "ssid": "Jio-Home-XXXX",
        "band": "2.4GHz",
        "channel": 6,
        "security": "WPA2"
      }
    ]
  }
}
```

**Status Codes:**

- `200 OK` - WiFi networks retrieved
- `401 Unauthorized` - Invalid or missing auth headers
- `400 Bad Request` - Invalid customerId or locationId
- `500 Internal Server Error` - Server error

---

#### `POST /api/dashboard/devices`

Retrieves connected devices for a specific customer location.

**Headers (Required):**

```
userToken: <token>
tokenIdentifier: <identifier>
```

**Request:**

```json
{
  "customerId": "...",
  "locationId": "..."
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "Devices retrieved successfully",
  "data": {
    "devices": [
      {
        "deviceId": "...",
        "deviceName": "...",
        "deviceType": "jiofi",
        "status": "online",
        "ipAddress": "192.168.1.x"
      }
    ]
  }
}
```

**Status Codes:**

- `200 OK` - Devices retrieved
- `401 Unauthorized` - Invalid or missing auth headers
- `400 Bad Request` - Invalid customerId or locationId
- `500 Internal Server Error` - Server error

---

#### `POST /api/dashboard/profiles`

Retrieves user profiles/configurations for a specific customer location.

**Headers (Required):**

```
userToken: <token>
tokenIdentifier: <identifier>
```

**Request:**

```json
{
  "customerId": "...",
  "locationId": "..."
}
```

**Response (Success):**

```json
{
  "success": true,
  "message": "Profiles retrieved successfully",
  "data": {
    "profiles": [
      {
        "profileId": "...",
        "profileName": "...",
        "status": "active"
      }
    ]
  }
}
```

**Status Codes:**

- `200 OK` - Profiles retrieved
- `401 Unauthorized` - Invalid or missing auth headers
- `400 Bad Request` - Invalid customerId or locationId
- `500 Internal Server Error` - Server error

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd JIO-HOME-WEB
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables:**
   - Create a `.env` file in the root directory (optional, for sensitive configs)
   - Update [configs/jioConfig.py](configs/jioConfig.py) with your Jio API credentials
   - Update [configs/deviceConfig.py](configs/deviceConfig.py) with device-specific settings

6. **Run the application:**

   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API:**
   - Base URL: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs` (Swagger UI)
   - Alternative Docs: `http://localhost:8000/redoc` (ReDoc)

---

## Configuration

### Environment Variables

Configure the following in `configs/jioConfig.py`:

```python
appId = "YOUR_JIO_APP_ID"
apiKey = "YOUR_JIO_API_KEY"
```

### API Configuration

The application connects to Jio Home API endpoints. Update the host URL in [utils/urls.py](utils/urls.py) if needed.

---

## Authentication Flow

### User Authentication Workflow

1. **Send OTP:**
   - User sends their mobile number to `/api/auth/otp/send`
   - Receives OTP on their mobile

2. **Verify OTP:**
   - User sends OTP to `/api/auth/otp/verify`
   - Receives `userToken`, `tokenIdentifier`, and `refreshToken`

3. **Access Protected Endpoints:**
   - Include `userToken` and `tokenIdentifier` headers in all dashboard requests

4. **Token Refresh:**
   - When token expires, use `/api/auth/refreshToken` with `refresh_token` and `token_identifier`
   - Receives new `userToken` and `tokenIdentifier`

5. **Logout:**
   - Call `/api/auth/logout` with current tokens to invalidate session

---

## License

Licensed under the terms in [LICENSE](LICENSE)

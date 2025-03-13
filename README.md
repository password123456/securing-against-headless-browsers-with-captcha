# Securing Against Headless Browsers with CAPTCHA
Securing Against Headless Browsers with CAPTCHA: Hands-On Implementation

![made-with-python][made-with-python]
![Python Versions][pyversion-button]
![Hits][hits-button]

[pyversion-button]: https://img.shields.io/pypi/pyversions/Markdown.svg
[made-with-python]: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
[hits-button]: https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fpassword123456%2Fsecuring-against-headless-browsers-with-captcha&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false


This repository implements a robust headless browser detection system designed to protect web applications, specifically targeting membership registration endpoints (`/memberships`). Built with **Python Flask**, it leverages advanced detection techniques and integrates Google reCAPTCHA v2 for bot verification. The system is tailored for security engineers looking to mitigate automated attacks by identifying and challenging headless browsers.

If you find this helpful, please the "star"🌟 to support further improvements.

## Features

- **Multi-Layered Detection**: Combines User-Agent analysis, WebDriver detection, Canvas Fingerprinting, WebGL checks, timing analysis, user interaction validation, and request frequency monitoring.
- **Score-Based Evaluation**: Assigns a headless score (0-100); scores >50 trigger CAPTCHA verification.
- **reCAPTCHA Integration**: Redirects suspected headless clients to a CAPTCHA challenge, ensuring human verification.
- **Session Management**: Uses UUID-based session tokens to track verification state and redirect users back to the original page upon success.
- **Dual Implementation**: Offers flexibility with Spring Boot (Java) and Flask (Python) backends.

## Project Structure  

```plaintext
flask/
├── app.py
├── requirements.txt
├── static/
|   └── index.html
```

## Use Case

This system is designed to secure the `/memberships` endpoint (e.g., a registration page) by:
1. Detecting headless browsers during access attempts.
2. Redirecting suspicious clients to a CAPTCHA challenge (`/captcha`).
3. Allowing verified users to return to `/memberships` with a "you are human" confirmation.

## Getting Started

1. Clone the repository:
```
git clone https://github.com/password123456/securing-against-headless-browsers-with-captcha
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Configure reCAPTCHA
- Open `app.py`.
- Replace `your-recaptcha-site-key` and `your-recaptcha-secret-key` with your Google reCAPTCHA keys.
- Update `app.secret_key` with a secure random string.

4. Run the Application
```
python app.py
```
- Access `http://localhost:5000/memberships` in a browser.

5. Client-Side
- The `static/index.html` handles client-side logic and reCAPTCHA rendering.

## How It Works
1. Initial Request (`/memberships`):
- The server evaluates browser attributes (User-Agent, WebDriver, etc.) and assigns a headless score.
- If score ≤ 50: Returns "message": "you are human".
- If score > 50: Returns a redirect URL (/captcha?session_token=...) with reCAPTCHA Site Key.

2. CAPTCHA Challenge (`/captcha`):
- Client is redirected to a page displaying Google reCAPTCHA v2.
- User completes the CAPTCHA challenge.

3. Verification (`/verify-captcha`):
- Client submits the reCAPTCHA response and session token.
- Server validates with Google’s API.
- Success: Returns `"message": "you are human"` and redirects to `/memberships`.
- Failure: Returns `"message": "Failed: Likely Bot"`.

## Detection Techniques
- **User-Agent:** Identifies strings like `HeadlessChrome`.
- **WebDriver:** Checks for `navigator.webdriver`.
- **Canvas Fingerprinting:** Detects missing or invalid canvas outputs.
- **WebGL:** Validates renderer and vendor info.
- **Timing Analysis:** Flags suspiciously fast requests (<10ms).
- **User Interaction:** Requires click events.
- **Request Frequency:** Monitors rapid successive requests (<50ms).

## Security Considerations
- **reCAPTCHA:** Replace placeholder keys with production keys and secure them (e.g., environment variables).
- **Session Tokens:** UUIDs ensure uniqueness; consider expiring tokens after a timeout.
- **Rate Limiting:** Add to `/memberships` to prevent brute-force attempts (not implemented here).

## Testing
- **Normal Browser:** Access `/memberships` → Expect "you are human".
- **Headless Browser** (e.g., Puppeteer):
  - Access `/memberships` → Redirect to `/captcha`.
  - Complete CAPTCHA → Redirect back to `/memberships` with "you are human".

  

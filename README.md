# Authentication Project

This project provides user authentication (Register, Login, Logout, and Profile `/me/`) using Django Rest Framework with CSRF + cookie-based sessions.

---

## 🚀 Setup Instructions

### 1. Clone or copy the project
Place the project in your desired folder (e.g. `C:\Users\USER\Desktop\pythonProj`).

### 2. Create and activate virtual environment
cmd
python -m venv venv

venv\Scripts\activate

3. Install dependencies
cmd

pip install -r requirements.txt

4. Apply database migrations
cmd

python manage.py migrate

5. Run the development server
cmd

python manage.py runserver



⚡ API Usage (with curl)
These commands are written for Windows Command Prompt (cmd.exe).
They use cookies.txt to persist the login session.

1. Get CSRF Token
cmd

curl -c cookies.txt -b cookies.txt http://127.0.0.1:8000/api/csrf/
You’ll receive something like:

2. Register a new user
cmd

curl -X POST http://127.0.0.1:8000/api/register/ ^
  -H "Content-Type: application/json" ^
  -H "X-CSRFToken: d0etwDkQTSK59blCO7Mv4lFjq7BIEKtZ" ^
  -b cookies.txt -c cookies.txt ^
  -d "{\"email\":\"yash@example.com\", \"password\":\"SuperSecret123\"}"

3. Login
cmd

curl -X POST http://127.0.0.1:8000/api/login/ ^
  -H "Content-Type: application/json" ^
  -H "X-CSRFToken: d0etwDkQTSK59blCO7Mv4lFjq7BIEKtZ" ^
  -b cookies.txt -c cookies.txt ^
  -d "{\"email\":\"yash@example.com\", \"password\":\"SuperSecret123\"}"

cmd

curl -X GET http://127.0.0.1:8000/api/me/ ^
  -H "X-CSRFToken: d0etwDkQTSK59blCO7Mv4lFjq7BIEKtZ" ^
  -b cookies.txt -c cookies.txt

5. Logout
cmd

curl -X POST http://127.0.0.1:8000/api/logout/ ^
  -H "X-CSRFToken: d0etwDkQTSK59blCO7Mv4lFjq7BIEKtZ" ^
  -b cookies.txt -c cookies.txt

6. Verify logout
cmd

curl -X GET http://127.0.0.1:8000/api/me/ ^
  -H "X-CSRFToken: d0etwDkQTSK59blCO7Mv4lFjq7BIEKtZ" ^
  -b cookies.txt -c cookies.txt

✅ Workflow Summary

Start server → python manage.py runserver

Get CSRF token → /api/csrf/

Register user → /api/register/

Login → /api/login/

Get profile → /api/me/

Logout → /api/logout/

Verify logout → /api/me/



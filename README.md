# 🔐 Secure Authentication System

A full-featured secure authentication system implementing real-world security practices such as password hashing, Two-Factor Authentication (2FA), JWT-based authentication, and Role-Based Access Control (RBAC).

---

## 🚀 Features

- User Registration & Login
- Secure Password Hashing
- Two-Factor Authentication (2FA) using Google Authenticator
- JWT Token-Based Authentication
- Role-Based Access Control (Admin, Manager, User)
- Protected API Routes
- Clean and Modular Code Structure

---

## 🧠 System Flow

1. User registers
2. Password is hashed and stored securely
3. 2FA secret is generated
4. QR code is displayed
5. User scans QR code using authenticator app
6. User logs in with email and password
7. User enters 2FA code
8. System verifies credentials and 2FA
9. JWT token is generated
10. User accesses protected routes
11. Access is controlled based on role

---

## 🔑 Roles

- **Admin** → Full system access
- **Manager** → Limited management access
- **User** → Basic access

---

## 🔐 Security Features

- Password hashing (no plain text passwords)
- Time-based One-Time Password (TOTP) 2FA
- JWT authentication with expiration
- Role-based authorization
- Protected API endpoints

---

## 📂 Project Structure

```
project/
│── app.py
│── database.py
│── middleware.py
│── requirements.txt
│── secure_system.db
│── templates/
│── static/
```

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/secure-authentication-system.git
cd secure-authentication-system
pip install -r requirements.txt
python database.py
python app.py
```

---

## 🔌 API Endpoints

| Endpoint           | Description              |
|------------------|--------------------------|
| POST /api/register | Register a new user      |
| POST /api/login    | Login user               |
| POST /api/verify-2fa | Verify 2FA code       |
| GET /api/profile   | User profile (Protected) |
| GET /api/admin     | Admin route              |
| GET /api/manager   | Manager route            |
| GET /api/user      | User route               |

---

## 🧪 Testing

You can test the APIs using:
- Postman
- Frontend pages

Make sure to:
- Register user
- Scan QR code
- Login + verify 2FA
- Use token to access protected routes

---

## 🛠️ Technologies Used

- Python (Flask)
- SQLite
- PyJWT
- pyotp
- qrcode
- Werkzeug

---

## 👨‍💻 Author

Mahmoud Mohamed Gomaa  
ID: 2305188

---

## 📌 Notes

This project was developed as part of the **Data Integrity and Authentication** course.


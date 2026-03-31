# 🔐 Fingerprint-Based ATM Security System

## 🚀 Overview
A secure ATM authentication system that replaces traditional PIN-based access with **biometric fingerprint verification** and **OTP-based multi-factor authentication**.

The system integrates **hardware (fingerprint sensor + Arduino)** with a **web-based application**, enabling secure, real-time user verification and fraud detection.

---

## 💡 Problem Statement
Traditional ATM systems rely on PIN-based authentication, which is vulnerable to:
- Shoulder surfing
- PIN theft
- Unauthorized access

---

## ✅ Solution
This project implements a **multi-layered authentication mechanism**:
- 🔐 Fingerprint-based identity verification
- 📲 OTP-based secondary authentication
- 🚨 Real-time fraud alerts (sound + notifications)

---

## 🛠 Tech Stack

### 🔹 Backend
- Python
- Flask
- SQLite

### 🔹 Frontend
- HTML, CSS, JavaScript
- Bootstrap

### 🔹 Hardware
- Arduino (NodeMCU)
- Fingerprint Sensor

---

## 🔥 Key Features
- Biometric fingerprint authentication
- OTP-based multi-factor verification
- Fraud alert system (audio + notifications)
- Firebase integration for alerts/storage
- Admin dashboard interface
- Image/data upload support

---

## 🧠 System Workflow
1. User initiates authentication
2. Fingerprint is scanned and validated
3. OTP is generated and sent to the user
4. User enters OTP
5. System verifies credentials
6. Access is granted or denied
7. Suspicious activity triggers alert mechanisms

---

## 📂 Project Structure
fingerprint-atm-system/
│
├── backend/ # Core application logic
├── frontend/ # UI (templates + static files)
├── hardware/ # Arduino + fingerprint integration
├── data/ # Dataset storage
├── uploads/ # User uploads (ignored in git)
├── assets/ # Static assets (alarm, etc.)
├── screenshots/ # Project screenshots
├── .gitignore
└── README.md
---

## How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/fingerprint-atm-system.git
cd fingerprint-atm-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python backend/app.py
```

### 4. Open in Browser
```
http://localhost:5000
```

## Screenshots

- Fingerprint Scan 
- Login Page
- OTP Verification Page
- OTP Notification
- Database View

## Notes

- `__pycache__/`, `.db`, and `uploads/` are excluded using `.gitignore`
- Hardware setup (Arduino + fingerprint sensor) is required for full functionality

## Future Improvements

- Convert backend to Spring Boot (Java)
- Implement secure authentication (JWT)
- Deploy on cloud (AWS / Render)
- Improve UI/UX and responsiveness

## Author

Preet Sahu

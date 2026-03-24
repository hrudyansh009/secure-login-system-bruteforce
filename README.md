# 🔐 Secure Login System with Attack Prevention

A secure authentication system built using Python Flask.  
This project focuses on implementing **secure login mechanisms** and **basic attack prevention techniques** in a clear and educational way.

---

## 📌 Project Overview

This project demonstrates how modern web applications handle authentication securely while protecting against common attacks such as brute-force login attempts and information leakage.

The goal of this project is **learning and correct security implementation**, not UI design or production deployment.

---

## 🛡️ Security Features

### Secure Password Handling
- Passwords are **hashed** before storage
- No plain-text password storage
- Uses industry-accepted hashing utilities

### Brute-Force Attack Prevention
- Tracks failed login attempts
- Temporarily locks accounts after repeated failures
- Automatically unlocks accounts after a cooldown period

### Secure Authentication Flow
- Generic login error messages to prevent username enumeration
- Secure session handling
- Logout functionality to invalidate sessions

### Input Validation & Error Handling
- Server-side input validation
- Graceful error handling without leaking sensitive details

---

## 🚀 How to Run the Application

### Requirements
- Python 3.8+
- pip

### Installation

```bash
git clone <repository-url>
cd secure-login-system
pip install -r requirements.txt
python app.py
````

The application will be available at:

```
http://127.0.0.1:5000
```

---

## 💻 Usage

* Register a new user account
* Login using registered credentials
* Trigger account lockout by entering incorrect passwords multiple times
* Observe lockout behaviour and secure error handling

---

## 📁 Project Structure

```
app.py              → Main Flask application
database.py         → Database schema and models
security.py         → Password hashing and security helpers
templates/          → Minimal HTML templates
requirements.txt    → Dependencies
README.md           → Documentation
```

Each component is kept separate to maintain clean and understandable code.

---

## 🎯 Learning Outcomes

Through this project, I gained hands-on experience with:

* Secure authentication design
* Password hashing best practices
* Brute-force attack mitigation
* Secure session management
* Ethical security development
* Writing clean, readable Flask applications

---

## ⚠️ Ethical Disclaimer

This project is intended **only for educational purposes**.

* Use only on systems you own or have permission to test
* Not intended for production use without further hardening
* Built strictly as part of a learning and internship task

---

## 📄 License

This project is released for educational use only. Use responsibly.

---

**Security is a mindset, not just code.**

---

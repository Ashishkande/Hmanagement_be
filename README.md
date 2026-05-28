# FastAPI + Redis Authentication Backend

## Features
- Register
- OTP Verification
- Login
- Forgot Password
- Reset Password
- Resend OTP
- JWT Authentication
- Redis OTP Expiry

---

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Run Redis

```bash
docker run -d --name redis -p 6379:6379 redis
```

---

### 3. Create PostgreSQL Database

Database name:

```
authdb
```

---

### 4. Configure .env

Copy:

```bash
.env.example -> .env
```

---

### 5. Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

## Swagger API Docs

```
http://127.0.0.1:8000/docs
```

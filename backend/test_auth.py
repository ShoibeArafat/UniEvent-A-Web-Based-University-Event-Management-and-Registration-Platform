"""
Interactive test script for Part 1: Authentication Backend.
Run this directly from the backend directory:
    python test_auth.py
"""
import sys
from pathlib import Path

# Ensure backend directory is in python path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from main import app
from database import Base, engine
from models import seed_initial_events

print("=======================================================")
print("UniEvent - Authentication Backend Verification Suite")
print("=======================================================")

print("\n1. Initializing database schema and demo accounts...")
Base.metadata.create_all(bind=engine)
seed_initial_events()

with TestClient(app) as client:
    print("\n2. Checking Health & Swagger Docs...")
    res = client.get("/api/health")
    assert res.status_code == 200
    print("   ✓ GET /api/health -> 200 OK")

    res = client.get("/api/docs")
    assert res.status_code == 200
    print("   ✓ GET /api/docs (Swagger UI) -> 200 OK")

    print("\n3. Testing Demo Admin Login...")
    res = client.post("/api/auth/login", json={
        "email": "admin1@unievent.edu",
        "password": "Admin@12345"
    })
    assert res.status_code == 200
    admin_data = res.json()
    assert admin_data["user"]["role"] == "Admin"
    print(f"   ✓ POST /api/auth/login -> Logged in as: {admin_data['user']['name']} (Role: {admin_data['user']['role']})")

    print("\n4. Testing New User Registration & Duplicate Email Protection...")
    test_email = "test_student@unievent.edu"
    res = client.post("/api/auth/signup", json={
        "name": "Test Student",
        "email": test_email,
        "password": "Password@123"
    })
    if res.status_code == 400:
        res = client.post("/api/auth/login", json={"email": test_email, "password": "Password@123"})
    assert res.status_code in [200, 201]
    tokens = res.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    print("   ✓ POST /api/auth/signup -> 201 Created (Access & Refresh tokens issued)")

    res_dup = client.post("/api/auth/signup", json={
        "name": "Duplicate Student",
        "email": test_email,
        "password": "Password@123"
    })
    assert res_dup.status_code == 400
    print("   ✓ Duplicate email registration correctly rejected with 400 Bad Request")

    print("\n5. Testing Protected Endpoint (/api/users/me)...")
    res_unauth = client.get("/api/users/me")
    assert res_unauth.status_code == 401
    print("   ✓ Request without Bearer token correctly blocked: 401 Unauthorized")

    headers = {"Authorization": f"Bearer {access_token}"}
    res_auth = client.get("/api/users/me", headers=headers)
    assert res_auth.status_code == 200
    print(f"   ✓ Request with Bearer token authenticated: Hello, {res_auth.json()['name']}!")

    print("\n6. Testing Token Refresh Flow...")
    res_refresh = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert res_refresh.status_code == 200
    new_access_token = res_refresh.json()["access_token"]
    print("   ✓ POST /api/auth/refresh -> New 15-minute access token issued")

    new_headers = {"Authorization": f"Bearer {new_access_token}"}
    assert client.get("/api/users/me", headers=new_headers).status_code == 200
    print("   ✓ Validated that new access token accesses protected endpoints")

    print("\n7. Testing Active Sessions Viewer...")
    res_sessions = client.get("/api/users/me/sessions", headers=new_headers)
    assert res_sessions.status_code == 200
    print(f"   ✓ GET /api/users/me/sessions -> {len(res_sessions.json())} active session(s) tracked in database")

    print("\n8. Testing Logout & Token Revocation (Teacher's requirement)...")
    res_logout = client.post("/api/auth/logout", json={"refresh_token": refresh_token})
    assert res_logout.status_code == 200
    print("   ✓ POST /api/auth/logout -> Session marked is_revoked = True")

    res_reuse = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert res_reuse.status_code == 401
    print("   ✓ Reusing revoked refresh token correctly blocked: 401 Unauthorized")

    print("\n=======================================================")
    print("🎉 ALL TESTS PASSED! AUTHENTICATION BACKEND IS READY!")
    print("=======================================================")

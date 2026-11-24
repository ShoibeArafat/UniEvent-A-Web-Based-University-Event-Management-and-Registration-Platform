"""
Automated verification test suite for Part 3: Event Ownership & Role-Based Access Control (RBAC).
Tests:
1. Unauthenticated event creation is rejected with 401 Unauthorized.
2. Authenticated user creates an event with creator_id recorded.
3. Creator can update their own event.
4. Non-creator user is forbidden (403 Forbidden) from updating another user's event.
5. Non-creator user is forbidden (403 Forbidden) from deleting another user's event.
6. Admin user can update any event (Admin bypass).
7. Admin user can delete any event (Admin bypass).
8. Unauthenticated public users can still browse events (GET /api/events).
"""
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from main import app
from models import seed_initial_events

def run_rbac_tests():
    print("=" * 60)
    print("UniEvent - Part 3: Event Ownership & RBAC Verification Suite")
    print("=" * 60)

    # 1. Initialize DB and seed demo users
    print("\n1. Seeding initial users and events...")
    seed_initial_events()

    with TestClient(app) as client:
        # 2. Login as Demo Admin and Demo Student
        print("\n2. Logging in as Admin and Student...")
        admin_res = client.post("/api/auth/login", json={"email": "admin1@unievent.edu", "password": "Admin@12345"})
        assert admin_res.status_code == 200, f"Admin login failed: {admin_res.text}"
        admin_token = admin_res.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        print("   ✓ Admin logged in")

        student_res = client.post("/api/auth/login", json={"email": "student@unievent.edu", "password": "User@12345"})
        assert student_res.status_code == 200, f"Student login failed: {student_res.text}"
        student_token = student_res.json()["access_token"]
        student_headers = {"Authorization": f"Bearer {student_token}"}
        student_id = student_res.json()["user"]["id"]
        print(f"   ✓ Student logged in (User ID: {student_id})")

        organizer_res = client.post("/api/auth/login", json={"email": "organizer@unievent.edu", "password": "User@12345"})
        assert organizer_res.status_code == 200, f"Organizer login failed: {organizer_res.text}"
        organizer_token = organizer_res.json()["access_token"]
        organizer_headers = {"Authorization": f"Bearer {organizer_token}"}
        print("   ✓ Organizer logged in (User ID: different user)")

        # 3. Test unauthenticated event creation rejection
        print("\n3. Testing unauthenticated event creation rejection...")
        event_payload = {
            "title": "Robotics Coding Marathon 2026",
            "description": "24-hour hands-on robotics marathon for student teams.",
            "location": "Robotics Innovation Lab 101",
            "event_date": "2026-12-15",
            "organizer": "Robotics Club",
            "category": "Competition",
            "capacity": 50,
            "status": "Upcoming"
        }
        unauth_res = client.post("/api/events", json=event_payload)
        assert unauth_res.status_code == 401, f"Expected 401 for unauth event create, got: {unauth_res.status_code}"
        print("   ✓ Unauthenticated event creation blocked with 401 Unauthorized")

        # 4. Student creates event
        print("\n4. Testing event creation by authenticated Student...")
        create_res = client.post("/api/events", json=event_payload, headers=student_headers)
        assert create_res.status_code == 201, f"Student event creation failed: {create_res.text}"
        created_event = create_res.json()
        event_id = created_event["id"]
        assert created_event["creator_id"] == student_id, f"Expected creator_id={student_id}, got: {created_event['creator_id']}"
        print(f"   ✓ Event created with ID {event_id} and creator_id={created_event['creator_id']}")

        # 5. Creator updates their own event
        print("\n5. Testing creator updating their own event...")
        update_payload = {"title": "Robotics Coding Marathon 2026 - Extended Edition", "capacity": 75}
        owner_update_res = client.put(f"/api/events/{event_id}", json=update_payload, headers=student_headers)
        assert owner_update_res.status_code == 200, f"Owner update failed: {owner_update_res.text}"
        assert owner_update_res.json()["capacity"] == 75
        print("   ✓ Event creator successfully updated their own event")

        # 6. Non-creator (Organizer) tries to update Student's event -> 403 Forbidden
        print("\n6. Testing non-owner (Organizer) update rejection...")
        non_owner_update_res = client.put(f"/api/events/{event_id}", json={"title": "Hacked Title"}, headers=organizer_headers)
        assert non_owner_update_res.status_code == 403, f"Expected 403 Forbidden, got: {non_owner_update_res.status_code}"
        print(f"   ✓ Non-owner modification blocked with 403 Forbidden: {non_owner_update_res.json()['detail']}")

        # 7. Non-creator (Organizer) tries to delete Student's event -> 403 Forbidden
        print("\n7. Testing non-owner (Organizer) delete rejection...")
        non_owner_del_res = client.delete(f"/api/events/{event_id}", headers=organizer_headers)
        assert non_owner_del_res.status_code == 403, f"Expected 403 Forbidden, got: {non_owner_del_res.status_code}"
        print(f"   ✓ Non-owner deletion blocked with 403 Forbidden: {non_owner_del_res.json()['detail']}")

        # 8. Admin updates Student's event -> 200 OK (Admin bypass)
        print("\n8. Testing Admin update bypass on another user's event...")
        admin_update_res = client.put(f"/api/events/{event_id}", json={"description": "Admin approved and verified description."}, headers=admin_headers)
        assert admin_update_res.status_code == 200, f"Admin update failed: {admin_update_res.text}"
        assert "Admin approved" in admin_update_res.json()["description"]
        print("   ✓ Admin successfully updated event (Admin bypass verified)")

        # 9. Admin deletes Student's event -> 200 OK (Admin bypass)
        print("\n9. Testing Admin delete bypass on another user's event...")
        admin_del_res = client.delete(f"/api/events/{event_id}", headers=admin_headers)
        assert admin_del_res.status_code == 200, f"Admin delete failed: {admin_del_res.text}"
        print("   ✓ Admin successfully deleted event (Admin bypass verified)")

        # 10. Public browsing remains accessible
        print("\n10. Testing public GET /api/events...")
        browse_res = client.get("/api/events")
        assert browse_res.status_code == 200
        print(f"   ✓ Public browsing returned {len(browse_res.json())} events with 200 OK")

    print("\n" + "=" * 60)
    print("🎉 ALL 10 RBAC TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_rbac_tests()

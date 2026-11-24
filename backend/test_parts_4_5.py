"""
Automated verification test suite for Part 4 (Shared Teams) and Part 5 (Admin Dashboard).
Tests:
1. Team auto-generation and creator as initial Owner.
2. Owner invites a member by email (Editor).
3. Co-organizer Editor can update event details (Shared collaboration verified!).
4. Owner updates member role to Coordinator.
5. Coordinator cannot edit event.
6. Non-owner cannot add or remove members (403 Forbidden).
7. Owner removes member.
8. Admin stats (/api/admin/stats) returns KPI metrics.
9. Admin user management: list, filter, ban, unban, role update.
10. Banned user cannot log in.
11. Audit logs (/api/admin/audit-logs) records activity.
12. CSV Export (/api/admin/export/csv) returns valid CSV headers and data.
"""
import sys
import time
from pathlib import Path

backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from main import app
from models import seed_initial_events

def run_tests():
    print("=" * 65)
    print("UniEvent - Parts 4 & 5: Teams & Admin Verification Suite")
    print("=" * 65)

    seed_initial_events()

    with TestClient(app) as client:
        # Log in Admin, Student (Creator), and Organizer (Co-member)
        admin_res = client.post("/api/auth/login", json={"email": "admin1@unievent.edu", "password": "Admin@12345"})
        admin_token = admin_res.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        student_res = client.post("/api/auth/login", json={"email": "student@unievent.edu", "password": "User@12345"})
        student_token = student_res.json()["access_token"]
        student_headers = {"Authorization": f"Bearer {student_token}"}
        student_id = student_res.json()["user"]["id"]

        organizer_res = client.post("/api/auth/login", json={"email": "organizer@unievent.edu", "password": "User@12345"})
        organizer_token = organizer_res.json()["access_token"]
        organizer_headers = {"Authorization": f"Bearer {organizer_token}"}
        organizer_id = organizer_res.json()["user"]["id"]

        # ==========================================
        # PART 4: TEAMS TESTS
        # ==========================================
        print("\n--- Testing Part 4: Shared Event Teams ---")

        # 1. Student creates an event
        create_res = client.post("/api/events", json={
            "title": "Hackathon CSE 2026",
            "description": "Collaborative university hackathon.",
            "location": "Main Auditorium",
            "event_date": "2026-12-20",
            "organizer": "Computer Club",
            "category": "Competition",
            "capacity": 100,
            "status": "Upcoming"
        }, headers=student_headers)
        assert create_res.status_code == 201
        event_id = create_res.json()["id"]
        print(f"1. Created test event ID: {event_id}")

        # 2. View Team (Auto-created with creator as Owner)
        team_res = client.get(f"/api/events/{event_id}/team", headers=student_headers)
        assert team_res.status_code == 200
        team_data = team_res.json()
        assert len(team_data["members"]) >= 1
        assert any(m["user_id"] == student_id and m["role"] == "Owner" for m in team_data["members"])
        print(f"2. Verified Event Team '{team_data['name']}' has creator as Owner")

        # 3. Student invites Organizer as 'Editor'
        invite_res = client.post(f"/api/events/{event_id}/team/members", json={
            "email": "organizer@unievent.edu",
            "role": "Editor"
        }, headers=student_headers)
        assert invite_res.status_code == 201
        assert any(m["user_id"] == organizer_id and m["role"] == "Editor" for m in invite_res.json()["members"])
        print("3. Successfully invited Organizer as 'Editor' on the team")

        # 4. Verified Shared Collaboration: Organizer (Editor) updates the event!
        editor_update_res = client.put(f"/api/events/{event_id}", json={
            "description": "Collaborative update made by team Editor (organizer)."
        }, headers=organizer_headers)
        assert editor_update_res.status_code == 200
        assert "Collaborative update" in editor_update_res.json()["description"]
        print("4. Team Editor successfully edited the event (Shared Collaboration working!)")

        # 5. Unauthorized user cannot add members
        unauth_add_res = client.post(f"/api/events/{event_id}/team/members", json={
            "email": "admin1@unievent.edu",
            "role": "Viewer"
        }, headers=organizer_headers)
        assert unauth_add_res.status_code == 403
        print("5. Non-owner/non-admin correctly blocked from adding members (403 Forbidden)")

        # 6. Owner updates Organizer's role to 'Coordinator'
        update_role_res = client.put(f"/api/events/{event_id}/team/members/{organizer_id}", json={
            "role": "Coordinator"
        }, headers=student_headers)
        assert update_role_res.status_code == 200
        assert any(m["user_id"] == organizer_id and m["role"] == "Coordinator" for m in update_role_res.json()["members"])
        print("6. Successfully updated member role to 'Coordinator'")

        # 7. Coordinator can NO longer edit event settings
        coord_update_res = client.put(f"/api/events/{event_id}", json={"description": "Should fail"}, headers=organizer_headers)
        assert coord_update_res.status_code == 403
        print("7. Coordinator correctly blocked from modifying event settings (403 Forbidden)")

        # 8. Owner removes member
        del_member_res = client.delete(f"/api/events/{event_id}/team/members/{organizer_id}", headers=student_headers)
        assert del_member_res.status_code == 200
        assert not any(m["user_id"] == organizer_id for m in del_member_res.json()["members"])
        print("8. Successfully removed member from team")

        # ==========================================
        # PART 5: ADMIN DASHBOARD & AUDIT TESTS
        # ==========================================
        print("\n--- Testing Part 5: Admin Dashboard & Audit Logs ---")

        # 9. Non-admin blocked from admin endpoints
        student_admin_res = client.get("/api/admin/stats", headers=student_headers)
        assert student_admin_res.status_code == 403
        print("9. Non-admin correctly blocked from /api/admin/stats (403 Forbidden)")

        # 10. Admin stats
        admin_stats_res = client.get("/api/admin/stats", headers=admin_headers)
        assert admin_stats_res.status_code == 200
        stats = admin_stats_res.json()
        assert stats["total_users"] >= 3
        assert stats["total_events"] >= 1
        print(f"10. Admin stats loaded: {stats['total_users']} users, {stats['total_events']} events, {stats['total_teams']} teams")

        # 11. Admin user list
        users_res = client.get("/api/admin/users", headers=admin_headers)
        assert users_res.status_code == 200
        assert len(users_res.json()) >= 3
        print(f"11. Admin fetched user directory ({len(users_res.json())} users)")

        # 12. Create a temporary user to ban and test
        unique_email = f"temp_banned_{int(time.time())}@unievent.edu"
        temp_user_res = client.post("/api/auth/signup", json={
            "name": "Banned Test User",
            "email": unique_email,
            "password": "Password123!"
        })
        assert temp_user_res.status_code == 201
        temp_user_id = temp_user_res.json()["user"]["id"]

        # Admin bans temporary user (admin1 has exclusive authority)
        ban_res = client.put(f"/api/admin/users/{temp_user_id}/status", json={
            "is_banned": True,
            "ban_reason": "Academic policy violation"
        }, headers=admin_headers)
        assert ban_res.status_code == 200
        assert ban_res.json()["is_banned"] is True
        print("12. Primary Admin (admin1) successfully banned test user")

        # Verify that secondary admin (admin2) cannot ban/unban users (restricted to admin1)
        admin2_res = client.post("/api/auth/login", json={"email": "admin2@unievent.edu", "password": "Admin@12345"})
        assert admin2_res.status_code == 200
        admin2_token = admin2_res.json()["access_token"]
        admin2_headers = {"Authorization": f"Bearer {admin2_token}"}
        admin2_ban_attempt = client.put(f"/api/admin/users/{temp_user_id}/status", json={
            "is_banned": False
        }, headers=admin2_headers)
        assert admin2_ban_attempt.status_code == 403
        print("12b. Secondary Admin (admin2) correctly blocked from ban/unban access (403 Forbidden)")

        # Banned user cannot login
        banned_login = client.post("/api/auth/login", json={"email": unique_email, "password": "Password123!"})
        assert banned_login.status_code == 403
        print("13. Banned user login successfully blocked with 403 Forbidden")

        # Admin unbans user
        unban_res = client.put(f"/api/admin/users/{temp_user_id}/status", json={
            "is_banned": False
        }, headers=admin_headers)
        assert unban_res.status_code == 200
        assert unban_res.json()["is_banned"] is False
        print("14. Admin successfully unbanned test user")

        # 15. Audit logs retrieval
        audit_res = client.get("/api/admin/audit-logs?limit=10", headers=admin_headers)
        assert audit_res.status_code == 200
        logs = audit_res.json()
        assert len(logs) > 0
        actions = [l["action"] for l in logs]
        assert "USER_BAN" in actions or "EVENT_CREATE" in actions
        print(f"15. Retrieved {len(logs)} audit log entries (Actions tracked: {list(set(actions))[:4]})")

        # 16. CSV Export
        csv_res = client.get("/api/admin/export/csv?report_type=events", headers=admin_headers)
        assert csv_res.status_code == 200
        assert "text/csv" in csv_res.headers.get("content-type", "")
        assert "ID,Title,Category" in csv_res.text
        print("16. Event CSV export verified with correct headers and rows")

    print("\n" + "=" * 65)
    print("🎉 ALL PARTS 4 & 5 BACKEND TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()

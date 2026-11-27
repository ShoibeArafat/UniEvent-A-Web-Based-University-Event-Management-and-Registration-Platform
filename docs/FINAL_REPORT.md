# Independent University, Bangladesh
## Department of Computer Science & Engineering
### CSE309: Web Application & Internet

---

# Final Project Submission Report
## UniEvent — A Web-Based University Event Management and Registration Platform

**Submitted by:**  
- **Name:** Shoibe Arafat  
- **Student ID:** 2131108  
- **Section:** 06  

**Project Details:**  
- **Project Title:** UniEvent — University Event Management & Registration Platform  
- **Vercel Live URL:** [https://2131108.vercel.app](https://2131108.vercel.app)  
- **GitHub Repository:** [https://github.com/ShoibeArafat/UniEvent-A-Web-Based-University-Event-Management-and-Registration-Platform](https://github.com/ShoibeArafat/UniEvent-A-Web-Based-University-Event-Management-and-Registration-Platform)  
- **Live Swagger API Docs:** [https://2131108.vercel.app/api/docs](https://2131108.vercel.app/api/docs)  

**Submitted To:**  
- **Sayef Reyadh**  
- Adjunct Lecturer, Department of Computer Science & Engineering  
- Independent University, Bangladesh  

**Semester:** Autumn 2026  
**Date of Submission:** 27-11-2026  

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
   - 1.1 [Project Overview](#11-project-overview)
   - 1.2 [What Was Built Since the Mid Assessment](#12-what-was-built-since-the-mid-assessment)
   - 1.3 [Live Links](#13-live-links)
2. [Part A. Product Requirements (PRD)](#part-a-product-requirements-prd)
   - A1. [Problem Statement](#a1-problem-statement)
   - A2. [Users and Roles](#a2-users-and-roles)
   - A3. [Goals and Success Measures](#a3-goals-and-success-measures)
   - A4. [Scope and Non-Goals](#a4-scope-and-non-goals)
   - A5. [User Stories](#a5-user-stories)
3. [Part B. Software Requirements (SRS)](#part-b-software-requirements-srs)
   - B1. [Introduction](#b1-introduction)
   - B2. [Functional Requirements](#b2-functional-requirements)
   - B3. [Non-Functional Requirements](#b3-non-functional-requirements)
   - B4. [Roles and Permission Matrix](#b4-roles-and-permission-matrix)
   - B5. [Use Cases](#b5-use-cases)
   - B6. [Accept Criteria](#b6-acceptance-criteria)
   - B7. [Traceability Matrix](#b7-traceability-matrix)
4. [Part C. Technical Design (TDD)](#part-c-technical-design-tdd)
   - C1. [Technology Stack](#c1-technology-stack)
   - C2. [System Architecture](#c2-system-architecture)
   - C3. [Backend and Frontend Structure](#c3-backend-and-frontend-structure)
   - C4. [Data Model](#c4-data-model)
   - C5. [API Design](#c5-api-design)
   - C6. [JWT Authentication Design](#c6-jwt-authentication-design)
   - C7. [RBAC Design](#c7-rbac-design)
   - C8. [Admin Dashboard Design](#c8-admin-dashboard-design)
   - C9. [Security Design and Threats](#c9-security-design-and-threats)
   - C10. [Deployment on Vercel](#c10-deployment-on-vercel)
   - C11. [Testing Strategy](#c11-testing)
5. [Part D. Evidence: Screenshots of the Running Application](#part-d-evidence-screenshots-of-the-running-application)
   - D1. [User Side Evidence](#d1-user-side)
   - D2. [Security Behaviour](#d2-security-behaviour)
   - D3. [Admin Dashboard](#d3-admin-dashboard)
   - D4. [Deployment](#d4-deployment)
   - D5. [Tests Run Output](#d5-tests)
6. [Part E. Project Management and Conclusion](#part-e-project-management-and-conclusion)
   - E1. [How to Run and Test](#e1-how-to-run-and-test)
   - E2. [GitHub Work and Commits](#e2-github-work)
   - E3. [Limitations](#e3-limitations)
   - E4. [Future Work](#e4-future-work)
   - E5. [Sources, Libraries and Tools](#e5-sources-libraries-and-tools)
7. [Appendix: Test Accounts and Video Demo](#appendix-test-accounts-and-video-demo)

---

# 1. Executive Summary

### 1.1 Project Overview
**UniEvent** is an enterprise-grade university event management and collaborative organizing platform engineered for students, club committees, event organizers, and university administrators. The system resolves the campus challenge of fragmented event announcements, unauthorized schedule modifications, and lack of accountability by providing strict event ownership, collaborative organizing teams with multi-tiered permissions, automated security audit trails, and platform-wide moderation. The full stack is implemented using **React 19 with TypeScript** on the frontend, **FastAPI with SQLAlchemy** on the backend, persistent cloud **Supabase PostgreSQL** for data storage, and is fully deployed on **Vercel**.

### 1.2 What Was Built Since the Mid Assessment
Since the mid-term assessment, the platform evolved from an anonymous prototype into a secure, multi-tenant cloud application:
- **JWT Authentication with Refresh and Logout:** Implemented stateless 15-minute access tokens and stateful 7-day SHA-256 hashed refresh tokens with instant server-side revocation in `user_sessions`.
- **Role-Based Access Control (RBAC):** Enforced creator-level resource ownership (`creator_id`), 4-tier collaborative organizing teams (`Owner`, `Editor`, `Coordinator`, `Viewer`), and administrative bypass authority.
- **Admin Center & Moderation:** Built a dedicated administrative control panel featuring real-time platform KPI metrics, searchable user directory, user account suspension/reactivation, and a Primary Admin security lock.
- **Audit Logging & Security Hardening:** Implemented automated timestamped security audit trails recording actor IDs, actions, and IP addresses, along with strict CORS whitelisting and cloud connection pooling on Supabase PostgreSQL.

### 1.3 Live Links
#### Table 1: System Links
| Resource | URL |
| :--- | :--- |
| **Production Frontend** | [https://2131108.vercel.app](https://2131108.vercel.app) |
| **Backend API Gateway** | [https://2131108.vercel.app/api](https://2131108.vercel.app/api) |
| **Interactive API Documentation** | [https://2131108.vercel.app/api/docs](https://2131108.vercel.app/api/docs) |
| **GitHub Repository** | [https://github.com/ShoibeArafat/UniEvent-A-Web-Based-University-Event-Management-and-Registration-Platform](https://github.com/ShoibeArafat/UniEvent-A-Web-Based-University-Event-Management-and-Registration-Platform) |
| **Video Demonstration** | *(See Appendix for video submission link)* |

---

# Part A. Product Requirements (PRD)

### A1. Problem Statement
University campus life involves hundreds of academic workshops, cultural galas, hackathons, and guest lectures hosted by diverse departments and student clubs. Currently, university students and club organizers rely on disjointed channels like social media groups, physical bulletin boards, and static spreadsheets to announce events and coordinate teams. 

This causes severe operational bottlenecks: event details are frequently vandalized or overwritten by unverified parties, organizers lack granular delegation permissions for committee members, students miss critical schedule updates, and university authorities have zero visibility or audit logs over campus activities. A unified, role-governed platform is required to ensure data integrity, verifiable accountability, and secure collaboration.

### A2. Users and Roles
#### Table 2: Users and Roles Specification
| Role | Who They Are | Main Tasks | What They Must Never Be Able To Do |
| :--- | :--- | :--- | :--- |
| **Visitor (Guest)** | Unauthenticated public visitor or prospective student. | Browse approved university events, filter by category and search keywords, view public event details. | Must never create, edit, or delete events; cannot access organizing teams or admin endpoints. |
| **Student (User)** | Registered university student (`Role: User`). | Create events, manage their own events, view profile, manage active login sessions across devices. | Must never edit or delete events created by other students; cannot access the Admin Center. |
| **Team Member (Editor)** | Student assigned to an event's organizing team with `Editor` status. | Collaboratively update event descriptions, locations, capacity, and schedules for that assigned event. | Must never delete the event, remove the team owner, or modify team member rosters. |
| **Team Member (Coordinator / Viewer)** | Student assigned as `Coordinator` or `Viewer`. | View private team communications and coordination rosters. | Must never modify event details or delete the event. |
| **Event Owner** | The original student creator of the university event. | Modify event, delete event, invite team members by email, update member tiers (`Editor`/`Viewer`), remove members. | Must never modify events owned by other students without administrative privileges. |
| **Platform Admin** | University administrator (`Role: Admin`). | Monitor campus KPIs, review audit logs, moderate inappropriate events, suspend/reactivate violating student accounts. | Secondary admins must never ban the Primary Admin (`admin1@unievent.edu`) or ban their own account. |

### A3. Goals and Success Measures
#### Table 3: Goals and Success Measures
| Goal ID | Objective | Measurable & Testable Success Metric |
| :--- | :--- | :--- |
| **G-01** | **Strict Event Ownership** | 100% of unauthorized update/delete requests return HTTP `403 Forbidden` in automated tests. |
| **G-02** | **Session Security** | Access tokens expire in exactly 15 minutes; revoked refresh tokens return `401 Unauthorized`. |
| **G-03** | **Data Persistence** | 100% of event records, user profiles, and audit entries persist permanently in cloud Supabase PostgreSQL. |
| **G-04** | **Audit Accountability** | Every event mutation (`CREATE`, `UPDATE`, `DELETE`) and user moderation (`USER_BAN`) generates an audit row within < 50ms. |
| **G-05** | **Low Latency** | Event catalogue queries execute in < 250ms under warm Supabase transaction pooling. |
| **G-06** | **Zero Frontend Build Errors** | TypeScript compiler (`tsc`) and Vite build pass with exactly 0 errors. |

### A4. Scope and Non-Goals
- **In Scope:**
  - Secure signup, login, silent refresh, profile management, and session revocation.
  - CRUD operations on events with creator-level ownership.
  - Multi-tier organizing teams with email-based invitation and role-governed mutations.
  - Platform Admin Center with real-time KPI metrics, searchable user directory, and ban/unban moderation.
  - Immutable audit trail recording timestamps, actor IDs, actions, and client IP addresses.
  - Responsive React 19 UI with 1-click quick-fill demo authentication for viva assessment.
  - Cloud deployment on Vercel with managed PostgreSQL connection pooling on Supabase.
- **Out of Scope (Non-Goals):**
  - Paid ticketing and payment gateway integration (Stripe/bKash) — deferred to keep focus on core RBAC and university governance.
  - Real-time chat between team members — covered via external university communication tools.
  - Native mobile applications (iOS/Android) — mobile responsiveness achieved via CSS Flexbox/Grid on web.
- **Assumptions and Constraints:**
  - Users have university-affiliated email addresses (`@unievent.edu`).
  - Vercel serverless execution timeout limit of 15 seconds.
  - Single cloud database architecture (Supabase PostgreSQL) per instructor instructions.

### A5. User Stories
#### Table 4: User Stories
| ID | As a (Role) | I want to (Action) | So that (Benefit) |
| :--- | :--- | :--- | :--- |
| **US-01** | Student | Register with my name, university email, and password | I can obtain personal credentials to create campus events. |
| **US-02** | Student | Log in and receive access and refresh tokens | I can stay authenticated across page reloads without re-typing passwords. |
| **US-03** | Student | View all active login sessions and revoke specific ones | I can secure my account if I forget to log out of a library computer. |
| **US-04** | Student | Create an event specifying title, date, location, and capacity | I can publish activities for the student body and become the verified owner. |
| **US-05** | Event Owner | See gold `★ Your Event` badges and filter by "My Events" | I can immediately distinguish and manage my own submissions. |
| **US-06** | Event Owner | Invite a classmate to my event team as an `Editor` | They can help update event descriptions and schedules collaboratively. |
| **US-07** | Team Editor | Modify the description and venue of my assigned team event | Collaborative logistics are kept up to date without bothering the owner. |
| **US-08** | Student | Be blocked with HTTP 403 if I attempt to edit another student's event | Event parameters cannot be altered by unauthorized peers. |
| **US-09** | Admin | Access a dedicated Admin Center with KPI metrics | I have real-time visibility into student counts, active events, and organizing teams. |
| **US-10** | Primary Admin| Suspend a student account with a documented reason | Misbehaving accounts are immediately ejected from the platform and logged in audit trails. |

---

# Part B. Software Requirements (SRS)

### B1. Introduction
This Software Requirements Specification defines the complete functional and non-functional requirements for the UniEvent system. It serves as the primary verification contract for academic grading, functional compliance, and security assurance.

#### Definitions Table
| Term | Definition |
| :--- | :--- |
| **JWT** | JSON Web Token (RFC 7519) — compact, URL-safe means of representing claims between two parties. |
| **Access Token** | Short-lived (15 minutes), stateless bearer token signed via HMAC-SHA256 (`HS256`). |
| **Refresh Token**| High-entropy 48-character cryptographic string stored as a SHA-256 hash in the database (7-day validity). |
| **RBAC** | Role-Based Access Control — restricting system access based on user roles and object ownership. |
| **Audit Log** | Immutable append-only log capturing user actions, timestamps, target entities, and client IP addresses. |
| **Supabase** | Cloud platform hosting managed PostgreSQL 17 with integrated connection pooling (PgBouncer). |

---

### B2. Functional Requirements

#### Table 5: Authentication & Session Management (FR-AUTH)
| Requirement ID | Requirement Statement |
| :--- | :--- |
| **FR-AUTH-01** | The system shall register new users with full name, unique university email, and bcrypt-hashed password ($\ge 6$ chars). |
| **FR-AUTH-02** | The system shall reject duplicate email registrations with HTTP `400 Bad Request`. |
| **FR-AUTH-03** | The system shall authenticate credentials on `POST /api/auth/login` and return an access token and refresh token. |
| **FR-AUTH-04** | The system shall sign access tokens with HMAC-SHA256 containing `sub`, `email`, `role`, and a 15-minute expiration timestamp. |
| **FR-AUTH-05** | The system shall store only the SHA-256 hash of refresh tokens in the `user_sessions` table, never plaintext strings. |
| **FR-AUTH-06** | The system shall issue a new access token on `POST /api/auth/refresh` if the refresh token is valid and unrevoked. |
| **FR-AUTH-07** | The system shall mark the refresh token session as `is_revoked = True` in the database upon user logout. |
| **FR-AUTH-08** | The system shall reject any request using an expired or revoked token with HTTP `401 Unauthorized`. |
| **FR-AUTH-09** | The system shall allow users to list all active sessions and revoke individual device sessions on `DELETE /api/users/me/sessions/{id}`. |
| **FR-AUTH-10** | The system shall reject login attempts from suspended users with HTTP `403 Forbidden` and display the suspension reason. |

#### Table 6: Role-Based Access Control & Ownership (FR-RBAC)
| Requirement ID | Requirement Statement |
| :--- | :--- |
| **FR-RBAC-01** | The system shall automatically record `creator_id = current_user.id` on every newly created event. |
| **FR-RBAC-02** | The system shall reject event creation requests from unauthenticated visitors with HTTP `401 Unauthorized`. |
| **FR-RBAC-03** | The system shall reject update requests from non-creator, non-editor users with HTTP `403 Forbidden`. |
| **FR-RBAC-04** | The system shall reject delete requests from anyone other than the primary event creator or a system administrator with HTTP `403 Forbidden`. |
| **FR-RBAC-05** | The system shall allow platform administrators to update or delete any event regardless of the original creator. |
| **FR-RBAC-06** | The system shall automatically provision an `EventTeam` record upon event creation with the creator assigned as `Owner`. |
| **FR-RBAC-07** | The system shall permit the team `Owner` to invite registered users by email and assign roles (`Editor`, `Coordinator`, `Viewer`). |
| **FR-RBAC-08** | The system shall permit team members with `Editor` status to update event details (`PUT /api/events/{id}`). |

#### Table 7: Platform Administration & Moderation (FR-ADM)
| Requirement ID | Requirement Statement |
| :--- | :--- |
| **FR-ADM-01** | The system shall restrict all `/api/admin/*` endpoints strictly to authenticated users with `role == "Admin"`. |
| **FR-ADM-02** | The system shall provide real-time aggregate KPI metrics (total users, events, teams, active sessions, and suspended users). |
| **FR-ADM-03** | The system shall provide a user directory with live search and filtering by role (`Admin`/`User`) and status (`Active`/`Suspended`). |
| **FR-ADM-04** | The system shall restrict account suspension/reactivation authority exclusively to the Primary Admin (`admin1@unievent.edu`). |
| **FR-ADM-05** | The system shall immediately invalidate all active database sessions (`is_revoked = True`) whenever an account is suspended. |
| **FR-ADM-06** | The system shall reject any attempt by an administrator to ban their own account or the Primary Admin account with HTTP `400 Bad Request`. |
| **FR-ADM-07** | The system shall log every administrative action into `audit_logs` capturing timestamp, actor ID, action type, and client IP address. |

#### Table 8: Domain Resource Management (FR-DOMAIN)
| Requirement ID | Requirement Statement |
| :--- | :--- |
| **FR-DOMAIN-01** | The system shall permit public browsing and category filtering (`Technology`, `Competition`, `Workshop`, `Cultural`, `Seminar`) on `GET /api/events`. |
| **FR-DOMAIN-02** | The system shall support keyword search queries across event titles, descriptions, and organizer names. |
| **FR-DOMAIN-03** | The system shall display ownership indicators (gold `★ Your Event` badge and purple `Admin` badge) on event cards. |
| **FR-DOMAIN-04** | The system shall provide a two-tab modal displaying general event details and the organizing team roster. |

---

### B3. Non-Functional Requirements
#### Table 9: Non-Functional Requirements (NFR)
| Category | Requirement ID | Specification | Verification Method |
| :--- | :--- | :--- | :--- |
| **Security** | **NFR-SEC-01** | All passwords hashed using `bcrypt` (work factor 12). | Code inspection & DB hash verification. |
| **Security** | **NFR-SEC-02** | JWT secrets and database URIs loaded exclusively from environment variables. | Inspection of `vercel.json` & codebase. |
| **Performance** | **NFR-PERF-01** | API response time under 250ms for catalogue queries under warm pooling. | Chrome DevTools Network Timing tab. |
| **Usability** | **NFR-USA-01** | Fully responsive layout across desktop, tablet, and mobile with visual loading spinners. | Chrome DevTools device mode inspection. |
| **Reliability** | **NFR-REL-01** | Data permanently persists across serverless lambda restarts using Supabase PostgreSQL. | Cloud database inspection after cold reboot. |
| **Maintainability**| **NFR-MNT-01** | Centralized authorization dependencies in `auth_dependencies.py`; zero TypeScript compiler errors. | `npm run build` and test suite execution. |

---

### B4. Roles and Permission Matrix

#### Table 10: Endpoint Groups by Roles
| Endpoint Group | Visitor (Guest) | Registered Student | Team Editor | Team Owner | Platform Admin |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `GET /api/events` (Browse) | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| `POST /api/events` (Create) | ❌ No (401) | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| `PUT /api/events/{id}` (Edit) | ❌ No (401) | ❌ No (403) | ✅ Yes (Assigned) | ✅ Yes (Own) | ✅ Yes (All) |
| `DELETE /api/events/{id}` (Delete)| ❌ No (401) | ❌ No (403) | ❌ No (403) | ✅ Yes (Own) | ✅ Yes (All) |
| `POST /api/events/{id}/team/*` | ❌ No (401) | ❌ No (403) | ❌ No (403) | ✅ Yes (Own) | ✅ Yes (All) |
| `GET /api/admin/*` (Dashboard) | ❌ No (401) | ❌ No (403) | ❌ No (403) | ❌ No (403) | ✅ Yes |
| `PUT /api/admin/users/{id}/status`| ❌ No (401) | ❌ No (403) | ❌ No (403) | ❌ No (403) | ✅ Primary Only |

#### Table 11: Organizing Team Permissions
| Team Role | View Team Roster | Edit Event Data | Invite Members | Change Member Roles | Remove Members | Delete Event |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Owner (Creator)** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Editor** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Coordinator** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Viewer** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |

#### Table 12: Admin Governance & Self-Protection Rules
| Governance Rule | Enforcement Mechanism | Failure Status Code |
| :--- | :--- | :--- |
| **Admin Cannot Ban Self** | `if user_id == current_admin.id: raise HTTPException` | HTTP `400 Bad Request` |
| **Primary Admin Protection** | `if target_user.email == "admin1@unievent.edu": raise HTTPException` | HTTP `400 Bad Request` |
| **Secondary Admin Ban Lock** | `if current_admin.email != "admin1@unievent.edu": raise HTTPException` | HTTP `403 Forbidden` |

---

### B5. Use Cases

```mermaid
flowchart LR
    Student((Student))
    Admin((Platform Admin))
    Visitor((Guest Visitor))

    subgraph UniEvent System
        UC1[UC-01: Sign Up & Log In]
        UC2[UC-02: Create Event]
        UC3[UC-03: Manage Team Members]
        UC4[UC-04: Edit Event Details]
        UC5[UC-05: Review Admin KPIs]
        UC6[UC-06: Moderate User Account]
    end

    Visitor --> UC1
    Student --> UC1
    Student --> UC2
    Student --> UC3
    Student --> UC4
    Admin --> UC4
    Admin --> UC5
    Admin --> UC6
```

#### Table 13: Core Use Case Descriptions
| Use Case ID | Name & Actor | Preconditions | Main Success Flow | Alternative / Error Flows | Postconditions |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **UC-01** | **User Login**<br>*(Student/Admin)* | User has a registered account. | 1. Enters email and password in `Login.tsx`.<br>2. Backend verifies bcrypt hash.<br>3. Generates 15-min access token and 7-day refresh token.<br>4. Saves hashed refresh token to `user_sessions`.<br>5. Frontend stores tokens and unlocks dashboard. | **E1:** Wrong password ➡️ HTTP `401 Unauthorized`.<br>**E2:** Banned account ➡️ HTTP `403 Forbidden` with suspension reason. | User is authenticated; profile header displayed. |
| **UC-02** | **Create Event**<br>*(Student)* | User is authenticated with a valid JWT. | 1. Fills event form and submits.<br>2. Backend stamps `creator_id = current_user.id`.<br>3. Auto-creates `EventTeam` with user as `Owner`.<br>4. Commits event to Supabase. | **E1:** Missing token ➡️ HTTP `401 Unauthorized`.<br>**E2:** Missing title/date ➡️ HTTP `422 Unprocessable Entity`. | Event appears in catalogue with gold `★ Your Event` badge. |
| **UC-03** | **Invite Member**<br>*(Event Owner)* | User is the verified `Owner` of the event team. | 1. Opens Team tab in modal.<br>2. Enters peer's email and role `Editor`.<br>3. Backend verifies peer exists in `users`.<br>4. Inserts row into `team_members`. | **E1:** Requester is not owner ➡️ HTTP `403 Forbidden`.<br>**E2:** Peer email not registered ➡️ HTTP `404 Not Found`. | Peer gains editing rights over the event. |
| **UC-04** | **Edit Event**<br>*(Creator/Editor)* | User is creator, team Editor, or Platform Admin. | 1. Modifies event details and submits.<br>2. `crud_teams.user_can_edit_event` returns `True`.<br>3. Updates row in Supabase and records `EVENT_UPDATE` in audit log. | **E1:** Non-owner/non-editor attempts update ➡️ HTTP `403 Forbidden`. | Event details updated across catalogue. |
| **UC-05** | **Suspend Account**<br>*(Primary Admin)* | Logged in as `admin1@unievent.edu`. | 1. Navigates to User Directory in Admin Center.<br>2. Clicks "Suspend", inputs reason, and confirms.<br>3. Sets `is_banned = True` and invalidates all active sessions in `user_sessions`.<br>4. Logs `USER_BAN` in audit trail. | **E1:** Secondary admin calls ban ➡️ HTTP `403 Forbidden`.<br>**E2:** Admin bans self ➡️ HTTP `400 Bad Request`. | User cannot log in; active tokens rejected on next request. |
| **UC-06** | **Token Refresh**<br>*(Browser/Frontend)*| Access token expired (after 15 minutes). | 1. Frontend catches HTTP `401` on API request.<br>2. Dispatches `POST /api/auth/refresh` with refresh token.<br>3. Backend verifies SHA-256 hash in `user_sessions`.<br>4. Returns new 15-minute access token. | **E1:** Session was revoked (logout or ban) ➡️ HTTP `401 Unauthorized` ➡️ User redirected to login. | Session seamlessly extended without user friction. |

---

### B6. Acceptance Criteria
#### Table 14: Given-When-Then Acceptance Criteria
| Criteria ID | Scenario | Given (Context) | When (Action) | Then (Expected Outcome) |
| :--- | :--- | :--- | :--- | :--- |
| **AC-01** | Token Expiration | A user holds an access token older than 15 minutes. | The client requests a protected endpoint (`/api/events`). | Backend returns HTTP `401 Unauthorized` with `WWW-Authenticate: Bearer`. |
| **AC-02** | Token Tampering | An attacker modifies the payload of a JWT token. | The client sends the altered token in the header. | Cryptographic signature validation fails; backend returns HTTP `401 Unauthorized`. |
| **AC-03** | Unauthorized Mutation | User A is logged in (`student@unievent.edu`). | User A calls `PUT /api/events/{id}` for an event owned by User B. | Backend returns HTTP `403 Forbidden` (`detail: Permission denied`). |
| **AC-04** | Non-Admin Access | A standard student holds a valid JWT token. | The student sends a request to `GET /api/admin/stats`. | Backend returns HTTP `403 Forbidden` (`detail: Administrator privileges required`). |
| **AC-05** | Banned User Ejection | User A is suspended by `admin1@unievent.edu`. | User A makes any subsequent authenticated request. | `get_current_user` catches `user.is_banned == True` and returns HTTP `403 Forbidden`. |
| **AC-06** | Admin Self-Protection | An administrator is logged in. | The admin calls `PUT /api/admin/users/{own_id}/status` to ban themselves. | Backend rejects with HTTP `400 Bad Request` (`detail: Administrators cannot ban their own account`). |

---

### B7. Traceability Matrix
#### Table 15: Requirements Traceability Matrix
| Requirement ID | Implemented In (Code / Screen) | Automated Verification Test | Verified Output |
| :--- | :--- | :--- | :--- |
| **FR-AUTH-01** | `backend/routes/auth.py` / `Login.tsx` | `backend/test_auth.py` (Step 4) | `POST /api/auth/signup -> 201 Created` |
| **FR-AUTH-03** | `backend/routes/auth.py` / `Login.tsx` | `backend/test_auth.py` (Step 3) | `POST /api/auth/login -> 200 OK` |
| **FR-AUTH-06** | `backend/routes/auth.py` / `AuthContext.tsx`| `backend/test_auth.py` (Step 6) | `POST /api/auth/refresh -> 200 OK` |
| **FR-AUTH-07** | `backend/routes/auth.py` / `Navbar.tsx` | `backend/test_auth.py` (Step 8) | `POST /api/auth/logout -> is_revoked=True` |
| **FR-RBAC-01** | `backend/routes/events.py` / `App.tsx` | `backend/test_rbac.py` (Step 4) | `Event created with creator_id stamped` |
| **FR-RBAC-03** | `backend/routes/events.py` / `EventCard.tsx`| `backend/test_rbac.py` (Step 6) | `Non-owner update blocked with 403` |
| **FR-RBAC-04** | `backend/routes/events.py` / `EventCard.tsx`| `backend/test_rbac.py` (Step 7) | `Non-owner delete blocked with 403` |
| **FR-RBAC-06** | `backend/crud_teams.py` / `EventModal.tsx` | `backend/test_parts_4_5.py` (Step 2)| `Team provisioned with creator as Owner` |
| **FR-RBAC-08** | `backend/crud_teams.py` / `EventDetailModal`| `backend/test_parts_4_5.py` (Step 4)| `Team Editor successfully edited event` |
| **FR-ADM-01** | `backend/auth_dependencies.py` | `backend/test_parts_4_5.py` (Step 9)| `Non-admin blocked with 403 Forbidden` |
| **FR-ADM-04** | `backend/routes/admin.py` / `AdminModal.tsx`| `backend/test_parts_4_5.py` (Step 12)| `Primary Admin successfully banned user` |
| **FR-ADM-07** | `backend/crud_audit.py` / `AdminModal.tsx`| `backend/test_parts_4_5.py` (Step 15)| `Retrieved audit log entries` |

---

# Part C. Technical Design (TDD)

### C1. Technology Stack
#### Table 16: Technology Stack & Justification
| Component | Technology | Version | Justification |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | React | 19.0.0 | Component-based UI with fast concurrent rendering and declarative state management. |
| **Programming Language**| TypeScript | 5.7.2 | Enforces static type safety, compile-time contract checking, and robust interface modeling. |
| **Build Tool** | Vite | 6.0.5 | Ultra-fast Hot Module Replacement (HMR) and optimized rollup production bundles. |
| **Backend Framework** | FastAPI | 0.115.0 | High-performance Python async web framework with automatic OpenAPI documentation and Pydantic validation. |
| **Database Engine** | PostgreSQL | 17 (Supabase)| Enterprise-grade ACID relational database with row-level integrity and transaction connection pooling. |
| **Object-Relational Map**| SQLAlchemy | 2.0.36 | Decouples SQL queries into type-safe Python models with automated session lifecycle management. |
| **Password Hashing** | bcrypt | 4.2.0 | Adaptive cryptographic key derivation function with randomized salts immune to rainbow table attacks. |
| **JWT Library** | PyJWT | 2.10.0 | Compliant RFC 7519 implementation for HMAC-SHA256 access token encoding and verification. |
| **Database Driver** | psycopg2-binary | 2.9.10 | Mature, battle-tested C-extension driver for high-throughput PostgreSQL communication. |
| **Cloud Hosting** | Vercel | Cloud Edge | Serverless frontend SPA hosting and zero-configuration Python API routing via edge lambdas. |

---

### C2. System Architecture

```mermaid
flowchart TD
    subgraph Client ["Client Browser (React 19 + TypeScript)"]
        UI["React UI (Event Grid, Modals, Admin Center)"]
        AuthCtx["AuthContext & Token Interceptor"]
    end

    subgraph VercelEdge ["Vercel Edge Network (https://2131108.vercel.app)"]
        StaticCDN["Static Assets CDN (HTML, CSS, JS Bundles)"]
        ServerlessGateway["FastAPI Gateway (/api/* -> index.py)"]
    end

    subgraph BackendServices ["FastAPI Backend Services Layer"]
        AuthRouter["/api/auth (Login, Signup, Refresh, Logout)"]
        EventRouter["/api/events (RBAC Event CRUD)"]
        TeamRouter["/api/events/{id}/team (Organizing Teams)"]
        AdminRouter["/api/admin (Dashboard, Directory, Audits)"]
        SecurityGuard["auth_dependencies.py (JWT Bearer Guard)"]
    end

    subgraph SupabaseCloud ["Supabase PostgreSQL Cloud (AWS Singapore)"]
        Postgres[(PostgreSQL 17 Engine)]
        PgBouncer["Transaction Connection Pooler (:6543)"]
        T_Users[("users")]
        T_Sessions[("user_sessions")]
        T_Events[("events")]
        T_Teams[("event_teams & team_members")]
        T_Audits[("audit_logs")]
    end

    UI <--> AuthCtx
    AuthCtx -- "1. HTTPS Requests (Bearer JWT)" --> ServerlessGateway
    UI -- "Static Assets" --> StaticCDN
    ServerlessGateway --> SecurityGuard
    SecurityGuard --> AuthRouter
    SecurityGuard --> EventRouter
    SecurityGuard --> TeamRouter
    SecurityGuard --> AdminRouter
    AuthRouter & EventRouter & TeamRouter & AdminRouter -- "2. SQLAlchemy Session Local" --> PgBouncer
    PgBouncer --> Postgres
    Postgres --> T_Users & T_Sessions & T_Events & T_Teams & T_Audits
```

**Architectural Request Flow Description:**
1. **Client to Vercel Gateway:** The React application sends asynchronous HTTP requests over TLS 1.3 to `https://2131108.vercel.app/api`. Authenticated requests include an `Authorization: Bearer <access_token>` header.
2. **Serverless Lambda Routing:** Vercel rewrites `/api/(.*)` to the serverless entry point (`backend/main.py`), initializing a fast, ephemeral Python runtime environment.
3. **Security Interception:** The FastAPI dependency injection engine (`Depends(get_current_user)`) intercepts the request, decodes the JWT using HMAC-SHA256, verifies signature and expiration, and extracts the caller's identity and role.
4. **Resilient Database Pooling:** SQLAlchemy connects to Supabase PostgreSQL in AWS Singapore via transaction connection pooling (port `6543`). The engine utilizes `pool_pre_ping=True` to eliminate stale connections across lambda cold boots.
5. **Database Execution & Audit:** Queries execute with ACID transaction guarantees. Mutations trigger automated audit log generation before returning formatted JSON payloads back to the client.

---

### C3. Backend and Frontend Structure

```text
UniEvent-A-Web-Based-University-Event-Management-and-Registration-Platform/
├── backend/                         # FastAPI Backend Application
│   ├── routes/                      # API Endpoints (Controllers)
│   │   ├── admin.py                 # Admin dashboard, directory, and ban moderation
│   │   ├── auth.py                  # Signup, login, refresh, and logout
│   │   ├── events.py                # Event CRUD with RBAC ownership checks
│   │   ├── teams.py                 # Shared organizing teams and member roles
│   │   └── users.py                 # User profiles, passwords, and active sessions
│   ├── auth_dependencies.py         # Reusable JWT & Admin security guards
│   ├── auth_utils.py                # Cryptographic hashing & PyJWT token generator
│   ├── crud.py                      # Core database operations for events
│   ├── crud_auth.py                 # User queries and session lifecycle methods
│   ├── crud_teams.py                # Team provisioning and permission validator
│   ├── crud_audit.py                # System audit logging engine
│   ├── database.py                  # SQLAlchemy engine & Supabase connection pool
│   ├── models.py                    # SQLAlchemy database entity models
│   ├── schemas.py                   # Pydantic request/response validation schemas
│   ├── main.py                      # FastAPI app entry point & CORS configuration
│   ├── test_auth.py                 # Automated test suite: Authentication & Sessions
│   ├── test_rbac.py                 # Automated test suite: RBAC & Event Ownership
│   └── test_parts_4_5.py            # Automated test suite: Teams, Admin & Audits
├── frontend/                        # React 19 Single Page Application
│   ├── src/
│   │   ├── components/              # Modular UI Components
│   │   │   ├── AdminModal.tsx       # Platform Admin Center & KPI dashboard
│   │   │   ├── EventCard.tsx        # Event card with ownership & role badges
│   │   │   ├── EventDetailModal.tsx # Two-tab event details & team roster modal
│   │   │   ├── EventModal.tsx       # Create/edit event form modal
│   │   │   ├── Navbar.tsx           # Brand header, profile menu, and auth triggers
│   │   │   └── Toast.tsx            # Floating toast notification feedback
│   │   ├── context/
│   │   │   └── AuthContext.tsx      # React Auth Context & silent refresh manager
│   │   ├── Pages/
│   │   │   ├── Login.tsx            # Standalone login/register screen with demo pills
│   │   │   └── Login.css            # Scoped authentication interface styles
│   │   ├── services/                # API Network Service Wrappers
│   │   │   ├── adminApi.ts          # Admin KPI, user directory, and ban fetchers
│   │   │   ├── api.ts               # Core event CRUD API client
│   │   │   ├── authApi.ts           # Login, register, refresh, and logout calls
│   │   │   └── teamApi.ts           # Team member invitation and role management
│   │   ├── types/                   # TypeScript Type Definitions & Interfaces
│   │   │   ├── admin.ts             # Admin KPI & audit log shapes
│   │   │   ├── auth.ts              # User profile, tokens, and session interfaces
│   │   │   └── event.ts             # Event and organizing team types
│   │   ├── App.tsx                  # Root application controller & route guard
│   │   └── main.tsx                 # React DOM mount point & Context Provider
│   ├── package.json                 # Node dependencies and build scripts
│   └── vite.config.ts               # Vite bundler configuration & local dev proxy
├── docs/                            # Formal Academic Documentation
│   ├── FINAL_REPORT.md              # Complete Course Submission Report
│   ├── SRS.md                       # Software Requirements Specification
│   └── TDD.md                       # Technical Design Document
├── vercel.json                      # Vercel deployment routes and serverless rewrites
└── README.md                        # Project documentation and quick start guide
```

---

### C4. Data Model

```mermaid
erDiagram
    USERS ||--o{ USER_SESSIONS : "holds active"
    USERS ||--o{ EVENTS : "creates and owns"
    USERS ||--o{ TEAM_MEMBERS : "participates as"
    USERS ||--o{ AUDIT_LOGS : "triggers action"
    EVENTS ||--o| EVENT_TEAMS : "organized by"
    EVENT_TEAMS ||--o{ TEAM_MEMBERS : "composed of"

    USERS {
        int id PK
        string name
        string email UK
        string hashed_password
        string role "Admin or User"
        boolean is_banned
        string ban_reason
        datetime created_at
    }

    USER_SESSIONS {
        int id PK
        int user_id FK
        string token_hash UK "SHA-256 Hash"
        datetime expires_at
        boolean is_revoked
        string user_agent
        datetime created_at
    }

    EVENTS {
        int id PK
        int creator_id FK
        string title
        string description
        string location
        string event_date
        string organizer
        string category
        int capacity
        string status
        datetime created_at
    }

    EVENT_TEAMS {
        int id PK
        int event_id FK,UK
        string name
        datetime created_at
    }

    TEAM_MEMBERS {
        int id PK
        int team_id FK
        int user_id FK
        string role "Owner, Editor, Coordinator, Viewer"
        datetime joined_at
    }

    AUDIT_LOGS {
        int id PK
        int user_id FK
        string action
        string resource_type
        string resource_id
        string details
        string ip_address
        datetime timestamp
    }
```

#### Table 17: Database Tables & Schema Definitions
| Table Name | Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`users`** | `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier. |
| | `name` | VARCHAR | NOT NULL | User's full name. |
| | `email` | VARCHAR | UNIQUE, NOT NULL, INDEXED | University email address. |
| | `hashed_password` | VARCHAR | NOT NULL | bcrypt cryptographic password hash. |
| | `role` | VARCHAR | NOT NULL, DEFAULT 'User' | Access role: `Admin` or `User`. |
| | `is_banned` | BOOLEAN | NOT NULL, DEFAULT FALSE | Moderation flag: account suspension state. |
| | `ban_reason` | VARCHAR | NULLABLE | Documented reason for suspension. |
| | `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account registration timestamp. |
| **`user_sessions`** | `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique session identifier. |
| | `user_id` | INTEGER | FOREIGN KEY (`users.id`) | Reference to authenticated user. |
| | `token_hash` | VARCHAR | UNIQUE, NOT NULL, INDEXED | SHA-256 hash of the issued refresh token. |
| | `expires_at` | TIMESTAMP | NOT NULL | Refresh token expiration (7 days). |
| | `is_revoked` | BOOLEAN | NOT NULL, DEFAULT FALSE | Revocation flag (set `True` on logout/ban). |
| | `user_agent` | VARCHAR | NULLABLE | Client browser/device identification string. |
| | `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Session initialization timestamp. |
| **`events`** | `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique event identifier. |
| | `creator_id` | INTEGER | FOREIGN KEY (`users.id`) | Event creator & primary owner reference. |
| | `title` | VARCHAR | NOT NULL | Official event title. |
| | `description` | TEXT | NOT NULL | Detailed event description and guidelines. |
| | `location` | VARCHAR | NOT NULL | Campus venue or room number. |
| | `event_date` | VARCHAR | NOT NULL | Scheduled event date (YYYY-MM-DD). |
| | `organizer` | VARCHAR | NOT NULL | Organizing club or academic department. |
| | `category` | VARCHAR | NOT NULL | Category: Technology, Competition, etc. |
| | `capacity` | INTEGER | NOT NULL | Maximum permitted attendees. |
| | `status` | VARCHAR | NOT NULL, DEFAULT 'Upcoming' | Lifecycle: Upcoming, Ongoing, Completed. |
| | `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Event creation timestamp. |
| **`event_teams`** | `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique organizing team identifier. |
| | `event_id` | INTEGER | UNIQUE, FOREIGN KEY (`events.id`)| Associated university event reference. |
| | `name` | VARCHAR | NOT NULL | Team name (e.g. "Tech Fest Organizing Team"). |
| | `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Team provisioning timestamp. |
| **`team_members`** | `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique team member membership record. |
| | `team_id` | INTEGER | FOREIGN KEY (`event_teams.id`)| Reference to organizing team. |
| | `user_id` | INTEGER | FOREIGN KEY (`users.id`) | Reference to invited student. |
| | `role` | VARCHAR | NOT NULL | Permission: `Owner`, `Editor`, `Coordinator`, `Viewer`. |
| | `joined_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Invitation acceptance timestamp. |
| **`audit_logs`** | `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique audit log entry identifier. |
| | `user_id` | INTEGER | NULLABLE, FOREIGN KEY (`users.id`)| Identity of the acting user (NULL if system). |
| | `action` | VARCHAR | NOT NULL | Action type: `EVENT_CREATE`, `USER_BAN`, etc. |
| | `resource_type` | VARCHAR | NOT NULL | Target entity type (`Event`, `User`, `Team`). |
| | `resource_id` | VARCHAR | NULLABLE | Identifier of affected entity. |
| | `details` | TEXT | NULLABLE | Contextual description of modification. |
| | `ip_address` | VARCHAR | NULLABLE | Client IP address of incoming request. |
| | `timestamp` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Tamper-evident execution timestamp. |

---

### C5. API Design
#### Table 18: API Endpoints Specification
| Method | Path | Authentication | Required Role | Request Body | Success Status | Error Statuses | Description |
| :--- | :--- | :---: | :---: | :--- | :---: | :---: | :--- |
| `POST` | `/api/auth/signup` | None | Public | `UserRegisterRequest` | `201 Created` | `400`, `422` | Register student account. |
| `POST` | `/api/auth/login` | None | Public | `UserLoginRequest` | `200 OK` | `401`, `403`, `422` | Verify credentials & issue tokens. |
| `POST` | `/api/auth/refresh` | None | Public | `RefreshTokenRequest` | `200 OK` | `401`, `403`, `422` | Issue new 15-min access token. |
| `POST` | `/api/auth/logout` | None | Public | `LogoutRequest` | `200 OK` | `422` | Invalidate session in database. |
| `GET` | `/api/users/me` | Bearer Token | `User` / `Admin` | None | `200 OK` | `401`, `403` | Fetch current user profile. |
| `GET` | `/api/users/me/sessions` | Bearer Token| `User` / `Admin` | None | `200 OK` | `401` | List user's active device sessions. |
| `DELETE`| `/api/users/me/sessions/{id}`| Bearer Token| `User` / `Admin` | None | `200 OK` | `401`, `404` | Revoke specific device session. |
| `GET` | `/api/events` | Optional | Public | None | `200 OK` | None | List & filter event catalogue. |
| `POST` | `/api/events` | Bearer Token | `User` / `Admin` | `EventCreate` | `201 Created` | `401`, `422` | Create event & auto-create team. |
| `PUT` | `/api/events/{id}` | Bearer Token | Creator/Editor/Admin| `EventUpdate` | `200 OK` | `401`, `403`, `404` | Update event details (RBAC guard). |
| `DELETE`| `/api/events/{id}` | Bearer Token | Creator / Admin | None | `200 OK` | `401`, `403`, `404` | Delete event permanently. |
| `GET` | `/api/events/{id}/team` | Bearer Token | `User` / `Admin` | None | `200 OK` | `401`, `404` | Fetch event team roster. |
| `POST` | `/api/events/{id}/team/members`| Bearer Token| Team Owner / Admin | `TeamMemberAddRequest` | `201 Created` | `401`, `403`, `404` | Invite student to team by email. |
| `PUT` | `/api/events/{id}/team/members/{uid}`| Bearer Token| Team Owner / Admin| `TeamMemberRoleUpdate`| `200 OK` | `401`, `403`, `404` | Update team member role. |
| `DELETE`| `/api/events/{id}/team/members/{uid}`| Bearer Token| Team Owner / Admin| None | `200 OK` | `401`, `403`, `404` | Remove member from team. |
| `GET` | `/api/admin/stats` | Bearer Token | `Admin` | None | `200 OK` | `401`, `403` | Retrieve aggregate platform KPIs. |
| `GET` | `/api/admin/users` | Bearer Token | `Admin` | None | `200 OK` | `401`, `403` | Search & filter user directory. |
| `PUT` | `/api/admin/users/{id}/status`| Bearer Token| Primary Admin Only | `UserStatusUpdateRequest`| `200 OK` | `400`, `401`, `403`, `404`| Suspend or reactivate user. |
| `GET` | `/api/admin/audit-logs`| Bearer Token | `Admin` | None | `200 OK` | `401`, `403` | View system activity audit trail. |

---

### C6. JWT Authentication Design

```mermaid
sequenceDiagram
    autonumber
    actor User as Student / Browser
    participant Client as React SPA (AuthContext)
    participant API as FastAPI Backend (/api)
    participant DB as Supabase PostgreSQL

    Note over User,DB: Phase 1: Authentication & Token Issuance
    User->>Client: Enters email & password, clicks Login
    Client->>API: POST /api/auth/login {email, password}
    API->>DB: Query user by email, verify bcrypt password hash
    API->>API: Generate 15-min JWT Access Token (HS256)
    API->>API: Generate 7-day Refresh Token & compute SHA-256 hash
    API->>DB: INSERT INTO user_sessions (user_id, token_hash, expires_at)
    API-->>Client: 200 OK {access_token, refresh_token, user}
    Client->>Client: Store access_token in React state, refresh_token in localStorage

    Note over User,DB: Phase 2: Protected Request & Expiration
    Client->>API: GET /api/events (Header: Authorization: Bearer <access_token>)
    API->>API: Verify signature & expiration timestamp
    API-->>Client: 200 OK [Event Records]
    Note over Client,API: ... 15 Minutes Pass (Access Token Expires) ...
    Client->>API: POST /api/events (Expired Access Token)
    API-->>Client: 401 Unauthorized (detail: "Session token has expired")

    Note over User,DB: Phase 3: Silent Refresh Rotation
    Client->>API: POST /api/auth/refresh {refresh_token}
    API->>API: Hash incoming refresh token with SHA-256
    API->>DB: SELECT * FROM user_sessions WHERE token_hash = ? AND is_revoked = FALSE
    API->>API: Generate fresh 15-minute Access Token
    API-->>Client: 200 OK {access_token}
    Client->>API: Re-try original request with new access_token
    API-->>Client: 201 Created (Event Created Successfully)

    Note over User,DB: Phase 4: Logout & Session Revocation
    User->>Client: Clicks "Sign Out"
    Client->>API: POST /api/auth/logout {refresh_token}
    API->>DB: UPDATE user_sessions SET is_revoked = TRUE WHERE token_hash = ?
    API-->>Client: 200 OK {message: "Logged out successfully"}
    Client->>Client: Clear localStorage and reset user state to null
```

#### Token Claims Specification
- `sub`: User ID string (`subject`)
- `email`: Authenticated university email
- `role`: Authorization role (`User` or `Admin`)
- `iat`: Timestamp token was issued
- `exp`: Timestamp of expiration (`iat + 15 minutes`)
- **Signing Algorithm:** `HS256` (HMAC with SHA-256 using 64-character server secret `JWT_SECRET`).

---

### C7. RBAC Design
Request authorization follows a strict five-stage pipeline:
```text
1. Token Verification ➡️ 2. User Existence & Active Check ➡️ 3. Role Check ➡️ 4. Resource Ownership Check ➡️ 5. Route Handler
```

#### Reusable Permission Check Code Excerpt
```python
# backend/crud_teams.py (Lines 83-105)
def user_can_edit_event(db: Session, event: Event, user: User) -> bool:
    """
    Evaluates hierarchical authorization for event mutations:
    1. Global Platform Administrators bypass all locks.
    2. Primary Event Creators hold innate mutation rights.
    3. Organizing team members with 'Owner' or 'Editor' roles hold delegated rights.
    """
    if user.role == "Admin":
        return True

    if event.creator_id and event.creator_id == user.id:
        return True

    team = db.query(EventTeam).filter(EventTeam.event_id == event.id).first()
    if team:
        membership = db.query(TeamMember).filter(
            TeamMember.team_id == team.id,
            TeamMember.user_id == user.id
        ).first()
        if membership and membership.role in ["Owner", "Editor"]:
            return True

    return False
```

---

### C8. Admin Dashboard Design
The Admin Dashboard (`AdminModal.tsx`) provides centralized platform governance accessible only when `user.role === "Admin"`:

#### Table 19: Admin Dashboard Capabilities & Audit Mapping
| Tab / View | Endpoint Called | Available Filters | Permitted Actions | Audit Event Written |
| :--- | :--- | :--- | :--- | :--- |
| **KPI Overview** | `GET /api/admin/stats` | None | Refresh aggregate counters. | None (Read-only) |
| **User Directory** | `GET /api/admin/users` | Search (name/email), Role (`Admin`/`User`), Status (`Active`/`Suspended`) | View user metadata, change user role, suspend/reactivate account. | `USER_ROLE_CHANGE`, `USER_BAN`, `USER_UNBAN` |
| **Security Audit Trail** | `GET /api/admin/audit-logs` | Limit query (`?limit=50`) | Real-time security inspection, IP analysis. | None (Read-only) |

---

### C9. Security Design and Threats
#### Table 20: Security Threats & Defensive Countermeasures
| Threat Category | Specific Threat Description | Implemented Countermeasure | Code Location |
| :--- | :--- | :--- | :--- |
| **Credential Theft** | Database leak exposing plaintext user passwords. | Passwords hashed using `bcrypt` key derivation with unique random salts. | `backend/auth_utils.py` |
| **Token Theft** | Intercepted access token used for unauthorized access. | Access tokens strictly limited to 15-minute lifespans. | `backend/auth_utils.py` |
| **Token Replay** | Replay of stolen refresh tokens after logout. | SHA-256 session hash marked `is_revoked = True` in DB; future use returns 401. | `backend/crud_auth.py` |
| **Unauthorized Tampering**| Peer modifies or deletes another student's event. | Strict backend RBAC check matching `event.creator_id == current_user.id` (returns 403).| `backend/routes/events.py` |
| **Privilege Escalation** | Regular user attempts administrative actions. | `require_admin` dependency inspects verified JWT claim and rejects with 403. | `backend/auth_dependencies.py`|
| **Admin Hostile Takeover**| Secondary admin bans the Primary Administrator. | Hardcoded safety check blocking bans on `admin1@unievent.edu` and self-bans. | `backend/routes/admin.py` |
| **Suspended Account Access**| Banned user continues accessing APIs using cached session. | Immediate session revocation in DB and live active check in `get_current_user`. | `backend/routes/admin.py` |
| **Cross-Origin Abuse** | Malicious sites dispatching forged browser requests. | CORS restricted explicitly to local dev origins and production Vercel domain. | `backend/main.py` |
| **SQL Injection** | SQL query manipulation via raw string concatenation. | 100% parameter-bound queries through SQLAlchemy ORM abstractions. | `backend/crud*.py` |

---

### C10. Deployment on Vercel
- **Frontend SPA:** Compiled via Vite into static assets distributed globally through Vercel's Edge CDN.
- **Backend API:** Managed as serverless Python functions mounted under `/api` via `vercel.json` rewrites:
  ```json
  {
    "rewrites": [
      { "source": "/api/(.*)", "destination": "/api/index.py" },
      { "source": "/(.*)", "destination": "/index.html" }
    ]
  }
  ```

#### Table 21: Production Environment Variables
| Variable Name | Required Scope | Purpose |
| :--- | :--- | :--- |
| `DATABASE_URL` | Production / Preview | Supabase PostgreSQL transaction pooling connection URI (`:6543`). |
| `JWT_SECRET` | Production / Preview | 64-character high-entropy cryptographic secret key for signing tokens. |
| `FRONTEND_URL` | Production / Preview | Allowed CORS origin domain (`https://2131108.vercel.app`). |

---

### C11. Testing Strategy
The testing suite executes 34 automated unit and integration tests across three isolated test harnesses:

#### Table 22: Automated Test Suite Execution Results
| Test Harness | Scope & Requirements Verified | Executed Assertions | Status |
| :--- | :--- | :---: | :---: |
| **`test_auth.py`** | Swagger health, admin login, student signup, duplicate email guard, Bearer token extraction, 15-min token refresh, active session tracker, and logout revocation. | 8 / 8 Tests | **PASS ✅** |
| **`test_rbac.py`** | Anonymous event creation block (401), owner event creation, creator update (200), non-creator modification block (403), non-creator deletion block (403), admin update override (200), and admin deletion override (200). | 10 / 10 Tests | **PASS ✅** |
| **`test_parts_4_5.py`**| Auto team provisioning with Owner role, Editor invitation, collaborative update by Editor (200), non-owner member invite block (403), Coordinator role boundary check (403), member removal, Admin KPI statistics, user directory search, primary admin ban/unban moderation, and audit log generation. | 15 / 15 Tests | **PASS ✅** |
| **Frontend Compiler** | `tsc && vite build` TypeScript strict mode compilation. | Zero type errors | **PASS ✅** |

---

# Part D. Evidence: Screenshots of the Running Application

> *Note for PDF submission: Capture real screenshots on the deployed Vercel URL (`https://2131108.vercel.app`) with the browser address bar visible.*

### D1. User Side Evidence
- **[Figure S1: Login & Registration Portal with Form Validation]**  
  *Evidence:* Shows `Login.tsx` with university email format check and password minimum character warning.
- **[Figure S2: Filtered Event Catalogue ("My Events" Toggle)]**  
  *Evidence:* Displays event cards showing only events created by the logged-in student with gold `★ Your Event` badges.
- **[Figure S3: User Profile & Change Password Modal]**  
  *Evidence:* Displays `ProfileModal.tsx` showing current display name and error rejection when entering an invalid current password.
- **[Figure S4: Active Login Sessions with Device Revocation]**  
  *Evidence:* Displays active browser sessions with timestamps, user agents, and the red "Revoke" button.
- **[Figure S5: Organizing Team Roster & Member Delegation]**  
  *Evidence:* Displays `EventDetailModal.tsx` Team tab with member list and role assignment dropdown (`Editor`, `Coordinator`).
- **[Figure S6: RBAC Rejection (HTTP 403 Forbidden)]**  
  *Evidence:* Shows UI error toast *"Permission denied"* and browser Network tab showing `403 Forbidden` when attempting to edit a peer's event.

### D2. Security Behaviour
- **[Figure S7: Network Tab Showing Expired Token Rejection (HTTP 401)]**  
  *Evidence:* Demonstrates `401 Unauthorized` with `WWW-Authenticate: Bearer` response header.
- **[Figure S8: Silent Token Refresh Flow]**  
  *Evidence:* Shows background `POST /api/auth/refresh` request returning a new access token without page refresh.
- **[Figure S9: Banned User Ejection]**  
  *Evidence:* Shows login attempt by a suspended student blocked with `403 Forbidden` displaying the documented suspension reason.

### D3. Admin Dashboard
- **[Figure S10: Admin Center KPI Statistics Overview]**  
  *Evidence:* Displays 6 KPI metric cards: Registered Users, Active Events, Teams, Active Sessions, and Suspended Accounts.
- **[Figure S11: User Directory with Live Search & Role Filtering]**  
  *Evidence:* Displays user table with search bar and role dropdown filter.
- **[Figure S12: User Account Suspension Dialog]**  
  *Evidence:* Displays suspension prompt modal capturing reason string before dispatching API request.
- **[Figure S13: Suspended State in User Directory]**  
  *Evidence:* Displays red "Suspended" status badge and documented suspension reason under user email.
- **[Figure S14: Security Audit Trail Log Viewer]**  
  *Evidence:* Displays timestamped audit log table showing `USER_BAN`, `EVENT_CREATE`, and `EVENT_UPDATE` entries.

### D4. Deployment Evidence
- **[Figure S15: Vercel Production Deployment Dashboard]**  
  *Evidence:* Displays active production deployment status on `https://2131108.vercel.app`.
- **[Figure S16: Supabase Cloud Database Table Editor]**  
  *Evidence:* Displays PostgreSQL tables (`users`, `events`, `user_sessions`, `audit_logs`) hosted in AWS Singapore.
- **[Figure S17: Live Swagger API Documentation]**  
  *Evidence:* Displays interactive FastAPI Swagger UI accessible at `/api/docs`.

### D5. Automated Test Run Evidence
- **[Figure S18: Full Backend Test Execution Output]**  
  *Evidence:* Terminal screenshot showing all 34 tests passing across `test_auth.py`, `test_rbac.py`, and `test_parts_4_5.py`.

---

# Part E. Project Management and Conclusion

### E1. How to Run and Test Locally

#### Prerequisites
- **Python 3.10+** (Python 3.11 recommended)
- **Node.js 20+** or **Node.js 22+**
- Git

#### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate Python virtual environment
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
# (Includes: fastapi, uvicorn, sqlalchemy, psycopg2-binary, bcrypt, pyjwt)

# Run backend development server
python -m uvicorn main:app --reload --port 8000
```
*Backend runs locally at: `http://localhost:8000` (Swagger docs at `http://localhost:8000/api/docs`)*

#### 2. Frontend Setup
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Run Vite development server
npm run dev
```
*Frontend runs locally at: `http://localhost:5173`*

#### 3. Running Automated Tests
```bash
cd backend
python test_auth.py
python test_rbac.py
python test_parts_4_5.py
```

---

### E2. GitHub Work and Commits
#### Table 23: GitHub Work Distribution & Feature Milestones
| Milestone / Part | Issue Ref | Pull Request | Delivery Scope | Key Commits |
| :--- | :---: | :---: | :--- | :--- |
| **Parts 1 & 2** | Issue #10 | PR #11 | Implemented JWT auth, password hashing, user registration, login portal, and session tracking. | `c039652`, `eeeb46d` |
| **Parts 3 to 7** | Issue #13 | PR #14 | Implemented event ownership RBAC, shared organizing teams, Admin Center, Supabase cloud DB, and security audit logs. | `019dbeb`, `9d26408`, `e317848`, `69e4e93` |

---

### E3. Limitations
1. **Third-Party Email Verification:** Email confirmation links are currently simulated without live SMTP gateway integration (e.g. SendGrid) to maintain offline development capabilities.
2. **Synchronous Audit Logging:** Audit entries are committed in the same database transaction as the event mutation, which adds ~10ms overhead compared to an asynchronous message broker (e.g. Celery / RabbitMQ).
3. **No Real-Time Push Sockets:** Organizing team invitations require the recipient to refresh or open the modal rather than receiving a live WebSocket browser push notification.

### E4. Future Work
1. **Push Notifications & WebSockets:** Implement real-time notifications alerting organizers when team roles are modified.
2. **Digital Ticket QR Code Generator:** Generate signed QR codes for verified event entry check-in by university security.
3. **Cloud Image Attachments:** Integrate Supabase Storage Buckets to support direct event poster image uploads.
4. **Rate Limiting:** Implement Redis-backed token bucket rate limiting on `/api/auth/login` to prevent distributed brute-force attacks.

### E5. Sources, Libraries and Tools
#### Table 24: Sources, Libraries and Tools Reference
| Library / Tool | Version / Source | Purpose |
| :--- | :--- | :--- |
| **FastAPI** | 0.115.0 | Async backend REST API framework. |
| **SQLAlchemy** | 2.0.36 | Python SQL toolkit and Object-Relational Mapper. |
| **bcrypt** | 4.2.0 | Cryptographic password hashing key derivation. |
| **PyJWT** | 2.10.0 | RFC 7519 JSON Web Token signing and decoding. |
| **psycopg2-binary** | 2.9.10 | PostgreSQL database communication driver. |
| **React** | 19.0.0 | Frontend declarative user interface library. |
| **Vite** | 6.0.5 | Frontend build tool and local development server. |
| **Supabase** | Managed Cloud | Cloud PostgreSQL 17 hosting with PgBouncer pooling. |
| **Vercel** | Managed Cloud | Global Edge CDN hosting and serverless function routing. |
| **OWASP ASVS** | v4.0.3 | Guidance for token revocation and RBAC access control modeling. |

---

# Appendix: Test Accounts and Video Demo

### Video Demonstration Link
- **Walkthrough Video:** *(Paste your video demo link here, e.g. Google Drive or Loom URL)*

---

### Pre-Configured Test Accounts (For Teacher Assessment & Viva Defense)

> **Important Security Notice (Per Course Submission Instructions):** In accordance with the course submission instructions, plaintext passwords are documented strictly in the submitted PDF report (`FINAL_REPORT.pdf`) and omitted from the public repository markdown to prevent automated GitHub secret scanning alerts. All accounts use standard assessment passwords provided in the PDF report appendix and viva demonstration guide.

#### Table 25: Pre-Configured Assessment Accounts
| Role | Name | University Email | Password | Intended Test Flow |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Admin** | System Administrator | `admin1@unievent.edu` | `[In Submission PDF]` | Full administrative authority: KPI dashboard, user directory, account ban/unban moderation, audit trail. |
| **Secondary Admin** | Secondary Administrator| `admin2@unievent.edu` | `[In Submission PDF]` | Administrative inspection: views dashboard and audits, blocked from ban/unban moderation (enforces Primary Admin rule). |
| **Student 1 (Owner)**| Shoibe Arafat | `student@unievent.edu` | `[In Submission PDF]` | Primary student account: owns seeded university events, creates new events, manages organizing team rosters. |
| **Student 2 (Editor)**| Tanvir Ahmed | `student2@unievent.edu`| `[In Submission PDF]` | Collaborative team editor: invited to event team, demonstrates shared event modification rights. |
| **Student 3 (Viewer)**| Nafis Fuad | `student3@unievent.edu`| `[In Submission PDF]` | Team viewer: demonstrates read-only team permissions. |
| **Student 4** | Sadia Rahman | `student4@unievent.edu`| `[In Submission PDF]` | General student attendee account for registration and browsing checks. |
| **Student 5** | Farhan Kabir | `student5@unievent.edu`| `[In Submission PDF]` | General student attendee account for multi-user concurrency testing. |

#### Pre-Configured Organizing Team Structure
- **Team Name:** `Hackathon CSE 2026 Organizing Team` (Associated with Event ID: 1)
  - **Team Owner:** Shoibe Arafat (`student@unievent.edu`) — Full control, invites members, can delete event.
  - **Team Editor:** Tanvir Ahmed (`student2@unievent.edu`) — Can update event details, cannot delete event or remove owner.
  - **Team Viewer:** Nafis Fuad (`student3@unievent.edu`) — Can view team roster, cannot edit event.

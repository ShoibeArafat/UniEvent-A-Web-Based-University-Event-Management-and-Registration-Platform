"""
Event Organizing Team routes (Part 4).
Allows organizing teams to manage members with 4 permission tiers:
Owner, Editor, Coordinator, Viewer.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from database import get_db
import crud
import crud_auth
import crud_teams
import crud_audit
from models import User
from auth_dependencies import get_current_user
from schemas import (
    EventTeamResponse,
    TeamMemberResponse,
    TeamMemberAddRequest,
    TeamMemberUpdateRequest,
    MessageResponse,
)

router = APIRouter(prefix="/api/events/{event_id}/team", tags=["teams"])


def format_team_response(team) -> EventTeamResponse:
    """Helper to convert ORM EventTeam into EventTeamResponse with user fields."""
    return EventTeamResponse(
        id=team.id,
        event_id=team.event_id,
        name=team.name,
        created_at=team.created_at,
        members=[
            TeamMemberResponse(
                id=m.id,
                user_id=m.user_id,
                user_name=m.user.name if m.user else "Unknown User",
                user_email=m.user.email if m.user else "unknown@unievent.edu",
                role=m.role,
                joined_at=m.joined_at,
            )
            for m in team.members
        ],
    )


@router.get(
    "",
    response_model=EventTeamResponse,
    summary="Get event organizing team",
    description="Retrieves the event organizing team and member roster.",
)
def get_event_team(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = crud.get_event_by_id(db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )

    team = crud_teams.get_or_create_event_team(db, event=event)
    return format_team_response(team)


@router.post(
    "/members",
    response_model=EventTeamResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a member to the event organizing team",
    description="Only the event Owner or an Admin can invite new members by university email.",
)
def add_team_member(
    event_id: int,
    payload: TeamMemberAddRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = crud.get_event_by_id(db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )

    team = crud_teams.get_or_create_event_team(db, event=event)

    # Authorization: Must be Admin or have Owner role on the team
    is_admin = current_user.role == "Admin"
    current_membership = crud_teams.get_team_member(db, team_id=team.id, user_id=current_user.id)
    is_owner = (event.creator_id == current_user.id) or (
        current_membership and current_membership.role == "Owner"
    )

    if not is_admin and not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: Only the Event Owner or an Administrator can invite team members.",
        )

    # Find the target user by email
    target_user = crud_auth.get_user_by_email(db, email=payload.email)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{payload.email}' is not registered on UniEvent.",
        )

    # Check if already a member
    existing = crud_teams.get_team_member(db, team_id=team.id, user_id=target_user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{target_user.name} ({target_user.email}) is already a member of this organizing team.",
        )

    # Validate role tier
    valid_roles = ["Owner", "Editor", "Coordinator", "Viewer"]
    role = payload.role.strip().capitalize()
    if role not in valid_roles:
        role = "Editor"

    crud_teams.add_team_member(db, team_id=team.id, user_id=target_user.id, role=role)

    # Log audit entry
    crud_audit.create_audit_log(
        db=db,
        action="TEAM_MEMBER_ADD",
        resource_type="EventTeam",
        resource_id=str(team.id),
        user_id=current_user.id,
        details=f"Added {target_user.email} as {role} to {event.title} team",
        ip_address=request.client.host if request.client else None,
    )

    # Refresh and return
    db.refresh(team)
    return format_team_response(team)


@router.put(
    "/members/{user_id}",
    response_model=EventTeamResponse,
    summary="Update a team member's role",
    description="Updates member permissions (Owner, Editor, Coordinator, Viewer). Owner/Admin only.",
)
def update_team_member_role(
    event_id: int,
    user_id: int,
    payload: TeamMemberUpdateRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = crud.get_event_by_id(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    team = crud_teams.get_or_create_event_team(db, event=event)

    # Check caller authority
    is_admin = current_user.role == "Admin"
    current_membership = crud_teams.get_team_member(db, team_id=team.id, user_id=current_user.id)
    is_owner = (event.creator_id == current_user.id) or (
        current_membership and current_membership.role == "Owner"
    )

    if not is_admin and not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: Only the Event Owner or an Administrator can modify member roles.",
        )

    target_membership = crud_teams.get_team_member(db, team_id=team.id, user_id=user_id)
    if not target_membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found on this team")

    valid_roles = ["Owner", "Editor", "Coordinator", "Viewer"]
    role = payload.role.strip().capitalize()
    if role not in valid_roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role. Must be one of: {valid_roles}")

    crud_teams.update_team_member_role(db, member=target_membership, new_role=role)

    crud_audit.create_audit_log(
        db=db,
        action="TEAM_MEMBER_ROLE_UPDATE",
        resource_type="EventTeam",
        resource_id=str(team.id),
        user_id=current_user.id,
        details=f"Updated user ID {user_id} role to {role} in {event.title} team",
        ip_address=request.client.host if request.client else None,
    )

    db.refresh(team)
    return format_team_response(team)


@router.delete(
    "/members/{user_id}",
    response_model=EventTeamResponse,
    summary="Remove a member from the organizing team",
    description="Removes a member from the team. Permitted for Owner, Admin, or self-leave.",
)
def remove_team_member(
    event_id: int,
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = crud.get_event_by_id(db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    team = crud_teams.get_or_create_event_team(db, event=event)

    is_admin = current_user.role == "Admin"
    current_membership = crud_teams.get_team_member(db, team_id=team.id, user_id=current_user.id)
    is_owner = (event.creator_id == current_user.id) or (
        current_membership and current_membership.role == "Owner"
    )
    is_self = current_user.id == user_id

    if not is_admin and not is_owner and not is_self:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: You cannot remove this member from the team.",
        )

    # Protect against removing the primary event creator unless admin
    if event.creator_id == user_id and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove the original event creator from the organizing team.",
        )

    target_membership = crud_teams.get_team_member(db, team_id=team.id, user_id=user_id)
    if not target_membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found on this team")

    crud_teams.remove_team_member(db, member=target_membership)

    crud_audit.create_audit_log(
        db=db,
        action="TEAM_MEMBER_REMOVE",
        resource_type="EventTeam",
        resource_id=str(team.id),
        user_id=current_user.id,
        details=f"Removed user ID {user_id} from {event.title} team",
        ip_address=request.client.host if request.client else None,
    )

    db.refresh(team)
    return format_team_response(team)

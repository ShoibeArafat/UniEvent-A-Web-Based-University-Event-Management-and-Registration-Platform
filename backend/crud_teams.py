"""
CRUD operations for Event Teams and Team Members (Part 4).
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models import Event, EventTeam, TeamMember, User


def get_or_create_event_team(db: Session, event: Event) -> EventTeam:
    """
    Retrieves the organizing team for an event, or creates it automatically.
    Ensures the event creator is registered as the initial 'Owner' member.
    """
    team = db.query(EventTeam).filter(EventTeam.event_id == event.id).first()
    if not team:
        team = EventTeam(
            event_id=event.id,
            name=f"{event.title} Organizing Team",
        )
        db.add(team)
        db.commit()
        db.refresh(team)

    # Ensure creator is registered as Owner if creator_id is set
    if event.creator_id:
        existing_owner = db.query(TeamMember).filter(
            TeamMember.team_id == team.id,
            TeamMember.user_id == event.creator_id
        ).first()
        if not existing_owner:
            owner_member = TeamMember(
                team_id=team.id,
                user_id=event.creator_id,
                role="Owner",
            )
            db.add(owner_member)
            db.commit()
            db.refresh(team)

    return team


def get_event_team_by_id(db: Session, team_id: int) -> Optional[EventTeam]:
    """Retrieve an event team by its primary key."""
    return db.query(EventTeam).filter(EventTeam.id == team_id).first()


def get_team_member(db: Session, team_id: int, user_id: int) -> Optional[TeamMember]:
    """Find a specific user's membership on a team."""
    return db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()


def add_team_member(db: Session, team_id: int, user_id: int, role: str = "Editor") -> TeamMember:
    """Add a new member to an organizing team."""
    member = TeamMember(
        team_id=team_id,
        user_id=user_id,
        role=role,
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def update_team_member_role(db: Session, member: TeamMember, new_role: str) -> TeamMember:
    """Update a team member's role (Owner, Editor, Coordinator, Viewer)."""
    member.role = new_role
    db.commit()
    db.refresh(member)
    return member


def remove_team_member(db: Session, member: TeamMember) -> None:
    """Remove a member from the organizing team."""
    db.delete(member)
    db.commit()


def user_can_edit_event(db: Session, event: Event, user: User) -> bool:
    """
    Checks if a user is permitted to edit an event:
    1. System Administrator
    2. Event Creator (creator_id == user.id)
    3. Team member with role 'Owner' or 'Editor'
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

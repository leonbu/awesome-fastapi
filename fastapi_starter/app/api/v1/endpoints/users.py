from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.api.deps import (
    CurrentUserDep,
    SessionDep,
    get_current_active_superuser,
)
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
async def read_current_user(current_user: CurrentUserDep):
    """Fetch details of the currently logged-in user."""
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
)
async def update_current_user(
    user_in: UserUpdate,
    current_user: CurrentUserDep,
    db: SessionDep,
):
    """Update profile information for the currently logged-in user."""
    return await UserService(db).update(current_user, user_in)


@router.get(
    "/",
    response_model=list[UserResponse],
    dependencies=[Depends(get_current_active_superuser)],
    summary="List all users (Superuser only)",
)
async def read_users(
    db: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    """Retrieve all users. Requires superuser privileges."""
    return await UserService(db).get_multi(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(get_current_active_superuser)],
    summary="Get user by ID (Superuser only)",
)
async def read_user_by_id(user_id: int, db: SessionDep):
    """Retrieve a specific user by ID. Requires superuser privileges."""
    user = await UserService(db).get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

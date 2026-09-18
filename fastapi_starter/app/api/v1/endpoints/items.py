from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, status
from app.api.deps import CurrentUserDep, SessionDep
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter()


@router.get(
    "/",
    response_model=list[ItemResponse],
    summary="List items belonging to current user",
)
async def read_items(
    current_user: CurrentUserDep,
    db: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    """Retrieve all items created by the authenticated user."""
    return await ItemService(db).get_multi_by_owner(
        owner_id=current_user.id, skip=skip, limit=limit
    )


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item",
)
async def create_item(
    item_in: ItemCreate,
    current_user: CurrentUserDep,
    db: SessionDep,
):
    """Create a new item owned by the current user."""
    return await ItemService(db).create_with_owner(
        item_in=item_in, owner_id=current_user.id
    )


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get item by ID",
)
async def read_item(item_id: int, current_user: CurrentUserDep, db: SessionDep):
    """Retrieve details of a single item owned by current user."""
    item = await ItemService(db).get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this item",
        )
    return item


@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update an item",
)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    current_user: CurrentUserDep,
    db: SessionDep,
):
    """Update an item owned by current user."""
    service = ItemService(db)
    item = await service.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this item",
        )
    return await service.update(item, item_in)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
)
async def delete_item(
    item_id: int,
    current_user: CurrentUserDep,
    db: SessionDep,
):
    """Delete an item owned by current user."""
    service = ItemService(db)
    item = await service.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this item",
        )
    await service.delete(item)

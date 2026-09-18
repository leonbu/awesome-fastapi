from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, item_id: int) -> Item | None:
        result = await self.db.execute(select(Item).where(Item.id == item_id))
        return result.scalars().first()

    async def get_multi_by_owner(
        self, owner_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Item]:
        result = await self.db.execute(
            select(Item).where(Item.owner_id == owner_id).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create_with_owner(self, item_in: ItemCreate, owner_id: int) -> Item:
        item = Item(**item_in.model_dump(), owner_id=owner_id)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update(self, item: Item, item_in: ItemUpdate) -> Item:
        update_data = item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete(self, item: Item) -> None:
        await self.db.delete(item)
        await self.db.commit()

from typing import List, Dict
from fastapi.routing import APIRouter
from fastapi import Request, Depends
from . import models as api_models

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.database import models as db_models

from sqlalchemy import select

items = APIRouter(prefix="/items")


@items.get("/", response_model=api_models.GetItemStoreResponse)
async def get_item_store(
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    query = select(db_models.ItemStore).order_by(db_models.ItemStore.item_id.asc())
    data = await session.stream_scalars(query)

    return {"items": [i.to_dict() async for i in data]}


@items.post("/", response_model=api_models.PostItemStoreResponse)
async def post_item_store(
    request: Request,
    payload: api_models.PostItemStorePayload,
    session: AsyncSession = Depends(get_db),
):
    item_ids = [i.item_id for i in payload.items]

    query = select(db_models.ItemStore).filter(
        db_models.ItemStore.item_id.in_(item_ids)
    )
    data = await session.stream_scalars(query)

    item_map: Dict[str, db_models.ItemStore] = {i.item_id: i async for i in data}
    for item in payload.items:
        item_row = item_map.get(item.item_id)
        if item_row is None:
            item_row = db_models.ItemStore(item_id=item.item_id)
            item_map[item.item_id] = item_row

        item_row.item_count = item.item_count

    session.add_all(item_map.values())
    await session.commit()

    return {"items": [i.to_dict() for i in item_map.values()]}

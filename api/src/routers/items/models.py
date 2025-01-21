from typing import List
from pydantic import BaseModel
from datetime import datetime


class ItemStore(BaseModel):
    """
    Represents a single item and its count in a ME storage system.
    """

    item_id: str
    item_count: int


class ItemStoreResponse(ItemStore):
    version_timestamp: datetime


class PostItemStorePayload(BaseModel):
    items: List[ItemStore]


class PostItemStoreResponse(BaseModel):
    items: List[ItemStore]


class GetItemStoreResponse(BaseModel):
    items: List[ItemStoreResponse]

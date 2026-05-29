"""
crud.py
[DOMAIN: GENERIC] Fabryka routera CRUD — reużywalna logika endpointów.
"""
from typing import Any, Callable, Type

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.common.store import InMemoryStore


def create_crud_router(
    prefix: str,
    tag: str,
    store: InMemoryStore,
    create_model: Type[BaseModel],
    update_model: Type[BaseModel],
    response_model: Type[BaseModel],
    to_response: Callable[[dict[str, Any]], BaseModel],
) -> APIRouter:
    """
    Tworzy router z pełnym CRUD: GET lista, GET jeden, POST, PUT, DELETE.
    """
    router = APIRouter(prefix=prefix, tags=[tag])

    @router.get("", response_model=list[response_model])
    def list_items() -> list[BaseModel]:
        return [to_response(item) for item in store.list_all()]

    @router.get("/{item_id}", response_model=response_model)
    def get_item(item_id: int) -> BaseModel:
        item = store.get(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail=f"{tag} o id={item_id} nie istnieje")
        return to_response(item)

    @router.post("", response_model=response_model, status_code=201)
    def create_item(body: create_model) -> BaseModel:  # type: ignore[valid-type]
        item = store.create(body.model_dump(exclude_unset=True))
        return to_response(item)

    @router.put("/{item_id}", response_model=response_model)
    def update_item(item_id: int, body: update_model) -> BaseModel:  # type: ignore[valid-type]
        item = store.update(item_id, body.model_dump(exclude_unset=True))
        if item is None:
            raise HTTPException(status_code=404, detail=f"{tag} o id={item_id} nie istnieje")
        return to_response(item)

    @router.delete("/{item_id}", status_code=204)
    def delete_item(item_id: int) -> None:
        if not store.delete(item_id):
            raise HTTPException(status_code=404, detail=f"{tag} o id={item_id} nie istnieje")

    return router

from src.database import geo
from src.municipality.models import Municipality

municipality_collection = geo.Municipality


async def fetch_all_municipalities() -> list[Municipality]:
    """
    Fetches all municipality documents from the collection
    and returns them as a list of Municipality objects.
    """
    municipalities = []
    cursor = municipality_collection.find({})
    async for document in cursor:
        municipalities.append(Municipality(**document))

    return municipalities


async def fetch_municipality_by_id(m_id: int) -> dict[str, str] | None:
    """
    Retrieves a municipality document from the collection based on the given ID.
    """
    document = await municipality_collection.find_one({"m_id": m_id})
    return document


async def create_municipality(municipality: Municipality) -> dict[str, str]:
    """
    Inserts a new municipality document into the collection
    and returns the created municipality.
    """
    await municipality_collection.insert_one(municipality.dict())
    return municipality.dict()


async def create_many_municipalities(
    municipalities: list[dict[str, str]],
) -> list[dict[str, str]]:
    """
    Inserts multiple municipality documents into the collection
    and returns a list of municipalities.
    """
    await municipality_collection.insert_many(municipalities)
    return municipalities


async def update_municipality(m_id: int, data: dict[str, str]) -> dict[str, str] | None:
    """
    Updates the name and state fields of a municipality document
    identified by the given ID, and returns the updated document.
    """
    updated_municipality = await municipality_collection.update_one(
        {"m_id": m_id},
        {"$set": data},
    )
    if updated_municipality.modified_count == 1:
        return await municipality_collection.find_one({"m_id": m_id})
    return None


async def remove_municipality(m_id: int) -> bool:
    """
    Deletes a municipality document from the collection based
    on the given ID, and returns True if the deletion was successful.
    """
    deleted_municipality = await municipality_collection.delete_one({"m_id": m_id})
    if deleted_municipality.deleted_count == 1:
        return True
    return False


async def remove_all_municipalities() -> None:
    """Removes all municipalities from the database"""
    x = await municipality_collection.delete_many({})
    print(f"Removed all ({x.deleted_count}) municipalities from the database.")

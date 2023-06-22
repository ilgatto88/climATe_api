from typing import Any

from app.core.database import climate_data
from app.core.models import MunicipalityData

municipality_data_collection = climate_data.MunicipalityData


async def fetch_municipality_data_by_id(m_id: int) -> dict[str, Any] | None:
    """
    Retrieves a municipality data document from the collection based on the given ID.
    """
    document = await municipality_data_collection.find_one(
        {"meta.municipalityId": m_id}
    )
    return document


async def create_municipality_data(
    municipality_data: MunicipalityData,
) -> MunicipalityData:
    """
    Inserts a new municipality data document into the collection
    and returns the created municipality data.
    """
    await municipality_data_collection.insert_one(municipality_data.dict())
    return municipality_data


async def remove_municipality_data_by_id(m_id: int) -> dict[str, Any] | None:
    """
    Removes a municipality data document from the collection based on the given ID.
    """
    document = await municipality_data_collection.find_one_and_delete(
        {"meta.municipalityId": m_id}
    )
    return document

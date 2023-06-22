import json

import pytest

from app.core.models import Municipality
from app.municipality import municipality_db
from app.tests.conftest import TEST_DATA_PATH


@pytest.mark.anyio
async def test_create_municipality():
    municipality = await municipality_db.create_municipality(
        Municipality(m_id=99999, name="Test Municipality", state="Test State")
    )
    assert municipality.m_id == 99999
    assert municipality.name == "Test Municipality"
    assert municipality.state == "Test State"


@pytest.mark.anyio(scope="module")
async def test_fetch_all_municipalities():
    municipalities = await municipality_db.fetch_all_municipalities()
    assert len(municipalities) > 0


@pytest.mark.anyio
async def test_fetch_municipality_by_id():
    test_municipality = Municipality(
        m_id=99999, name="Test Municipality", state="Test State"
    )
    municipality = await municipality_db.fetch_municipality_by_id(99999)
    assert municipality is not None
    municipality.pop("_id")
    assert municipality == test_municipality.dict()


@pytest.mark.anyio(scope="module")
async def test_update_municipality():
    municipality = await municipality_db.update_municipality(
        m_id=99999, name="Test Municipality 2", state="Test State 2"
    )
    assert municipality is not None
    assert municipality["name"] == "Test Municipality 2"
    assert municipality["state"] == "Test State 2"


@pytest.mark.anyio(scope="module")
async def test_delete_municipality():
    await municipality_db.remove_municipality(99999)
    municipality = await municipality_db.fetch_municipality_by_id(99999)
    assert municipality is None


@pytest.mark.anyio(scope="module")
async def test_delete_municipality_which_doesnt_exist():
    municipality = await municipality_db.remove_municipality(99999)
    assert municipality is False


@pytest.mark.anyio(scope="module")
async def test_delete_all_municipalities():
    await municipality_db.remove_all_municipalities()
    municipalities = await municipality_db.fetch_all_municipalities()
    assert len(municipalities) == 0


@pytest.mark.anyio(scope="module")
async def test_create_many_municipalities():
    sample_file_path = f"{TEST_DATA_PATH}/sample_municipalities.json"
    with open(sample_file_path) as json_file:
        sample_data = json.load(json_file)
    municipalities = await municipality_db.create_many_municipalities(sample_data)
    assert len(municipalities) > 2000
    assert len(municipalities) > 2000

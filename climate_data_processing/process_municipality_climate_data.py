from climate_data_processing import (
    config,
    create_data_dictionaries,
    format_conversion,
    process_historical,
    process_oeks,
)
from core.api_models import Municipality
from core.misc_models import MunicipalityDataSettings


def create_municipality_climate_data(settings: MunicipalityDataSettings):
    meta_dict = create_data_dictionaries.create_municipality_meta_dict(settings)

    historical_dict = create_data_dictionaries.create_historical_data_dict()
    historical_dict["historical"].update(
        process_historical.create_historical_raw_data(settings)
    )
    historical_dict["historical"].update(
        process_historical.create_historical_statistics(settings)
    )

    oeks_1d_model_statistics = process_oeks.oeks_1d_data_pipeline(settings)
    ensemble_dict = create_data_dictionaries.create_ensemble_data_dict(
        oeks_1d_model_statistics
    )
    ensemble_dict["ensemble"]["modelStatistics0D"] = process_oeks.oeks_0d_data_pipeline(
        settings
    )

    climate_data_dict = format_conversion.concatenate_dictionaries(
        [meta_dict, historical_dict, ensemble_dict]
    )

    return climate_data_dict


if __name__ == "__main__":
    municipality = Municipality(
        m_id=10101,
        name="Eisenstadt",
        state="Burgenland",
    )

    municipality_settings = MunicipalityDataSettings(
        municipality=municipality,
        scenario="rcp26",
        parameter="tm",
        temporal_resolution="annual",
        analysis_start_year=config.ANALYSIS_START_YEAR,
        analysis_end_year=config.ANALYSIS_END_YEAR,
        ensemble_start_year=config.ENSEMBLE_START_YEAR,
        ensemble_end_year=config.ENSEMBLE_END_YEAR,
    )

    print(
        f"Processing {municipality_settings.municipality.name}: "
        f"{municipality_settings.scenario} - {municipality_settings.parameter} ..."
    )
    data = create_municipality_climate_data(municipality_settings)
    print(data)
    print("Processing finished.")

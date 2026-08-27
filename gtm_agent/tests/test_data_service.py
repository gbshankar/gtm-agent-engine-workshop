from gtm_agent import data_service


def test_update_prospect_info_persists_technology():
    prospect_id = "LEAD-39002"
    technology = "Terraform"
    original_tech_stack = list(data_service.PROSPECTS[prospect_id]["tech_stack"])
    data_service._PROFILES.pop(prospect_id, None)

    try:
        data_service.update_prospect_info(prospect_id, technology)
        assert technology in data_service.fetch_tech_stack(prospect_id)
    finally:
        data_service.PROSPECTS[prospect_id]["tech_stack"] = original_tech_stack
        data_service._PROFILES.pop(prospect_id, None)

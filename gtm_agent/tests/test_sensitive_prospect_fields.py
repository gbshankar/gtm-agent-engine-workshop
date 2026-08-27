from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile, get_prospect


SENSITIVE_FIELDS = {
    "billing_qualification",
    "tax_id",
    "date_of_birth",
    "card_on_file",
    "credit_check_ref",
}


def test_prospect_tools_and_profile_cache_exclude_sensitive_fields():
    data_service._PROFILES.clear()

    prospect = get_prospect.invoke({"prospect_id": "LEAD-71001"})
    profile = build_prospect_profile.invoke({"prospect_id": "LEAD-71001"})

    assert SENSITIVE_FIELDS.isdisjoint(prospect["prospect"].keys())
    assert SENSITIVE_FIELDS.isdisjoint(profile["prospect_profile"].keys())
    assert SENSITIVE_FIELDS.isdisjoint(
        data_service.get_profile_from_db("LEAD-71001")["prospect_profile"].keys()
    )


def test_save_profile_redacts_nested_sensitive_fields():
    data_service._PROFILES.clear()

    data_service.save_profile_to_db(
        "LEAD-test",
        {
            "name": "Test Prospect",
            "billing_qualification": {"tax_id": "123-45-6789"},
            "nested": [{"card_on_file": "4111111111111111"}],
        },
    )

    saved = data_service.get_profile_from_db("LEAD-test")["prospect_profile"]
    assert saved == {"name": "Test Prospect", "nested": [{}]}

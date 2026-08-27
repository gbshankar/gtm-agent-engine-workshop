import os
from types import SimpleNamespace

os.environ.setdefault("OPENAI_API_KEY", "test")

from gtm_agent import data_service
from gtm_agent.gtm_agent import send_prospect_email


def test_send_prospect_email_blocks_disqualified_prospect(monkeypatch):
    prospect_id = "LEAD-50002"
    prospect = {
        "prospect_id": prospect_id,
        "name": "Liam O'Brien",
        "email": "liam.obrien@meridiansystems.com",
    }
    monkeypatch.setattr(
        data_service,
        "get_prospect_record",
        lambda requested_id: {"disqualified": requested_id == prospect_id},
    )

    result = send_prospect_email.func(
        prospect,
        "Scheduling a Technical Deep Dive",
        "Please let me know your availability.",
        SimpleNamespace(config={}),
    )

    assert result == {
        "status": "blocked",
        "reason": "prospect is disqualified",
        "prospect_id": prospect_id,
    }
    assert "message_id" not in result

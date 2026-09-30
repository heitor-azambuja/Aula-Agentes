from app.api import create_app


def test_simulate_endpoint_returns_summary_and_monthly_records():
    client = create_app().test_client()

    response = client.post(
        "/api/simulate",
        json={
            "initial_amount": 1000,
            "annual_interest_rate": 0,
            "duration_months": 2,
            "monthly_contribution": 100,
            "one_time_withdrawals": [{"month": 2, "amount": 50}],
            "recurring_withdrawals": [],
        },
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["summary"] == {
        "final_balance": 1150.0,
        "total_contributed": 1200.0,
        "total_withdrawn": 50.0,
        "total_interest": 0.0,
    }
    assert len(data["monthly_records"]) == 2


def test_simulate_endpoint_returns_400_for_invalid_payload():
    client = create_app().test_client()

    response = client.post(
        "/api/simulate",
        json={
            "initial_amount": -1,
            "annual_interest_rate": 0,
            "duration_months": 2,
            "monthly_contribution": 0,
        },
    )

    assert response.status_code == 400
    assert "aporte inicial" in response.get_json()["error"]

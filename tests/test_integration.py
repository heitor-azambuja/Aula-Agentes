from app.api import create_app
from run import app


def test_create_app_can_mount_dashboard_and_keep_api_available():
    client = create_app(include_dashboard=True).test_client()

    root_response = client.get("/")
    dashboard_response = client.get("/dashboard/")
    api_response = client.post(
        "/api/simulate",
        json={
            "initial_amount": 1000,
            "annual_interest_rate": 0,
            "duration_months": 1,
            "monthly_contribution": 0,
        },
    )

    assert root_response.status_code == 302
    assert root_response.headers["Location"] == "/dashboard/"
    assert dashboard_response.status_code == 200
    assert api_response.status_code == 200


def test_run_module_exposes_integrated_flask_app():
    assert app.test_client().get("/dashboard/").status_code == 200

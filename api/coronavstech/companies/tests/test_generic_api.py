import pytest
import requests
import json

# import responses

testing_env_companies_url = "http://127.0.0.1:8000/companies/"


@pytest.mark.skip_in_ci
def test_zero_companies_django_agnostic() -> None:
    response = requests.get(url=testing_env_companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_create_company_with_layoffs_django_agnostic() -> None:
    response = requests.post(
        url=testing_env_companies_url,
        data={"name": "test company name", "status": "Layoffs"},
    )
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("status") == "Layoffs"

    cleanup_company(company_id=response_content["id"])


def cleanup_company(company_id: str) -> None:
    response = requests.delete(url=f"http://127.0.0.1:8000/companies/{company_id}")
    assert response.status_code == 204


@pytest.mark.exchange_rate
@pytest.mark.skip(reason="This test needs not free version of the site presented in url.")
def test_min_fin_api() -> None:
    url = "https://api.minfin.com.ua/mb/72e37eb216279d8bacac77132ea2b183ccbe1c86/"
    response = requests.get(url=url)
    assert response.status_code == 200
    response_content = json.loads(response.content)
    assert response_content[0]["currency"] == "eur"


# TODO should include example of json.
# @pytest.mark.exchange_rate
# @responses.activate
# def test_mocked_min_fin_api() -> None:
#     url = "https://api.minfin.com.ua/mb/72e37eb216279d8bacac77132ea2b183ccbe1c86/"
#     responses.add(responses.GET, url=url, json={'error': 'not found'}, status=404)
#     response = requests.get(url=url)
#     assert response.status_code == 404
#     response_content = json.loads(response.content)
#     assert response_content[0]['currency'] == 'usd'

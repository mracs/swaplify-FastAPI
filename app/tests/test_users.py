from fastapi.testclient import TestClient

from app.main import app
from app.core.utils import get_token

test_source = "{'commercial': True, 'offer_type': 'sale'}"
test_invalid_source = "{'commercial': True, 'offer_type': null}"
test_user_ip = 'testclient'
test_uuid = str(get_token(f'{test_user_ip}:{test_source}'))


def test_pydict_to_json(temp_db):
    test_data = [
        {'body': {'source': test_source}, 'status': 200},
        {'body': {'source': test_invalid_source}, 'status': 200},
        {'body': {'somekey': 'value'}, 'status': 422},
        {'body': {}, 'status': 422}
    ]
    for item in test_data:
        with TestClient(app) as client:
            response = client.post(
                '/pydict-to-json',
                json=item['body'],
            )
            assert response.status_code == item['status']
            if response.status_code not in (200, 422):
                assert response.json()['detail']
            elif response.status_code == 200:
                assert response.json().get('res') or response.json().get('err')


def test_save_and_share(temp_db):
    test_data = [
        {'body': {'source': test_source}, 'status': 201},
        {'body': {'source': test_source}, 'status': 200},
        {'body': {'somekey': 'value'}, 'status': 422},
        {'body': {}, 'status': 422}
    ]
    for item in test_data:
        with TestClient(app) as client:
            response = client.post(
                '/save-and-share',
                json=item['body'],
            )
        assert response.status_code == item['status']


def test_get_source(temp_db):
    test_data = [
        {'token': test_uuid, 'status': 200},
        {'token': 'test', 'status': 400},
        {'token': get_token('test'), 'status': 404}
    ]
    for item in test_data:
        with TestClient(app) as client:
            response = client.get(f'/source/{item["token"]}')
            assert response.status_code == item['status']
            if response.status_code == 200:
                assert response.json() == {'source': test_source}


def test_update_source(temp_db):
    test_data = [
        {
            'token': test_uuid,
            'body': {'source': "{'commercial': True, 'offer_type': null}"},
            'status': 204
        },
        {
            'token': 'test_uuid',
            'body': {'source': "{'commercial': True, 'offer_type': null}"},
            'status': 400,
            'detail': 'UUID is not valid'
        },
        {'token': 'test_uuid', 'body': {'somekey': 'value'}, 'status': 422},
        {'token': test_uuid, 'body': {}, 'status': 422},
        {
            'token': get_token('test'),
            'body': {'source': test_source},
            'status': 404,
            'detail': 'Source not found'
        },
        {'token': get_token('test'), 'body': {}, 'status': 422},
    ]
    for item in test_data:
        with TestClient(app) as client:
            response = client.patch(f'/source/{item["token"]}',
                                    json=item['body'])
            assert response.status_code == item['status']
            if response.status_code not in (204, 422):
                assert response.json()['detail'] == item['detail']

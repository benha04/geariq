import json
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_search_rationale_shape():
    res = client.get('/v1/search?q=MIPS+helmet')
    assert res.status_code == 200
    j = res.json()
    assert 'rationale' in j
    r = j['rationale']
    assert 'score_breakdown' in r
    assert 'why' in r


def test_admin_tracks_list():
    res = client.get('/v1/admin/tracks')
    assert res.status_code == 200
    j = res.json()
    assert 'rules' in j
    assert isinstance(j['rules'], list)

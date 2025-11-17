from app import app

def test_index_route():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200

def test_get_tasks():
    client = app.test_client()
    res = client.get('/api/tasks')
    assert res.status_code == 200


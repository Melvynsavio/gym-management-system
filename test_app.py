import app

def test_home():
    tester = app.app.test_client()
    response = tester.get('/')
    assert response.status_code == 200

def test_dashboard():
    tester = app.app.test_client()
    response = tester.get('/dashboard')
    assert response.status_code == 200
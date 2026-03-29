class TestRegister:

    def test_register_success(self, client):
        response = client.post('/auth/register', json={
            'username': 'ahmed',
            'email': 'ahmed@test.com',
            'password': 'password123'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['user']['username'] == 'ahmed'

    def test_register_missing_fields(self, client):
        response = client.post('/auth/register', json={
            'username': 'ahmed'
        })
        assert response.status_code == 400

    def test_register_duplicate_email(self, client):
        client.post('/auth/register', json={
            'username': 'user1',
            'email': 'same@test.com',
            'password': 'password123'
        })
        response = client.post('/auth/register', json={
            'username': 'user2',
            'email': 'same@test.com',
            'password': 'password456'
        })
        assert response.status_code == 409

    def test_register_short_password(self, client):
        response = client.post('/auth/register', json={
            'username': 'ahmed',
            'email': 'ahmed@test.com',
            'password': '123'
        })
        assert response.status_code == 400


class TestLogin:

    def test_login_success(self, client):
        client.post('/auth/register', json={
            'username': 'ahmed',
            'email': 'ahmed@test.com',
            'password': 'password123'
        })
        response = client.post('/auth/login', json={
            'email': 'ahmed@test.com',
            'password': 'password123'
        })
        assert response.status_code == 200
        assert 'token' in response.get_json()

    def test_login_wrong_password(self, client):
        client.post('/auth/register', json={
            'username': 'ahmed',
            'email': 'ahmed@test.com',
            'password': 'password123'
        })
        response = client.post('/auth/login', json={
            'email': 'ahmed@test.com',
            'password': 'wrong'
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post('/auth/login', json={
            'email': 'nobody@test.com',
            'password': 'password123'
        })
        assert response.status_code == 401
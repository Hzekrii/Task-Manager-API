class TestCreateTask:

    def test_create_task_success(self, client, auth_header):
        response = client.post('/tasks/', json={
            'title': 'Ma première tâche',
            'description': 'Description test',
            'priority': 'high'
        }, headers=auth_header)
        assert response.status_code == 201
        data = response.get_json()
        assert data['task']['title'] == 'Ma première tâche'
        assert data['task']['status'] == 'todo'

    def test_create_task_no_title(self, client, auth_header):
        response = client.post('/tasks/', json={
            'description': 'Pas de titre'
        }, headers=auth_header)
        assert response.status_code == 400

    def test_create_task_invalid_status(self, client, auth_header):
        response = client.post('/tasks/', json={
            'title': 'Test',
            'status': 'invalid'
        }, headers=auth_header)
        assert response.status_code == 400

    def test_create_task_no_auth(self, client):
        response = client.post('/tasks/', json={
            'title': 'Sans auth'
        })
        assert response.status_code == 401


class TestGetTasks:

    def test_get_empty_list(self, client, auth_header):
        response = client.get('/tasks/', headers=auth_header)
        assert response.status_code == 200
        assert response.get_json()['total'] == 0

    def test_get_tasks_with_data(self, client, auth_header):
        client.post('/tasks/', json={'title': 'T1'}, headers=auth_header)
        client.post('/tasks/', json={'title': 'T2'}, headers=auth_header)
        response = client.get('/tasks/', headers=auth_header)
        assert response.get_json()['total'] == 2

    def test_filter_by_status(self, client, auth_header):
        client.post('/tasks/', json={
            'title': 'Todo', 'status': 'todo'
        }, headers=auth_header)
        client.post('/tasks/', json={
            'title': 'Done', 'status': 'done'
        }, headers=auth_header)
        response = client.get('/tasks/?status=done', headers=auth_header)
        data = response.get_json()
        assert data['total'] == 1
        assert data['tasks'][0]['status'] == 'done'


class TestUpdateTask:

    def test_update_success(self, client, auth_header):
        res = client.post('/tasks/', json={
            'title': 'Avant'
        }, headers=auth_header)
        task_id = res.get_json()['task']['id']

        response = client.put(f'/tasks/{task_id}', json={
            'title': 'Après',
            'status': 'done'
        }, headers=auth_header)
        assert response.status_code == 200
        assert response.get_json()['task']['title'] == 'Après'

    def test_update_not_found(self, client, auth_header):
        response = client.put('/tasks/9999', json={
            'title': 'Nope'
        }, headers=auth_header)
        assert response.status_code == 404


class TestDeleteTask:

    def test_delete_success(self, client, auth_header):
        res = client.post('/tasks/', json={
            'title': 'À supprimer'
        }, headers=auth_header)
        task_id = res.get_json()['task']['id']

        response = client.delete(f'/tasks/{task_id}', headers=auth_header)
        assert response.status_code == 200

        response = client.get(f'/tasks/{task_id}', headers=auth_header)
        assert response.status_code == 404

    def test_delete_not_found(self, client, auth_header):
        response = client.delete('/tasks/9999', headers=auth_header)
        assert response.status_code == 404


class TestTaskStats:

    def test_stats_empty(self, client, auth_header):
        response = client.get('/tasks/stats', headers=auth_header)
        assert response.status_code == 200
        assert response.get_json()['total_tasks'] == 0

    def test_stats_with_data(self, client, auth_header):
        client.post('/tasks/', json={
            'title': 'T1', 'status': 'done'
        }, headers=auth_header)
        client.post('/tasks/', json={
            'title': 'T2', 'status': 'todo'
        }, headers=auth_header)
        response = client.get('/tasks/stats', headers=auth_header)
        data = response.get_json()
        assert data['total_tasks'] == 2
        assert data['completion_rate'] == '50.0%'
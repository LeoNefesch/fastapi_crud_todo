from datetime import datetime
from tests.conftest import client, todo_data, get_first_todo_id


class TestTodo:
    def test_create_todo(self, client):
        """Тест корректности метода post."""
        for todo in todo_data:
            response = client.post("/api/todo", json=todo)
            assert response.status_code == 201
            data = response.json()
            assert data["title"] == todo["title"]
            assert data["is_completed"] == todo["is_completed"]

    def test_get_todos(self, client):
        """Тест корректности метода get для всех записей."""
        response = client.get("/api/todo")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        for todo, response_todo in zip(todo_data, data):
            assert response_todo["title"] == todo["title"]
            assert response_todo["is_completed"] == todo["is_completed"]

    def test_get_todo(self, client, get_first_todo_id):
        """Тест корректности метода get для одной записи."""
        todo_id = get_first_todo_id
        response_by_id = client.get(f"/api/todo/{todo_id}")
        assert response_by_id.status_code == 200
        todo = response_by_id.json()
        assert todo["id"] == todo_id
        assert todo["title"] == todo_data[0]["title"]
        assert todo["is_completed"] == todo_data[0]["is_completed"]

    def test_get_todo_not_found(self, client):
        """Тест корректности метода get при передаче id несуществующей записи."""
        response = client.get("/api/todo/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_patch_todo(self, client, get_first_todo_id):
        """Тест корректности метода patch для одной записи."""
        todo_id = get_first_todo_id
        patch_data = {"title": "Updated Task"}
        patch_response = client.patch(f"/api/todo/{todo_id}", json=patch_data)
        assert patch_response.status_code == 200
        updated_todo = patch_response.json()
        assert updated_todo["id"] == todo_id
        assert updated_todo["title"] == patch_data["title"]
        assert updated_todo["is_completed"] == todo_data[0]["is_completed"]

    def test_update_todo(self, client, get_first_todo_id):
        """Тест корректности метода put для одной записи."""
        todo_id = get_first_todo_id
        update_data = {
            "title": "Updated Task",
            "is_completed": True,
            "created_at": datetime.now().isoformat(),
        }
        response = client.put(f"/api/todo/{todo_id}", json=update_data)
        assert response.status_code == 200
        updated_todo = response.json()
        assert updated_todo["id"] == todo_id
        assert updated_todo["title"] == update_data["title"]
        assert updated_todo["is_completed"] == update_data["is_completed"]

    def test_delete_todo_not_found(self, client):
        """Тест корректности метода delete при передаче id несуществующей записи."""
        response = client.delete("/api/todo/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_delete_todo(self, client, get_first_todo_id):
        """Тест корректности метода delete для одной записи."""
        todo_id = get_first_todo_id
        delete_response = client.delete(f"/api/todo/{todo_id}")
        assert delete_response.status_code == 204
        get_response = client.get(f"/api/todo/{todo_id}")
        assert get_response.status_code == 404
        assert get_response.json()["detail"] == "Todo not found"

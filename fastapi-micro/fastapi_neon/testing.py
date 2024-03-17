from fastapi.testclient import TestClient
from fastapi_neon.main import app
import pytest

client = TestClient(app)

id = 7
in_id = 15

def test_all_todos():
    response = client.get("/todos")
    assert response.status_code == 200

def test_get_todo():
    response = client.get(f"/todos/{id}")
    assert response.status_code == 200

def test_create_todo():
    response = client.post("/todos", json={"description": "Test Todo"})
    assert response.status_code == 200

    
def test_update_todo():
    response = client.put(f"/todos/{id}", json={"description": "Updated Todo"})
    assert response.status_code == 200


def test_delete_todo():
    response = client.delete(f"/todos/{id}")
    assert response.status_code == 200

# Test for invalid id
def test_invalid_get():
    response = client.get(f"/todos/{in_id}")
    assert response.status_code == 404

def test_invalid_update():
    response = client.put(f"/todos/{in_id}", json={"description": "Updated Todo"})
    assert response.status_code == 404

def test_invalid_delete():
    response = client.delete(f"/todos/{in_id}")
    assert response.status_code == 404


from fastapi.testclient import TestClient

def test_find_all(client_fixture: TestClient):
    response = client_fixture.get("/user")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 2

def test_find_by_id_正常系(client_fixture: TestClient):
    response = client_fixture.get("/user/1")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1

def test_find_by_id_異常系(client_fixture: TestClient):
    response = client_fixture.get("/user/3")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."

def test_find_by_name_正常系1(client_fixture: TestClient):
    response = client_fixture.get("/user/?name=Yamada")
    assert response.status_code == 200
    user = response.json()
    assert len(user) == 1
    assert user[0]["last_name"] == "Yamada"

def test_find_by_name_正常系2(client_fixture: TestClient):
    response = client_fixture.get("/user/?name=Ya")
    assert response.status_code == 200
    user = response.json()
    assert len(user) == 1
    assert user[0]["last_name"] == "Yamada"

def test_find_by_name_正常系3(client_fixture: TestClient):
    response = client_fixture.get("/user/?name=ma")
    assert response.status_code == 200
    user = response.json()
    assert len(user) == 1
    assert user[0]["last_name"] == "Yamada"

def test_find_by_name_正常系4(client_fixture: TestClient):
    response = client_fixture.get("/user/?name=da")
    assert response.status_code == 200
    user = response.json()
    assert len(user) == 1
    assert user[0]["last_name"] == "Yamada"

def test_create(client_fixture: TestClient):
    response = client_fixture.post(
        "/user", json={"password": "123abc", "last_name": "Suzuki", "first_name": "Ichiro", "email": "suzuki-ichiro@xxx.co.jp"}
    )
    assert response.status_code == 201
    user = response.json()
    assert user["id"] == 3
    assert user["last_name"] == "Suzuki"
    assert user["first_name"] == "Ichiro"
    assert user["email"] == "suzuki-ichiro@xxx.co.jp"
    assert user["role"] == "Staff"

    response = client_fixture.get("/user")
    assert len(response.json()) == 3

def test_update_正常系(client_fixture: TestClient):
    response = client_fixture.put(
        "/user/2", json={"last_name": "Tanaka", "first_name": "Kenji", "email": "kenji-tanaka@com", "role": "Senior Manager"}
    )
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 2
    assert user["last_name"] == "Tanaka"
    assert user["first_name"] == "Kenji"
    assert user["email"] == "kenji-tanaka@com"
    assert user["role"] == "Senior Manager"

def test_update_異常系1(client_fixture: TestClient):
    response = client_fixture.put(
        "/user/1", json={"last_name": "Tanaka", "first_name": "Kenji", "email": "kenji-tanaka@com", "role": "Senior Manager"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Cannot update yourself."

def test_update_異常系2(client_fixture: TestClient):
    response = client_fixture.put(
        "/user/10", json={"last_name": "Tanaka", "first_name": "Kenji", "email": "kenji-tanaka@com", "role": "Senior Manager"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not updated."

def test_delete_正常系(client_fixture: TestClient):
    response = client_fixture.delete("/user/2")
    assert response.status_code == 200

    response = client_fixture.get("/user")
    assert len(response.json()) == 1

def test_delete_異常系1(client_fixture: TestClient):
    response = client_fixture.delete("/user/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cannot delete yourself."

def test_delete_異常系2(client_fixture: TestClient):
    response = client_fixture.delete("/user/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not deleted."
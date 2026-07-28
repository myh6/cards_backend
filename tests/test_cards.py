def auth_headers(client):
    r1 = client.post("/auth/register",
                json = {"email": "mina@test.com", "password": "secret123"})
    
    assert r1.status_code == 201, f"register failed: {r1.status_code} {r1.text}"
    r = client.post("/auth/login",
                    data = {"username": "mina@test.com", "password": "secret123"})
    
    assert r.status_code == 200, f"login failed: {r.status_code} {r.text}"
    return {"Authorization": "Bearer " + r.json()["access_token"]}

def test_create_card(client):
    h = auth_headers(client=client)
    r = client.post("/cards", headers=h,
                    json = {"member": "Nayeon", "set_name": "Formula of Love"})
    assert r.status_code == 201
    assert r.json()["member"] == "Nayeon"

def test_requires_auth(client):
    assert client.get("/cards").status_code == 401

def test_missing_card_is_404(client):
    h = auth_headers(client=client)
    assert client.get("/cards/999", headers=h).status_code == 404

def test_users_are_isolated(client):
    h1 = auth_headers(client=client)
    client.post("/cards", headers=h1,
                json = {"member": "Sana", "set_name": "With YOU-th"})
    client.post("/auth/register",
                json = {"email": "momo@test.com", "password": "secret123"})
    r = client.post("/auth/login",
                    data={"username": "momo@test.com", "password": "secret123"})
    h2 = {"Authorization": "Bearer " + r.json()["access_token"]}
    assert client.get("/cards", headers=h2).json() == []
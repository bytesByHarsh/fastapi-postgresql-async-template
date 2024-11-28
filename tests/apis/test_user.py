from app.core.config import settings

def test_create_user(client):
    # response = client.get("/api/user/get-users")
    # assert response.status_code == 200
    # assert response.json() == []

    response = client.post(
        "/users/",
        json={
        "user_role": "guest",
        "profile_image_url": "https://www.imageurl.com/profile_image.jpg",
        "name": "Test User",
        "username": "test123",
        "email": "test123@example.com",
        "password": "Str1ngst!"
        },
    )
    assert response.status_code == 201

    # response = client.get(f"/api/user/get-user?id={response.json().get('id')}")
    # assert response.status_code == 200
    # assert response.json() == {
    #     "id": response.json().get("id"),
    #     "email": "test@example.com",
    #     "full_name": "Full Name Test",
    # }

    # response = client.get("/api/user/get-users")
    # assert response.status_code == 200
    # assert len(response.json()) == 1
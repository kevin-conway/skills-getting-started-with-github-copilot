import src.app as app_module


def test_signup_full_activity(client):
    # Arrange: create a tiny activity with max 1 participant
    name = "Tiny Club"
    app_module.activities[name] = {
        "description": "Tiny",
        "schedule": "Now",
        "max_participants": 1,
        "participants": [],
    }

    # Act: sign up first student
    resp1 = client.post(f"/activities/{name}/signup", params={"email": "a@b.com"})

    # Assert: first signup succeeds
    assert resp1.status_code == 200
    assert "a@b.com" in app_module.activities[name]["participants"]

    # Act: sign up second student
    resp2 = client.post(f"/activities/{name}/signup", params={"email": "c@d.com"})

    # Assert: second signup fails because full
    assert resp2.status_code == 400


def test_unregister_nonexistent_activity(client):
    # Act
    resp = client.post("/activities/DefinitelyNotThere/unregister", params={"email": "x@y.com"})

    # Assert
    assert resp.status_code == 404


def test_signup_unregister_and_resign(client):
    # Arrange
    activity = "Chess Club"
    email = "temp@mergington.edu"

    # Act: signup
    resp_signup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp_signup.status_code == 200

    # Act: unregister
    resp_unreg = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp_unreg.status_code == 200

    # Act: signup again
    resp_resign = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: signup allowed again
    assert resp_resign.status_code == 200
    assert email in app_module.activities[activity]["participants"]

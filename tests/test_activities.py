import src.app as app_module

def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_success(client):
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

def test_signup_duplicate(client):
    activity = "Chess Club"
    email = app_module.activities[activity]["participants"][0]
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 400

def test_signup_not_found(client):
    resp = client.post("/activities/NonexistentActivity/signup", params={"email": "a@b.com"})
    assert resp.status_code == 404

def test_unregister_success(client):
    activity = "Chess Club"
    email = app_module.activities[activity]["participants"][0]
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]

def test_unregister_not_signed_up(client):
    activity = "Chess Club"
    email = "not-signed-up@mergington.edu"
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert resp.status_code == 400

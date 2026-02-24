def test_get_activities_returns_data(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_activity in payload
    assert "participants" in payload[expected_activity]


def test_signup_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert email in payload["message"]

    verify = client.get("/activities")
    assert email in verify.json()[activity]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    payload = response.json()
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity = "Astronomy Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    payload = response.json()
    assert payload["detail"] == "Activity not found"


def test_delete_participant_removes_student(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/participants", params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert email in payload["message"]

    verify = client.get("/activities")
    assert email not in verify.json()[activity]["participants"]


def test_delete_unknown_activity_returns_404(client):
    # Arrange
    activity = "Astronomy Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/participants", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    payload = response.json()
    assert payload["detail"] == "Activity not found"


def test_delete_missing_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity}/participants", params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    payload = response.json()
    assert payload["detail"] == "Student not signed up for this activity"

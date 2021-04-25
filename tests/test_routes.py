from app.models import StudentModel

def test_index(client):
    rv = client.get("/index")
    assert rv.status_code == 200


def test_students(client):
    rv = client.get("/students/")
    assert rv.status_code == 200


def test_groups(client):
    rv = client.get("/groups/")
    assert rv.status_code == 200


def test_student(client):
    rv = client.get("/students/1")
    assert rv.status_code == 200




def test_error(client):
    rv = client.get("/student")
    assert rv.status_code == 404


def test_api(client):
    rv = client.get("/api/v1/students/1")
    assert rv.status_code == 200


def test_api2(client):
    rv = client.get("/api/v1/students/1")
    json_data = rv.get_json()
    assert json_data['id'] == 1


def test_api3(client):
    client.post("/api/v1/students/", json={'first_name': 'Jon', 'last_name': 'Snow'})
    rv = client.get("/api/v1/students/", json={'first_name': 'Jon', 'last_name': 'Snow'})
    json_data = rv.get_json()
    assert json_data[0]['first_name'] == 'Jon'
    assert json_data[0]['last_name'] == 'Snow'
    assert json_data[0]['courses'] == []

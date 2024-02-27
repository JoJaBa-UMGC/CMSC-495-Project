def test_load_app(client):
    response = client.get('/')
    print(response.text)
    assert b'Login Page' in response.data

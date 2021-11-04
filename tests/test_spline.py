import pytest
from spline_vs import create_app


@pytest.fixture
def client():
    """
    This fixture Creates flask test client object to make requests
    """
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_spline_annotate_without_image(client):
    """
        Test if no image included in the request,
        would it response with an error response or not
    """
    rv = client.post('/sp/annotate')
    assert rv.status_code == 400
    assert b'No image has been uploaded for spline annotation' in rv.data

def test_spline_annotate_without_tck(client):

    rv = client.post('/sp/annotate',)
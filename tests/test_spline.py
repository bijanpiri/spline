import pytest
import io
from spline_vs import create_app, config
from werkzeug.datastructures import FileStorage
import PIL
from flask import Flask


@pytest.fixture
def client():
    """
    This fixture Creates flask test client object to make requests
    """

    app: Flask = create_app({'TESTING': True})
    app.config.from_object(config)

    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_image():
    """
        Creates a 400x400 JPEG black image to be sent by post requests.
    """
    im = PIL.Image.new(mode='RGB', size=(400, 400), color=(0, 0, 0))
    buffer = io.BytesIO()
    im.save(buffer, format='JPEG')
    buffer.seek(0)
    return FileStorage(buffer, filename='test_pic.jpg', content_type='image/jpeg')


def test_spline_annotate_image_bad_extension(client, mock_image):
    # changed filename extension to non-image format
    mock_image.filename = 'test_pic.txt'
    data = {
        'image': mock_image,
        't': '[100, 200,300,400]',
        'c': '[50,100,80,100]',
        'k': 1
    }
    rv = client.post('/sp/annotate', data=data,
                     content_type='multipart/form-data')

    assert rv.status_code == 400
    assert b'This file extension is not supported.' in rv.data


def test_spline_annotate_image_corrupted_content(client):

    mock_image = FileStorage(io.BytesIO(b'inavlid image content: hahaha...'),
                             filename='test_pic.jpg', content_type='image/jpeg')
    data = {
        'image': mock_image,
        't': '[100, 200,300,400]',
        'c': '[50,100,80,100]',
        'k': 1
    }

    rv = client.post('/sp/annotate', data=data,
                     content_type='multipart/form-data')

    assert rv.status_code == 400

    assert b'Bad image file or corrupted image' in rv.data


def test_spline_annotate_without_image(client):
    """
        Test if no image included in the request,
        would it response with an error response or not
    """
    rv = client.post('/sp/annotate')
    assert rv.status_code == 400
    assert b'No image has been uploaded for spline annotation' in rv.data


@pytest.mark.parametrize("tck,error_msg", [
    ({'c': [1], 'k': 0}, b'Knot points not found'),
    ({'t': [1], 'k': 0}, b'No coefficient has been set'),
    ({'t': [1], 'c': [2]}, b'Degree of spline has not been sent'),
    ({'t': '[,,,,,]', 'c': [2], 'k': 0}, b'Error parsing request parameters'),
    ({'t': [1], 'c': [2], 'k': 'a'}, b'invalid literal for int() '),
    ({'t': '[110, 125, 150, 200, 320, 420, 550, 610]', 'c': '[12, 1,  10]',
     'k': 2}, b'Knots, coefficients and degree are inconsistent'),
    ({'t': '[110, 125, 150]', 'c': '[12, 1, 13, 2, 10]',
     'k': 2}, b'Need at least 6 knots for degree 2'),

])
def test_spline_annotate_bad_tck(client, mock_image, tck, error_msg):

    data = {
        'image': mock_image,
        **tck
    }

    rv = client.post('/sp/annotate', data=data,
                     content_type='multipart/form-data')

    assert rv.status_code == 400
    assert error_msg in rv.data

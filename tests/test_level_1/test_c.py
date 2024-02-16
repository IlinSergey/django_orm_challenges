from unittest.mock import patch

import pytest

from challenges.views.level_1.b_book_details import get_book
from challenges.views.level_1.c_delete_book import delete_book


@pytest.mark.django_db
def test__delete_book_handler__success(client, create_book):
    with (
        patch('challenges.views.level_1.c_delete_book.delete_book') as delete_book_mock,
        patch('challenges.views.level_1.c_delete_book.get_book') as get_book_mock,
    ):
        get_book_mock.return_value = create_book
        delete_book_mock.return_value = None
        response = client.post('/book/1/delete/')
        assert response.status_code == 200


def test__delete_book_handler__not_found(client):
    with patch('challenges.views.level_1.c_delete_book.get_book') as get_book_mock:
        get_book_mock.return_value = None
        response = client.post('/book/1/delete/')
        assert response.status_code == 404


def test__delete_book_handler__not_allowed(client):
    response = client.get('/book/1/delete/')
    assert response.status_code == 405


@pytest.mark.django_db
def test__delete_book(create_book):
    book = create_book
    result = get_book(book_id=1)
    assert result == book
    delete_book(book_id=1)
    result = get_book(book_id=1)
    assert result is None

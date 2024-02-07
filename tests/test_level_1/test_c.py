from unittest.mock import patch

import pytest

from challenges.models import Book
from challenges.views.level_1.b_book_details import get_book
from challenges.views.level_1.c_delete_book import delete_book


def test__delete_book_handler__success(client):
    with (
        patch('challenges.views.level_1.c_delete_book.delete_book') as delete_book_mock,
        patch('challenges.views.level_1.c_delete_book.get_book') as get_book_mock,
    ):
        get_book_mock.return_value = Book(id=1, title='test', author_full_name='test', isbn='test')
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
def test__delete_book():
    book = Book.objects.create(title='test title', author_full_name='test name', isbn='test isbn')
    result = get_book(book_id=1)
    assert result == book
    delete_book(book_id=1)
    result = get_book(book_id=1)
    assert result is None

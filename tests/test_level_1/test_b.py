from unittest.mock import patch

import pytest

from challenges.models import Book
from challenges.views.level_1.b_book_details import get_book


def test__book_details_handler__success(client):
    with patch('challenges.views.level_1.b_book_details.get_book') as mock:
        mock.return_value = Book(id=1, title='test', author_full_name='test', isbn='test')
        response = client.get('/book/1/')
        assert response.status_code == 200
        assert response.json() == {
            'id': 1,
            'title': 'test',
            'author_full_name': 'test',
            'isbn': 'test',
        }


def test__book_details_handler__failure(client):
    with patch('challenges.views.level_1.b_book_details.get_book') as mock:
        mock.return_value = None
        response = client.get('/book/2/')
        assert response.status_code == 404


@pytest.mark.django_db
def test__get_book():
    book = Book.objects.create(title='test title', author_full_name='test name', isbn='test isbn')
    result = get_book(book_id=1)
    assert result == book
    empty_result = get_book(book_id=2)
    assert empty_result is None

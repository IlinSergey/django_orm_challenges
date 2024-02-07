from unittest.mock import patch

import pytest

from challenges.models import Book
from challenges.views.level_1.b_book_details import get_book
from challenges.views.level_1.d_update_book import update_book


def test__update_book_handler__success(client):
    with patch('challenges.views.level_1.d_update_book.update_book') as update_book_mock:
        update_book_mock.return_value = Book(id=1, title='new title', author_full_name='new name', isbn='new isbn')
        response = client.post('/book/1/update/', data={
            'title': 'new title',
            'author_full_name': 'new name',
            'isbn': 'new isbn',
        })
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "title": "new title",
            "author_full_name": "new name",
            "isbn": "new isbn",
        }


def test__update_book_handler__not_found(client):
    with patch('challenges.views.level_1.d_update_book.update_book') as update_book_mock:
        update_book_mock.return_value = None
        response = client.post('/book/333/update/', data={
            'title': 'new title',
            'author_full_name': 'new name',
            'isbn': 'new isbn',
        })
        assert response.status_code == 400


def test__update_book_handler__missing_parameters(client):
    response = client.post('/book/1/update/', data={
        'title': 'new title',
    })
    assert response.status_code == 400
    assert response.content == b'One of required parameters are missing'


@pytest.mark.django_db
def test__update_book():
    book = Book.objects.create(title='test title', author_full_name='test name', isbn='test isbn')
    result = get_book(book_id=1)
    assert result == book
    new_book = update_book(
        book_id=1,
        new_title='new title',
        new_author_full_name='new name',
        new_isbn='new isbn',
    )
    assert new_book.title == 'new title'
    assert new_book.author_full_name == 'new name'
    assert new_book.isbn == 'new isbn'

    check_new_book = get_book(book_id=1)
    assert check_new_book == new_book

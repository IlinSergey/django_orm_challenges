from unittest.mock import patch

import pytest

from challenges.models import Book


@pytest.mark.django_db
def test__create_book_handler__success(client, create_book):
    with patch('challenges.views.level_1.a_create_book.create_book') as mock:
        mock.return_value = create_book
        response = client.post('/book/create/', {'title': 'test title',
                                                 'author_full_name': 'test name',
                                                 'isbn': 'test isbn',
                                                 })
        assert response.status_code == 200
        assert response.json() == {
            'id': 1,
            'title': 'test title',
            'author_full_name': 'test name',
            'isbn': 'test isbn',
        }


def test__create_book_handler__missing_parameters(client):
    response = client.post('/book/create/', {'title': 'test', 'author_full_name': 'test'})
    assert response.status_code == 400
    assert response.content == b'One of required parameters are missing'


@pytest.mark.django_db
def test__create_book(create_book):
    book = create_book
    assert book.pk == 1
    assert book.title == 'test title'
    assert book.author_full_name == 'test name'
    assert book.isbn == 'test isbn'

    saved_book = Book.objects.get(pk=1)
    assert saved_book == book

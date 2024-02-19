from unittest.mock import patch

import pytest

from challenges.views.level_1.b_book_details import get_book


@pytest.mark.django_db
def test__book_details_handler__success(client, create_book):
    with patch('challenges.views.level_1.b_book_details.get_book') as mock:
        mock.return_value = create_book
        response = client.get('/book/1/')
        assert response.status_code == 200
        assert response.json() == {
            'id': 1,
            'title': 'test title',
            'author_full_name': 'test name',
            'isbn': 'test isbn',
        }


def test__book_details_handler__failure(client):
    with patch('challenges.views.level_1.b_book_details.get_book') as mock:
        mock.return_value = None
        response = client.get('/book/2/')
        assert response.status_code == 404


@pytest.mark.django_db
def test__get_book(create_book):
    book = create_book
    result = get_book(book_id=1)
    assert result == book
    empty_result = get_book(book_id=2)
    assert empty_result is None

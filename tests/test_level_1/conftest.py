import pytest

from challenges.models import Book


@pytest.fixture(scope='function')
def create_book() -> Book:
    book = Book.objects.create(
        title='test title',
        author_full_name='test name',
        isbn='test isbn',
        )
    return book

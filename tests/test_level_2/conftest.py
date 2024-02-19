import pytest

from challenges.models import Laptop, Post


@pytest.fixture
def create_laptops():
    laptops = [
        Laptop.objects.create(brand='HP', year=2019, ram=4, hdd=64, price=10, quantity=2),
        Laptop.objects.create(brand='Apple', year=2020, ram=8, hdd=128, price=1000, quantity=1),
        Laptop.objects.create(brand='Asus', year=2021, ram=16, hdd=256, price=2000, quantity=2),
        Laptop.objects.create(brand='HP', year=2022, ram=32, hdd=512, price=3000, quantity=3),
        Laptop.objects.create(brand='Lenovo', year=2023, ram=64, hdd=1024, price=4000, quantity=4),
        Laptop.objects.create(brand='Asus', year=2024, ram=128, hdd=2048, price=5000, quantity=0),
        Laptop.objects.create(brand='Apple', year=2024, ram=256, hdd=4096, price=6000, quantity=5),
        Laptop.objects.create(brand='Asus', year=2025, ram=512, hdd=8192, price=7000, quantity=0),
    ]
    yield laptops
    Laptop.objects.all().delete()


@pytest.fixture
def create_last_laptop():
    yield Laptop.objects.create(brand='Asus', year=2025, ram=512, hdd=8192, price=7000, quantity=1)
    Laptop.objects.all().delete()


@pytest.fixture
def create_posts():
    posts = [
        Post.objects.create(title='test title 1', text='test text 1', author='test author 1',
                            category='news', status='published'),
        Post.objects.create(title='test title 2', text='test text 2', author='test author 2',
                            category='travel', status='draft'),
        Post.objects.create(title='test title 3', text='test text 3', author='test author 3',
                            category='food', status='ban'),
        Post.objects.create(title='test title 4', text='test text 4', author='test author 4',
                            category='travel', status='published'),
        Post.objects.create(title='test title 5', text='test text 5', author='test author 5',
                            category='music', status='ban'),
        Post.objects.create(title='test title 6', text='test text 6', author='test author 6',
                            status='published'),
        Post.objects.create(title='test title 7', text='test text 7', author='test author 7',
                            status='draft'),

    ]
    yield posts
    Post.objects.all().delete()

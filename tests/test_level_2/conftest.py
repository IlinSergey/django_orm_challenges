import pytest

from challenges.models import Laptop


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

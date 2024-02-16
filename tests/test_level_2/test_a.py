import pytest


class TestLaptopDetailView():

    @pytest.mark.parametrize('_id, brand, year, ram, hdd, price, quantity', [
        (1, 'HP', 2019, 4, 64, '10.00', 2),
        (2, 'Apple', 2020, 8, 128, '1000.00', 1),
        (3, 'Asus', 2021, 16, 256, '2000.00', 2),
    ])
    @pytest.mark.django_db
    def test__laptop_details_view__success(self, client, _id, brand, year, ram, hdd, price,
                                           quantity, create_laptops):
        response = client.get(f'/laptops/{_id}/')
        assert response.status_code == 200
        assert response.json() == {
            'brand': brand,
            'year': year,
            'ram': ram,
            'hdd': hdd,
            'price': price,
            'quantity': quantity,
        }

    @pytest.mark.django_db
    def test__laptop_details_view__not_found(self, client):
        response = client.get('/laptops/100/')
        assert response.status_code == 404

    def test__laptop_details_view__not_allowed(self, client):
        response = client.post('/laptops/1/')
        assert response.status_code == 405


class TestLaptopInStockListView():

    @pytest.mark.django_db
    def test__laptop_in_stock_list_view__success(self, client, create_laptops):
        response = client.get('/laptops/in-stock/')
        assert response.status_code == 200
        assert len(response.json()) == 6

    def test__laptop_in_stock_list_view__not_allowed(self, client):
        response = client.post('/laptops/in-stock/')
        assert response.status_code == 405


class TestLaptopFilterView():

    @pytest.mark.parametrize('brand, min_price, _len', [
        ('HP', '10.00', 2),
        ('Apple', '1000.00', 2),
        ('Asus', '5000.00', 2),
    ])
    @pytest.mark.django_db
    def test__laptop_filter_view__success(self, client, brand, min_price, _len, create_laptops):
        response = client.get('/laptops/', data={
            'brand': brand,
            'min_price': min_price,
        })
        assert response.status_code == 200
        assert len(response.json()) == _len

    @pytest.mark.parametrize('brand, min_price', [
        (' ', '10.00'),
        ('Dexp', '10.00'),
        ('Apple', 'price')
    ])
    def test__laptop_filter_view__forbidden(self, client, brand, min_price):
        response = client.get('/laptops/', data={
            'brand': brand,
            'min_price': min_price,
        })
        assert response.status_code == 403

    def test__laptop_filter_view__no_brand(self, client):
        response = client.get('/laptops/', data={
            'min_price': '10.00',
        })
        assert response.status_code == 403

    def test__laptop_filter_view__not_allowed(self, client):
        response = client.post('/laptops/')
        assert response.status_code == 405


class TestLastLaptopDetailView():

    @pytest.mark.django_db
    def test__last_laptop_details_view__success(self, client, create_laptops, create_last_laptop):
        response = client.get('/laptops/last/')
        assert response.status_code == 200
        assert response.json() == {
            'brand': 'Asus',
            'year': 2025,
            'ram': 512,
            'hdd': 8192,
            'price': '7000.00',
            'quantity': 1,
        }

    @pytest.mark.django_db
    def test__last_laptop_details_view__not_found(self, client):
        response = client.get('/laptops/last/')
        assert response.status_code == 404

    def test__last_laptop_details_view__not_allowed(self, client):
        response = client.post('/laptops/last/')
        assert response.status_code == 405

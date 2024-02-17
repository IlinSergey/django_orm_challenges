import datetime

import pytest

from challenges.models import Post


class TestLastsPostListView():

    @pytest.mark.django_db
    def test__last_posts_list_view__success(self, client, create_posts):
        response = client.get('/posts/latest/')
        assert response.status_code == 200
        assert len(response.json()) == 3

    @pytest.mark.django_db
    def test__last_posts_list_view__success_no_posts(self, client):
        response = client.get('/posts/latest/')
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test__last_posts_list_view__not_allowed(self, client):
        response = client.post('/posts/latest/')
        assert response.status_code == 405


class TestPostsSearchView():

    @pytest.mark.parametrize('query, _len', [
        ('1', 1),
        ('2', 1),
        ('test', 7),

    ])
    @pytest.mark.django_db
    def test__posts_search_view__success(self, client, query, _len, create_posts):
        response = client.get('/posts/search/', data={
            'query': query,
        })
        assert response.status_code == 200
        assert len(response.json()) == _len

    def test__posts_search_view__missing_query(self, client):
        response = client.get('/posts/search/')
        assert response.status_code == 403

    def test__posts_search_view__not_allowed(self, client):
        response = client.post('/posts/search/')
        assert response.status_code == 405


class TestUntaggetPostsListView():

    @pytest.mark.django_db
    def test__untagged_posts_list_view__success(self, client, create_posts):
        response = client.get('/posts/untagged/')
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]['author'] == 'test author 6'

    @pytest.mark.django_db
    def test__untagged_posts_list_view__no_posts(self, client):
        response = client.get('/posts/untagged/')
        assert response.status_code == 404

    def test__untagged_posts_list_view__not_allowed(self, client):
        response = client.post('/posts/untagged/')
        assert response.status_code == 405


class TestCategoriesPostsListView():

    @pytest.mark.parametrize('categories, _len', [
        ('travel', 2),
        ('food,news', 2),
        ('food', 1),
    ])
    @pytest.mark.django_db
    def test__categories_posts_list_view__success(self, client, categories, _len, create_posts):
        response = client.get('/posts/by-categories/', data={
            'categories': categories
        })
        assert response.status_code == 200
        assert len(response.json()) == _len

    def test__categories_posts_list_view__missing_categories(self, client):
        response = client.get('/posts/by-categories/')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test__categories_posts_list_view__not_str_categories(self, client):
        response = client.get('/posts/by-categories/', data={
            'categories': {'key': 'value'}
        })
        assert response.status_code == 404

    def test__categories_posts_list_view__not_allowed(self, client):
        response = client.post('/posts/by-categories/')
        assert response.status_code == 405


class TestLastDaysPostsView():

    @pytest.mark.django_db
    def test__last_days_posts_list_view__success(self, client, create_posts):
        post_1 = Post.objects.get(pk=1)
        post_1.created_at = datetime.datetime.now() - datetime.timedelta(days=10)
        post_1.save()
        response = client.get('/posts/last-published/', data={
            'last_days': 8
        })
        assert response.status_code == 200
        assert len(response.json()) == 6
        assert post_1.to_json() not in response.json()

    def test__last_days_posts_list_view__not_correct_query(self, client):
        response = client.get('/posts/last-published/', data={
            'last_days': 'test'
        })
        assert response.status_code == 403

    def test__last_days_posts_list_view__missing_query(self, client):
        response = client.get('/posts/last-published/')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test__last_days_posts_list_view__no_posts(self, client):
        response = client.get('/posts/last-published/', data={
            'last_days': 10
        })
        assert response.status_code == 404

    def test__last_days_posts_list_view__not_allowed(self, client):
        response = client.post('/posts/last-published/')
        assert response.status_code == 405

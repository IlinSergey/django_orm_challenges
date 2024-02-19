"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст,
имя автора, статус (опубликован/не опубликован/забанен), дата создания, дата публикации,
категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими постами для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект поста
 в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работы в браузере
"""
import datetime

from django.db.models import Q
from django.http import (HttpRequest, HttpResponse, HttpResponseNotAllowed,
                         JsonResponse)
from django.shortcuts import get_list_or_404

from challenges.models import Post


def last_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    if request.method == "GET":
        last_posts = Post.objects.filter(status="published")[:3]
        last_three_posts_json_list = [post.to_json() for post in last_posts]
        return JsonResponse(last_three_posts_json_list, safe=False)
    return HttpResponseNotAllowed(["GET"])


def posts_search_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    if request.method == "GET":
        query = request.GET.get('query', None)
        if query is not None:
            posts = get_list_or_404(Post.objects.filter(
                Q(title__icontains=query) | Q(text__icontains=query)
                ))
            posts_json_list = [post.to_json() for post in posts]
            return JsonResponse(posts_json_list, safe=False)
        else:
            return HttpResponse(status=403)
    return HttpResponseNotAllowed(["GET"])


def untagged_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    if request.method == "GET":
        posts = get_list_or_404(Post.objects.filter(category__isnull=True).order_by('author', 'created_at'))
        posts_json_list = [post.to_json() for post in posts]
        return JsonResponse(posts_json_list, safe=False)
    return HttpResponseNotAllowed(["GET"])


def categories_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    if request.method == "GET":
        categories = request.GET.get('categories', None)
        if categories is not None:
            category_list = categories.split(',')
            posts = get_list_or_404(Post.objects.filter(category__in=category_list))
            posts_json_list = [post.to_json() for post in posts]
            return JsonResponse(posts_json_list, safe=False)
        else:
            return HttpResponse(status=403)
    return HttpResponseNotAllowed(["GET"])


def last_days_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    if request.method == "GET":
        last_days = request.GET.get('last_days', None)
        if last_days is not None:
            try:
                start_date = datetime.datetime.now() - datetime.timedelta(days=int(last_days))
            except ValueError:
                return HttpResponse(status=403)
            posts = get_list_or_404(Post.objects.filter(created_at__gte=start_date))
            posts_json_list = [post.to_json() for post in posts]
            return JsonResponse(posts_json_list, safe=False)
        else:
            return HttpResponse(status=403)
    return HttpResponseNotAllowed(["GET"])

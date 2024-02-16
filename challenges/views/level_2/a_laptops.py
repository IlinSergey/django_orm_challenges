"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
- реализовать у модели метод to_json, который будет преобразовывать объект ноутбука в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import (HttpRequest, HttpResponse, HttpResponseNotAllowed,
                         JsonResponse)
from django.shortcuts import get_list_or_404, get_object_or_404

from challenges.models import Laptop
from challenges.views.level_2.utils import brand_and_price_validator


def laptop_details_view(request: HttpRequest, laptop_id: int) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    laptop = get_object_or_404(Laptop, pk=laptop_id)
    laptop = laptop.to_json()
    return JsonResponse(laptop)


def laptop_in_stock_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    laptops = get_list_or_404(Laptop.objects.order_by('-created_at'), quantity__gt=0)
    laptops_json_list = [laptop.to_json() for laptop in laptops]
    return JsonResponse(laptops_json_list, safe=False)


def laptop_filter_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    brand = request.GET.get('brand', None)
    min_price = request.GET.get('min_price', None)
    if brand is not None and min_price is not None:
        min_price = float(min_price)
        check = brand_and_price_validator(brand, min_price)
        if check:
            laptops = get_list_or_404(Laptop.objects.order_by('price'), brand=brand, price__gte=min_price)
            laptops_json_list = [laptop.to_json() for laptop in laptops]
            return JsonResponse(laptops_json_list, safe=False)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=403)


def last_laptop_details_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    try:
        laptop = Laptop.objects.order_by('-created_at').first()
        laptop = laptop.to_json()
        return JsonResponse(laptop)
    except Laptop.DoesNotExist:
        return HttpResponse(status=404)

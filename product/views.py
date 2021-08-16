from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, \
    CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from product.models import Product, ProductReview
from product.permissions import IsAuthorOrIsAdmin
from product.serializers import (ProductSerializer, ProductDetailsSerializer,
                                 CreateProductSerializer, ReviewSerializer)


# def test_view(request):
#     return HttpResponse('Hello World!')

#
# @api_view(['GET'])
# def products_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)
#
# class ProductsListView(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
#
# class ProductsListView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ProductDetailsView(RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailsSerializer
#
#
# class CreateProductView(CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer
#
#
# class UpdateProductView(UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer
#
#
# class DeleteProductView(DestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    # def create(self, request, *args, **kwargs):
    #     if not (request.user.is_authenticated and request.user.is_staff):
    #         return Response('Создавать продукты может только админ',
    #                         status=403)
    #     data = request.data
    #     serializer = self.get_serializer(data=data,
    #                                      context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data, status=201)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        elif self.action == 'retrieve':
            return ProductDetailsSerializer
        return CreateProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []

    #api/v1/products/id
    #api/v1/products/id/reviews/
    @action(['GET'], detail=True)
    def reviews(self, request, pk=None):
        product = self.get_object()
        # reviews = ProductReview.objects.filter(product=product)
        reviews = product.reviews.all()
        # [review1, review2]
        serializer = ReviewSerializer(reviews, many=True)
        # [{}, {}]
        return Response(serializer.data, status=200)


# CRUD(Create,  Retrieve,    Update,     Delete)
#        POST     GET      PUT, PATCH    DELETE


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrIsAdmin()]
        return []


#TODO: ViewSet для отзывов, листинг будет в товарах, деталей нет
#TODO: Пагинация (разбивка листинга на страницы)
#TODO: Фильтрация
#TODO: Поиск продуктов по названию и описанию
#TODO: ограничение количества запросов
#TODO: тесты
#TODO: Отзывы
#TODO: Разобрать взаимодействие

# REST - архитектурный подход
# 1. Модель клиент - сервер
# 2. Отсутствие состояния
# 3. Кэширование
# 4. Единообразие интерфейса
# 1. определение ресурсов
# URI ('api/v1/products/1/')

# 2. управление ресурсом через представление
# 3. самодостаточные сообщения
# 4. гипермедиа
# 5. Слои
# 6. Код по требованию
#
# 'GET',    'POST',     'PUT',     'PATCH',            'DELETE'
# list       create     update     partial_update       destroy
# retrieve


# API (Application Programming Interface)
# паттерн MVC

# Product.objects.all() - выдаёт весь список объектов модели
# SELECT * FROM product;

# Product.objects.create() - создаёт новый объект
# INSERT INTO product ...

# Product.objects.update() - обновляет выбранные объекты
# UPDATE product ...;

# Product.objects.delete() - удаляет объекты
# DELETE FROM product;

# Product.objects.filter(условие)
# SELECT * FROM product WHERE условие;

# Операции сравнения
# "="
# Product.objects.filter(price=10000)
# SELECT * FROM product WHERE price = 10000;

# ">"
# Product.objects.filter(price__gt=10000)
# SELECT * FROM product WHERE price > 10000;

# "<"
# Product.objects.filter(price__lt=10000)
# SELECT * FROM product WHERE price < 10000;

# ">="
# Product.objects.filter(price__gte=10000)
# SELECT * FROM product WHERE price >= 10000;

# "<="
# Product.objects.filter(price__lte=10000)
# SELECT * FROM product WHERE price <= 10000;

# BETWEEN
# Product.objects.filter(price__range=[50000, 80000])
# SELECT * FROM product WHERE price BETWEEN 50000 AND 80000;

# IN
# Product.objects.filter(price__in=[50000, 80000])
# SELECT * FROM product WHERE price IN (50000, 80000);

# LIKE
# ILIKE

# 'work%'
# Product.objects.filter(title__startswith='Apple')
# SELECT * FROM product WHERE title LIKE 'Apple%';
# Product.objects.filter(title__istartswith='Apple')
# SELECT * FROM product WHERE title ILIKE 'Apple%';

# '%work'
# Product.objects.filter(title__endswith='GB')
# SELECT * FROM product WHERE title LIKE '%GB';

# Product.objects.filter(title__iendswith='GB')
# SELECT * FROM product WHERE title ILIKE '%GB';

# '%work%'
# Product.objects.filter(title__contains='Samsung')
# SELECT * FROM product WHERE title LIKE '%Samsung%';
# Product.objects.filter(title__icontains='Samsung')
# SELECT * FROM product WHERE title ILIKE '%Samsung%';

# 'work'
# Product.objects.filter(title__exact='Apple Iphone 12')
# # SELECT * FROM product WHERE title LIKE 'Apple Iphone 12';
# Product.objects.filter(title__iexact='Apple Iphone 12')
# # SELECT * FROM product WHERE title ILIKE 'Apple Iphone 12';

# ORDER BY

# Product.objects.order_by('price')
# SELECT * FROM product ORDER BY price ASC;

# Product.objects.order_by('-price')
# SELECT * FROM product ORDER BY price DESC;

# Product.objects.order_by('-price', 'title')
# SELECT * FROM product ORDER BY price DESC, title ASC;

# LIMIT
# Product.objects.all()[:2]
# SELECT * FROM product LIMIT 2;

# Product.objects.all()[3:6]
# SELECT * FROM product LIMIT 3 OFFSET 3;

# Product.objects.first()
# SELECT * FROM product LIMIT 1;


# get(условие) - возвращает один объект

# Product.objects.get(id=1)
# SELECT * FROM product WHERE id=1;

# DoesNotExist - возникает, если не найден ни один объект
# MultipleObjectsReturned - возникает, когда найдено больше одного
# объекта

# count() - возвращает количество результатов

# Product.objects.count()
# SELECT COUNT(*) FROM product;

# Product.objects.filter(...).count()
# SELECT COUNT(*) FROM product WHERE ...;

# exclude()
# Product.objects.filter(price__gt=10000)
# SELECT * FROM product WHERE price > 10000;

# Product.objects.exclude(price__gt=10000)
# SELECT * FROM product WHERE NOT price > 10000;

# QuerySet - список объектов модели

# HTTP методы ("GET", "POST", "PUT", "PATCH", 'DELETE")
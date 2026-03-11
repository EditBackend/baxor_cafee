from rest_framework import viewsets
from .models import Table, Product, Category
from .serializer import TableSerializer, ProductSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @api_view(['GET'])
    def category_list(request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Category bo'yicha filter qilish
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category')
        if category_id:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
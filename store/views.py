from django.db.models import Count
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from .models import Product, Collection, OrderItem, Review


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            return Product.objects.filter(collection_id=collection_id)
        return Product.objects.all()

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'can not delete this product'}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(self, request, *args, **kwargs)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('products')).all()
    serializer_class = CollectionSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

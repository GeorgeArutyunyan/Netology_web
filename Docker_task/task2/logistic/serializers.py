from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']



class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']

class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'adress', 'products', 'positions']

    def create(self, validated_data):

        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for item in positions:
            StockProduct.objects.create(
                stock=stock,
                product=item.get('product'),
                quantity=item.get('quantity'),
                price=item.get('price')
            )
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for item in positions:
            StockProduct.ojbects.update_or_create(
                product=item.get('product'),
                quantity=item.get('quantity'),
                defaults={'price': item.get['price'],
                         'quantity': item.get['quantity']}
            )
        return stock

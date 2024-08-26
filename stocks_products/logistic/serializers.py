from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']


    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions_data = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = Stock.objects.create(**validated_data)

        for position_data in positions_data:
            StockProduct.objects.create(
                stock = stock,
                product = position_data['product'],
                quantity = position_data['quantity'],
                price = position_data['price'])

        return stock


    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions_data = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        for position_data in positions_data:
            StockProduct.objects.update_or_create(
                stock = stock,
                product = position_data['product'],
                defaults={
                    'quantity': position_data['quantity'],
                    'price': position_data['price']
                })

        return stock

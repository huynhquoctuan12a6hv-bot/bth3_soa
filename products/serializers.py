
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Giá sản phẩm không được âm."
            )
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Số lượng không được âm."
            )
        return value

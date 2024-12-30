from rest_framework import serializers
from .models import BusinessUser, Offer, Category, Product, Order, OrderProduct


class BusinessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUser
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = '__all__'


class OrderProductNestedSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.product_name')

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'product_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    business_user_name = serializers.ReadOnlyField(source='business_user.company_name')
    order_products = OrderProductNestedSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'business_user', 'business_user_name', 'order_date', 'total_price',
            'billing_address', 'status', 'order_type', 'order_products'
        ]

    def create(self, validated_data):
        order_products_data = validated_data.pop('order_products', [])
        # Automatically associate the order with the BusinessUser from the request user
        business_user = validated_data['business_user']
        total_price = validated_data['total_price']

        # Create the Order instance
        order = Order.objects.create(**validated_data)

        # Add associated OrderProducts
        for product_data in order_products_data:
            product = product_data.get('product')
            quantity = product_data.get('quantity')
            price = product_data.get('price')
            total = price * quantity

            OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                total=total
            )

        # Apply cashback if the referral code is "leafcoin"
        cashback = 0
        if business_user.referral_code == "leafcoin":
            cashback = total_price * 0.05
            business_user.cashback_amount += cashback
            business_user.save()

        # Track the cashback applied in the order (optional, for auditing)
        order.cashback_applied = cashback
        order.save()

        return order

from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import BusinessUser, Offer, Category, Product, Order, OrderProduct
from .serializers import (
    BusinessUserSerializer, OfferSerializer, CategorySerializer,
    ProductSerializer, OrderSerializer, OrderProductNestedSerializer
)


class BusinessUserViewSet(viewsets.ModelViewSet):
    queryset = BusinessUser.objects.all()
    serializer_class = BusinessUserSerializer
    
    
class BusinessUserOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    @action(detail=False, methods=['post'], url_path='create-order')
    def create_order(self, request):
        # Ensure the logged-in user is a BusinessUser
        if not hasattr(request.user, 'businessuser'):
            return Response({"error": "You must be a BusinessUser to create an order."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the 'business_user' to the logged-in user
        data = request.data
        data['business_user'] = request.user.businessuser.id  # Associate with logged-in business user

        # Serialize and validate the order data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            # Save the order
            order = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductNestedSerializer

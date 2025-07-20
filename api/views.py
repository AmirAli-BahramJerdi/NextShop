from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import *
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny





# Api view app account

class UserCreateApiView(generics.GenericAPIView, CreateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':'user created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginUserApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLoginSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user_serializer = UserLoginSerializer(data=request.data)
        print(request.data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user:
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'user not found'}, status=status.HTTP_400_BAD_REQUEST)




class EditUserApiView(generics.GenericAPIView, UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = UserEditSerializer

    def put(self, request, pk=None, *args, **kwargs):
        instance = User.objects.get(id=pk)
        username = instance.username
        print(username)
        serializer = UserEditSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'success', 'username': username}, status=status.HTTP_200_OK)
        return Response(request, username, *args, **kwargs)



class ProfileApiView(generics.GenericAPIView, RetrieveModelMixin):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        return Profile.objects.filter(user__profile=self.request.user)




class AddressApiView(generics.GenericAPIView, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'success': 'address successfully created!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)




class AddressListApiView(generics.GenericAPIView, ListModelMixin):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        return Address.objects.filter(user__address=self.request.user)




class UserListApiView(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserDetailApiView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ---------------------------------------------------------------------------------------------

# Api view app main

class NewsletterApiView(generics.GenericAPIView, CreateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = NewsletterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':'email successfully registered!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------------------

# Api view app products

class ReviewApiView(generics.GenericAPIView, CreateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def create(self, request, *args, **kwargs):
        product_id = self.kwargs.get('id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            return Response({'success': 'Comment successfully created!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class WishlistApiView(generics.GenericAPIView, CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer
    queryset = Wishlist.objects.all()
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'wishlist successfully created!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = Wishlist.objects.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        wishlist_id = kwargs.get('id')
        try:
            wishlist_item = Wishlist.objects.get(id=wishlist_id, user=request.user)
            wishlist_item.delete()
            return Response({'success': 'product successfully deleted!'}, status=status.HTTP_200_OK)
        except Wishlist.DoesNotExist:
            return Response({'error': 'wishlist item not found.'}, status=status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------------------------------------------------------

# Api view app cart

class AddToCartView(generics.GenericAPIView, CreateModelMixin):
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            product = get_object_or_404(Product, id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items, created = CartItem.objects.get_or_create(cart=cart, product=product, quantity=quantity)
            if created:
                cart_items.quantity = quantity # مقداردهی اولیه
            else:
                cart_items.quantity += quantity  # اضافه کردن به مقدار فعلی
            cart_items.save()
            print(cart_items)
            return Response({'success': 'Product by successfully added to cart!'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Product not Found or Invalid Request!'})



class RemoveFromCartView(APIView):
    def delete(self, request, product_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()
        return Response({'message': 'Product removed from cart successfully!'}, status=status.HTTP_200_OK)



class CartDetail(RetrieveAPIView):
    serializer_class = CartSerializer()
    def get_object(self):
        return get_object_or_404(Cart, user=self.request.user)

# --------------------------------------------------------------------------------------------------------

# Api view app order

class OrderApiView(generics.GenericAPIView, CreateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order_instance = serializer.save(buyer=request.user)  # ذخیره سفارش اصلی
            items = request.data.get("items", [])  # دریافت لیست آیتم‌های سفارش از داده‌های درخواست
            for item in items:
                item_serializer = OrderItemSerializer(data={**item, "order": order_instance.id})
                if item_serializer.is_valid():
                    item_data = item_serializer.validated_data
                    item_serializer.save(order=order_instance, product=item_data['product'],
                                            quantity=item_data['quantity'], price=item_data['price'])
                    item_serializer.save()
                    print(item_serializer)
                else:
                    return Response({'error': 'Invalid request, order not created'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': 'order by successfully created!'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Order creation failed'}, status=status.HTTP_400_BAD_REQUEST)



class OrderListApiView(generics.GenericAPIView, ListModelMixin):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()



class PaymentApiView(generics.GenericAPIView, CreateModelMixin, ListModelMixin):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)





from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from apps.products.models import Category, Product, Review, Wishlist, ProductImage
from apps.main.models import Banner, PromoBanner, Feature, Newsletter
from apps.cart.models import Cart, CartItem
from apps.accounts.models import Profile, Address
from apps.orders.models import Order, OrderItem, Payment
from rest_framework import serializers




# serializers account

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'is_active', 'is_staff', 'is_superuser']



class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        email = attrs.get('email')
        if not email:
            raise serializers.ValidationError({'email': 'ایمیل اجباری است!'})

        if not email.endswith('@gmail.com'):
            raise serializers.ValidationError({'email': 'ایمیل مجاز نیست! لطفا یک ایمیل دیگر وارد کنید.'})
        return attrs

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'],
                    first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        print(user)
        if not user:
            raise serializers.ValidationError('نام کاربری یا رمز عبور نادرست است')
        return {'user': user}



class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'phone', 'address', 'postal_code', 'city', 'avatar']




class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['id', 'is_default']

    def create(self, validated_data):
        address = Address(title=validated_data['title'], recipient_name=validated_data['recipient_name'],
                          phone=validated_data['phone'], address=validated_data['address'],
                          postal_code=validated_data['postal_code'], city=validated_data['city'],
                          address_type=validated_data['address_type'])
        address.save()
        return address



class LogoutSerializer(serializers.Serializer):
    confirm_logout = serializers.BooleanField(label='logout', required=True)


# ----------------------------------------------------------
# serializers main

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'subtitle', 'description', 'image', 'button_text', 'button_link', 'is_active', 'created_at']
        read_only_fields = ['id', 'is_active', 'created_at']



class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title', 'description', 'icon', 'order']
        read_only_fields = ['id']



class PromoBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoBanner
        fields = ['id', 'title', 'subtitle', 'description', 'image', 'button_text', 'button_link', 'end_date', 'is_active']
        read_only_fields = ['id', 'end_date', 'is_active']



class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id', 'email', 'is_active', 'created_at']
        read_only_fields = ['id', 'is_active', 'created_at']

    def create(self, validated_data):
        news_letter = Newsletter(email=validated_data['email'])
        news_letter.save()
        return news_letter



# ---------------------------------------------------------------------------------------

# serializers product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'image', 'parent', 'is_featured', 'product_count']
        read_only_fields = ['slug', 'product_count']



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']



class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = [
            'id', 'slug', 'sold', 'rating', 'rating_count', 'created_at',
            'updated_at', 'images', 'category_detail', 'discount_percentage'
        ]

    def get_discount_percentage(self, obj):
        # فراخوانی متد get_discount_percentage از مدل Product
        return obj.get_discount_percentage()



class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at', 'user_username', 'product_name']
        read_only_fields = ['id', 'created_at', 'user_username', 'product_name']
        extra_kwargs = {
            'product': {'write_only': True},
            'user': {'write_only': True}
        }



class WishlistSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'created_at', 'user_username', 'product_name']
        read_only_fields = ['id', 'created_at', 'user_username', 'product_name']
        extra_kwargs = {
            'product': {'write_only': True},
            'user': {'write_only': True}
        }


# -------------------------------------------------------------------------------------

# serializers cart

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity']
        read_only_fields = ['id', 'cart']



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'session_id', 'created_at', 'updated_at']



class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=0)


# -------------------------------------------------------------------------------------------

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'user', 'payment_id', 'tracking_code', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        order = Order(full_name=validated_data['full_name'], email=validated_data['email'],phone=validated_data['phone'],
                      address=validated_data['address'], postal_code=validated_data['postal_code'],
                      city=validated_data['city'], notes=validated_data['notes'])
        order.save()
        return order



class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'price', 'quantity', 'total_price']
        read_only_fields = ['order', 'product']

    def get_total_price(self, obj):
        return obj.total_price



class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    amount_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'amount', 'amount_formatted',
            'transaction_id', 'payment_method', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def get_amount_formatted(self, obj):
        return f"{obj.amount:,}تومان"












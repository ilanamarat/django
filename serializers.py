from rest_framework import serializers
from main.models import *

class AddressSerializer(serializers.Serializer):
  country = serializers.CharField(max_length=100)
  city = serializers.CharField(max_length=50)
  apartment_address = serializers.CharField(max_length=100)
  zip = serializers.CharField(max_length=50)


class UserSerializer(serializers.Serializer):
  name = serializers.CharField( max_length=100)
  login = serializers.CharField(max_length=50)
  gender = serializers.CharField()
  
  # inheritance
  address = AddressSerializer()


class CategorySerializer(serializers.ModelSerializer):
  class Meta: 
    model = Books
    fields = '__all__'
  # name = serializers.CharField(max_length=200)

class OrderItemSerializer(serializers.ModelSerializer):
  # inheritance
  storage_address= AddressSerializer()
  # inheritance
  user = UserSerializer()

  class Meta: 
    model = OrderItem
    fields = '__all__'

class SellItemsSerializer(serializers.ModelSerializer):
  # title = serializers.CharField(max_length=100)
  # price = serializers.FloatField()
  # description = serializers.CharField(max_length=500)
  # image = serializers.ImageField()
  # # inheritance
  # category = CategorySerializer()
  class Meta: 
    model = Electronics
    fields = '__all__'

class BasketSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  items = SellItemsSerializer()
  class Meta: 
    model = Basket
    fields = '__all__'
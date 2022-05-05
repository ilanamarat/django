from rest_framework import serializers
from authentication.serializers import UserSerializer
from core.models import *

class AddressSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=50)
    apartment_address = serializers.CharField(max_length=100)
    zip = serializers.CharField(max_length=50)


class FileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = FileModel
        fields = '__all__'

class ItemSerializer(FileSerializer):
    storage_address= AddressSerializer()

class ElectronicsSerializer(ItemSerializer):
    
    class Meta: 
        model = Electronics
        fields = '__all__'

class BooksSerializer(ItemSerializer):
    id=serializers.FloatField()
    title = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    description = serializers.CharField(max_length=500)
    author= serializers.CharField(max_length=200)
    page_number= serializers.IntegerField()
    publisher = serializers.CharField(max_length=300)
    

class SportItemsSerializer(ItemSerializer):

    class Meta: 
        model = SportItems
        fields = '__all__'

# class SellItemsSerializer(serializers.ModelSerializer):
#     # title = serializers.CharField(max_length=100)
#     # price = serializers.FloatField()
#     # description = serializers.CharField(max_length=500)
#     # image = serializers.ImageField()
#     # # inheritance
#     # category = CategorySerializer()
#     class Meta: 
#         model = Electronics
#         fields = '__all__'

class BasketSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    books = BooksSerializer()
    sport_items= SportItemsSerializer()
    electronics = ElectronicsSerializer()
    class Meta: 
        model = Basket
        fields = '__all__' 
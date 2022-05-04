from ast import Return
import json
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from authentication.models import User
from authentication.serializers import UserSerializer
from core.models import Basket, Books, Electronics, FileModel, SportItems, Address
from core.serializers import AddressSerializer, BasketSerializer, BooksSerializer, ElectronicsSerializer, FileSerializer, SportItemsSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser,AllowAny
# Create your views here.
@api_view(['GET', 'DELETE'])
def electronics_list(request):
    if request.method == 'GET':
        items = Electronics.objects.all()
        serializer = ElectronicsSerializer(items, many = True)
        return JsonResponse(serializer.data, safe=False)
    

@api_view(['GET'])
def book_list(request):
    if request.method == 'GET':
        books = Books.objects.all()
        serializer = BooksSerializer(books, many = True)
        return JsonResponse(serializer.data, safe=False)
    # elif request.method == 'PUT':
    #     # data = json.loads(request.body)
    #     # book = Books.objects.create(**data)
    #     # return JsonResponse(book.to_json_detail())
    #     data = json.loads(request.body)
    #     book = Books.objects.create(**data)
    #     return JsonResponse({'created': True},safe=False,)
    # return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BooksDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        item = Books.objects.filter(id=kwargs.get('pk')).first()
        serializer = BooksSerializer(item)
        if item:
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse({'message': 'Item not found'}, status=404)

    def put(self, *args, **kwargs):
        item = Books.objects.filter(id=kwargs.get('pk')).first()
        
        if item:
            data = json.loads(self.request.body)
            item.title = data.get('title', item.title)
            item.price = data.get('price', item.price)
            item.description = data.get('description', item.description)
            item.page_number = data.get('page_number', item.page_number)
            item.publisher = data.get('publisher', item.publisher)
            item.save()
            serializer = BooksSerializer(item)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse({'message': 'Book not found'}, status=404)

    def delete(self, request, *args, **kwargs):
        item = Books.objects.filter(id=kwargs.get('pk')).first()
        if item:
            item.delete()
            return JsonResponse('', safe=False, status=204)
        return JsonResponse({'message': 'Book not found'}, status=404)

class ElectronicsDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        item = Electronics.objects.filter(id=kwargs.get('pk')).first()
        serializer = ElectronicsSerializer(item)
        if item:
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse({'message': 'Item not found'}, status=404)

    def put(self, *args, **kwargs):
        item = Electronics.objects.filter(id=kwargs.get('pk')).first()
        
        if item:
            data = json.loads(self.request.body)
            item.title = data.get('title', item.title)
            item.price = data.get('price', item.price)
            item.description = data.get('description', item.description)
            item.manufacturer = data.get('manufacturer', item.manufacturer)
            item.save()
            serializer = ElectronicsSerializer(item)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse({'message': 'Book not found'}, status=404)

    def delete(self, request, *args, **kwargs):
        electronics = Electronics.objects.filter(id=kwargs.get('pk')).first()
        if electronics:
            electronics.delete()
            return JsonResponse('', safe=False, status=204)
        return JsonResponse({'message': 'electronics not found'}, status=404)

class SportItemsListView(APIView):
    def get(self, request, *args, **kwargs):
        items = SportItems.objects.all()
        serializer = SportItemsSerializer(items, many = True)
        return JsonResponse(serializer.data, safe=False)

    # def post(self, request, *args, **kwargs):
    #     data = json.loads(self.request.body)
    #     serializer = SportItemsSerializer(data=request.data)
    #     item = SportItems.objects.create(**data)
    #     item.save()
    #     return JsonResponse({'created': True},safe=False,)

class SportItemDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        item = SportItems.objects.filter(id=kwargs.get('pk')).first()
        serializer = SportItemsSerializer(item)
        if item:
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse({'message': 'Item not found'}, status=404)

    def put(self, *args, **kwargs):
        item = SportItems.objects.filter(id=kwargs.get('pk')).first()
        
        if item:
            data = json.loads(self.request.body)
            item.title = data.get('title', item.title)
            item.price = data.get('price', item.price)
            item.description = data.get('description', item.description)
            item.manufacturer = data.get('manufacturer', item.manufacturer)
            item.size = data.get('size', item.size)
            item.save()
            serializer = SportItemsSerializer(item)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse({'message': 'item not found'}, status=404)

    def delete(self, request, *args, **kwargs):
        item = SportItems.objects.filter(id=kwargs.get('pk')).first()
        if item:
            item.delete()
            return JsonResponse('', safe=False, status=204)
        return JsonResponse({'message': 'item not found'}, status=404)

class BasketViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def list(self, request):
        queryset = Basket.items.get_by_user(request.user.id)
        serializer = BasketSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    
class BasketBooksViewSet(viewsets.ViewSet):
    # serializer_class = BooksSerializer
    # queryset = Basket.objects.only('books')
    permission_classes = (IsAuthenticated,)
    def list(self, request):
        queryset = Basket.items.get_by_user(request.user.id).values('books','user')
        # serializer = BasketSerializer(queryset, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return Response(queryset)

class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAdminUser,)
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

class FileModelViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)
    def list(self, request):
        queryset = FileModel.objects.all()
        serializer = FileSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAdminUser,)
    def list(self, request):
        queryset = Address.objects.all()
        serializer = AddressSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

class ItemViewSet(GenericViewSet):
    permission_classes = (IsAdminUser,)
    def list(self, request, *args, **kwargs):
        queryset = Books.objects.all()
        serializer = BooksSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def create(self, *args, **kwargs):
        data = json.loads(self.request.body)
        serializer = BooksSerializer(data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer)
        return JsonResponse(serializer.data, safe= False)

    def destroy(self, request):
        item = self.get_object()
        item.delete()
        return JsonResponse({"deleted":True}, safe= False)
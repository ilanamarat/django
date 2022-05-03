from rest_framework import status
import json
from django.shortcuts import redirect, render
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from main.forms import CategoryForm, SellItemForm
from main.models import *
from rest_framework import viewsets
from main.serializers import BasketSerializer, CategorySerializer, OrderItemSerializer, UserSerializer,SellItemsSerializer
# Create your views here.

def home(request):
  return render(request, 'main/index.html')

@api_view(['GET'])
def order_items(request):
  if request.method == 'GET':
    items = OrderItem.objects.all()
    serializer = OrderItemSerializer(items, many=True)
    return JsonResponse(serializer.data, safe=False)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  def list(self, request):
    queryset = UserProfile.objects.all()
    serializer = UserSerializer(queryset, many = True)
    return render(request, 'main/users.html', {'users':json.loads(json.dumps(serializer.data))})

@api_view(['GET','POST'])
def items(request):
  error = ''
  if request.method == 'GET':
    items = Books.objects.all()
    serializer = SellItemsSerializer(items, many=True)
    # return JsonResponse(items, safe=False)
    form = SellItemForm()
    context = {
      'form':form,
      'error':error,
      'items':json.loads(json.dumps(serializer.data))
    }
    return render(request, 'main/items.html', context)
  
  
  if request.method == 'POST':
    form = SellItemsSerializer(data=request.data)
    if form.is_valid():
      form.save()
      return redirect('/items/')
    else:
      error = 'Incorrect values are entered!'

  form = SellItemForm()
  context = {
    'form':form,
    'error':error
  }
  return render(request, 'main/items.html', context)


class BasketView(APIView):
  def get_object(self, id):
    try:
      return Basket.objects.get(id=id)
    except Basket.DoesNotExist:
      raise Http404

  def get(self, request):
    items = Basket.objects.all()
    serializer = BasketSerializer(items, many=True)
    data=json.loads(json.dumps(serializer.data))
    return render(request, 'main/basket.html', {'items':data})
  
  def delete(self, request, id):
    item = self.get_object(id)
    item.delete()
    items = Basket.objects.all()
    serializer = BasketSerializer(items, many=True)
    return render(request, 'main/basket.html', {'items':json.loads(json.dumps(serializer.data))})

@api_view(['GET','POST'])
def create(request):
  error = ''
  if request.method == 'POST':
    form = CategorySerializer(data=request.data)
    if form.is_valid():
      form.save()
      return redirect('/')
    else:
      error = 'Incorrect values are entered!'


  form = CategoryForm()
  serializer = CategorySerializer( many = True)
  context = {
    'form':form,
    'error':error,
    'categories':json.loads(json.dumps(serializer.data))
  }
  return render(request, 'main/category.html', context)


class Item_detail(APIView):
  def get(self, request,id):
    item = self.get_object(id)
    serializer = SellItemsSerializer(item)
    return render(request, 'main/item_details.html', {'item':json.loads(json.dumps(serializer.data))})
  
  def post(self, request, id):
    item = self.get_object(id)
    item.delete()
    items = Books.objects.all()
    serializer = SellItemsSerializer(items, many=True)
    return render(request, 'main/index.html', {'items':json.loads(json.dumps(serializer.data))})


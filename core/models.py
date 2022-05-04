from django.db import models
from authentication.models import User
# Create your models here.

POSITION_CATEGORY=(
  ('U', 'User'),
  ('M', 'Manager'), 
)
GADGETS_CATEGORY = (
  ('HP','Headphones'),
  ('PH','Phones'),
  ('AC','Accessories'),
  ('TV','Television'),
  ('UN','Undefined')
)

FILE_FORMAT=(
    ('IMG', 'Image'),
    ('FL', 'File'),
    ('UN', 'Undefined')
)

class ItemsManager(models.Manager):
    def sortedUp(self):
        return self.get_queryset().only('price')

    def sortedDown(self):
        return self.get_queryset().order_by('-price')
    
class BasketManager(models.Manager):
    def get_related_books(self):
        return self.select_related('books')
    def get_by_user(self, user_id):
        return self.filter(user_id = user_id)
    def get_books(self):
        return self.get_queryset().only("books")
        # return self.select_related('books').filter(user_id=user_id)
    def get_electronics(self):
        return self.select_related('user','electronics')
    def get_sport_items(self):
        return self.select_related('user','sport_items')

class AddressManager(models.Manager):
    def sorted(self):
        return self.get_queryset().order_by('country')

class CategoryManager(models.Manager):
    def get_phones(self):
        return self.get_queryset().filter(category='PH')
    def get_tv(self):
        return self.get_queryset().filter(category = 'TV')
    def get_accessories(self):
        return self.get_queryset().filter(category = 'AC')

class Address(models.Model):
    country = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=50,null=True, blank=True)
    apartment_address = models.CharField(max_length=100,null=True, blank=True)
    zip = models.CharField(max_length=50,null=True, blank=True)

    objects = models.Manager()
    addresses = AddressManager()
    class Meta:
        verbose_name_plural= 'Адресы'
        verbose_name = 'Адрес'
    def __str__(self):
        return self.country

class FileModel(models.Model):
    filename  = models.CharField(choices=GADGETS_CATEGORY, max_length=2, default='UN' )
    file = models.FileField(upload_to='images',null=True, blank=True)
    file_format = models.CharField(choices=FILE_FORMAT, default='UN', max_length=3)

class Item(models.Model):
    title = models.CharField(max_length=100, default='No title', null=True, blank=True)
    price = models.FloatField(default=0,null=True, blank=True)
    description = models.TextField(default = 'no description',null=True, blank=True)
    storage_address= models.ForeignKey(Address, on_delete=models.PROTECT,null=True, blank=True)
    image = models.ForeignKey(FileModel, on_delete=models.PROTECT, null=True, blank=True)
    objects = models.Manager()
    items = ItemsManager()
    def __str__(self):
        return self.title
    class Meta:
        abstract= True

class Electronics(Item):
    category = models.CharField(choices=GADGETS_CATEGORY, max_length=2, default='UN' )
    manufacturer = models.TextField(max_length=300, null=True, blank=True)
    
    objects = models.Manager()
    items = CategoryManager()

    class Meta:
        verbose_name_plural= 'Электроники'
        verbose_name = 'Электроника'

class Books(Item):
    author= models.TextField(max_length=200,null=True, blank=True)
    page_number= models.IntegerField(null=True, blank=True)
    publisher = models.TextField(max_length=300, null=True, blank=True)
    items = ItemsManager()
    class Meta:
        verbose_name_plural= 'Книги'
        verbose_name = 'Книга'
    def to_json(self):
        return{
            'price':self.price,
            'title':self.title
        }

class SportItems(Item):
    manufacturer = models.TextField(max_length=200,null=True, blank=True)
    size = models.CharField(max_length=10,null=True, blank=True)
    class Meta:
        verbose_name_plural= 'Спортивный инвентарь'
        verbose_name = 'Спортивный инвентарь'

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    books =models.ForeignKey(Books, on_delete=models.CASCADE,null=True, blank=True)
    electronics =models.ForeignKey(Electronics, on_delete=models.CASCADE,null=True, blank=True)
    sport_items =models.ForeignKey(SportItems, on_delete=models.CASCADE,null=True, blank=True)
    
    objects = models.Manager()
    items = BasketManager()
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural= 'Корзины'
        verbose_name = 'Корзина'

# class OrderItem(models.Model):
#   item = models.ForeignKey(Item, on_delete=models.CASCADE,null=True, blank=True)
#   user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True, blank=True)
#   quantity = models.IntegerField(default=1,null=True, blank=True)

#   def __str__(self):
#     return self.item.title
#   class Meta:
#     abstract= True


# class Order(OrderItem):
#   delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE)
#   items = models.ManyToManyField(OrderItem)
#   ordered = models.BooleanField(default=False)
#   ordered_date = models.DateTimeField()
#   received = models.BooleanField(default=False)
#   received_date= models.DateTimeField()

#   objects = models.Manager()
#   orders = OrderManager()
#   def __str__(self):
#     return self.id

#   class Meta:
#     verbose_name_plural= 'Orders'
#     verbose_name = 'Order'
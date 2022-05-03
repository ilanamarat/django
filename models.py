from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
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

class PeopleCountManager(models.Manager):
  def males(self):
    return self.get_queryset().filter(gender='M')

  def females(self):
    return self.get_queryset().filter(gender='F')
  
class ItemsManager(models.Manager):
  def sortedUp(self):
    return self.get_queryset().order_by('price')
  
  def sortedDown(self):
    return self.get_queryset().order_by('-price')

class AddressManager(models.Manager):
  def sorted(self):
    return self.get_queryset().order_by('country')

class OrderManager(models.Manager):
  def receivedItems(self):
    return self.get_queryset().filter(received=True)
  def sentItems(self):
    return self.get_queryset().filter(received=False)
  def get_total_item_price(self):
    return self.quantity * self.item.item.price
  

class Address(models.Model):
  country = models.CharField(max_length=100,null=True, blank=True)
  city = models.CharField(max_length=50,null=True, blank=True)
  apartment_address = models.CharField(max_length=100,null=True, blank=True)
  zip = models.CharField(max_length=50,null=True, blank=True)
  
  objects = models.Manager()
  addresses = AddressManager()
  class Meta:
    verbose_name_plural= 'Addresses'
  def __str__(self):
    return self.country

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True,related_name='profile')
  address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True, blank=True)
  category = models.CharField(choices=POSITION_CATEGORY, max_length=1, default='U')
  
  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
    if created:
      UserProfile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
  
  objects = models.Manager()
  people = PeopleCountManager()

  def __str__(self):
    return self.user.username

class Item(models.Model):
  title = models.CharField(max_length=100, default='No title', null=True, blank=True)
  price = models.FloatField(default=0,null=True, blank=True)
  description = models.TextField(default = 'no description',null=True, blank=True)
  image = models.ImageField(upload_to='images',null=True, blank=True)
  storage_address= models.ForeignKey(Address, on_delete=models.CASCADE,null=True, blank=True)

  objects = models.Manager()
  items = ItemsManager()
  def __str__(self):
    return self.title
  class Meta:
    abstract= True
  
class Electronics(Item):
  category = models.CharField(choices=GADGETS_CATEGORY, max_length=2, default='UN' )

class Books(Item):
  author= models.TextField(max_length=200,null=True, blank=True)

class SportItems(Item):
  size = models.CharField(max_length=10,null=True, blank=True)

class OrderItem(models.Model):
  item = models.ForeignKey(Item, on_delete=models.CASCADE,null=True, blank=True)
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True, blank=True)
  quantity = models.IntegerField(default=1,null=True, blank=True)

  def __str__(self):
    return self.item.title
  class Meta:
    abstract= True


class Order(OrderItem):
  delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE)
  ordered = models.BooleanField(default=False)
  ordered_date = models.DateTimeField()
  received = models.BooleanField(default=False)
  received_date= models.DateTimeField()
  
  objects = models.Manager()
  orders = OrderManager()
  def __str__(self):
    return self.id
  

class Basket(models.Model):
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True, blank=True)
  items = models.ManyToManyField(Item)
  def __str__(self):
    return self.user.user.username
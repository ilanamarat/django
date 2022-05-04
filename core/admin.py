from django.contrib import admin


from .models import Address, Basket, Books, Electronics, FileModel, SportItems  

admin.site.register(Books)
admin.site.register(Address)
admin.site.register(FileModel)
admin.site.register(Electronics)
admin.site.register(SportItems)
admin.site.register(Basket)

# django
Made for Backend Django course

Detailed information about the structure of the project with the class  diagram is in "E-commerce websie.pdf" file.



This is a website that works as a platform where users can see, edit, add and delete products to the basket. JWT Authentication is used.

**Website has models:**
Address
User
FileModel
Item(abstract)
Electronics(Inherited from Item)
Books(Inherited from Item)
SportItems(Inherited from Item)
Basket
**Model Managers:**
ItemsManager
BasketManager
AddressManager
CategoryManager
UserManager
**Connection between models(Foreign Key):**
Address in Item
Image in Item
User in Basket
Books in Basket
Electronics in Basket
SportItems in Basket
**Serializers:**
**serializer.ModelSerializer:**
FileSerializer
ElectronicsSerializer(AddressSerializer, FileSerializer)
SportItemsSerializer(AddressSerializer, FileSerializer)
BasketSerializer(UserSerializer, BooksSerializer, SportItemsSerializer, ElectronicsSerializer)
**serializer.Serializer:**
AddressSerializer
BooksSerializer(AddressSerializer, FileSerializer)
UserSerializer
**Views:
Function Based View(FBV):**
electronics_list
book_list
**Class Based View(CBV):**
BooksDetailView
ElectronicsDetailView
SportItemsListView
SportItemDetailView
**ViewSets:**
AccountViewSet
BasketViewSet
BasketBooksViewSet
FileModelViewSet
AddressViewSet
ItemViewSet

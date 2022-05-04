from django.urls import path

from core.views import AccountViewSet, AddressViewSet, BasketBooksViewSet, BasketViewSet, BooksDetailView, ElectronicsDetailView, FileModelViewSet, ItemViewSet, SportItemDetailView, SportItemsListView, book_list, electronics_list
urlpatterns = [
    path('books/', book_list),
    path('books/<int:pk>/', BooksDetailView.as_view()),
    path('electronics/', electronics_list),
    path('electronics/<int:pk>/',ElectronicsDetailView.as_view()),
    path('sport-items/', SportItemsListView.as_view()),
    path('sport-items/<int:pk>/',SportItemDetailView.as_view()),
    path('basket/', BasketViewSet.as_view({'get':'list'})),
    path('basket/books/', BasketBooksViewSet.as_view({'get':'list'})),
    path('admin/books/', ItemViewSet.as_view({'get':'list'})),
    path('admin/accounts/', AccountViewSet.as_view({'get':'list'})),
    path('admin/files/', FileModelViewSet.as_view({'get':'list'})),
    path('admin/addresses/', AddressViewSet.as_view({'get':'list'})),

    # path('admin/books/', ItemViewSet.as_view({'delete':'destroy'})),
]
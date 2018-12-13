from django.conf.urls import url
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse, path
from QuanLyNhaSach.views import customer
from QuanLyNhaSach.views import merchandise, supplier
from django.contrib.auth import views

app_name = 'QuanLyNhaSach'


def logout_view(request):
    logout(request)
    return redirect(reverse('QuanLyNhaSach:index'))


urlpatterns = [
    path('', customer.CustomerListView.as_view(), name='index'),
    path('logout/', logout_view, name='logout'),

    path('customers/', customer.CustomerListView.as_view(), name='customers'),
    path('customers/add/', customer.CustomerAddView.as_view(), name='customers-add'),
    path('customers/<int:id>/', customer.CustomerUpdateView.as_view(), name='customers-update'),
    path('customers-type/', customer.CustomerTypeListView.as_view(), name='customers-type'),
    path('customers-type/add/', customer.CustomerTypeAddView.as_view(), name='customers-type-add'),
    path('customers-type/<int:id>/', customer.CustomerTypeUpdateView.as_view(), name='customers-type-update'),

    path('books/', merchandise.BookListView.as_view(), name='books'),
    path('books/add/', merchandise.BookAddView.as_view(), name='books-add'),
    path('books/<int:id>/', merchandise.BookUpdateView.as_view(), name='books-update'),
    path('books-type/', merchandise.BookTypeListView.as_view(), name='books-type'),
    path('books-type/add/', merchandise.BookTypeAddView.as_view(), name='books-type-add'),
    path('books-type/<int:id>/', merchandise.BookTypeUpdateView.as_view(), name='books-type-update'),
    path('stationeries/', merchandise.StationeryListView.as_view(), name='stationeries'),
    path('stationeries/add/', merchandise.StationeryAddView.as_view(), name='stationeries-add'),
    path('stationeries/<int:id>/', merchandise.StationeryUpdateView.as_view(), name='stationeries-update'),
    path('stationeries-type/', merchandise.StationeryTypeListView.as_view(), name='stationeries-type'),
    path('stationeries-type/add/', merchandise.StationeryTypeAddView.as_view(), name='stationeries-type-add'),
    path('stationeries-type/<int:id>/', merchandise.StationeryTypeUpdateView.as_view(),
         name='stationeries-type-update'),

    path('suppliers/', supplier.SupplierListView.as_view(), name='suppliers'),
    path('suppliers/add/', supplier.SupplierAddView.as_view(), name='suppliers-add'),
    path('suppliers/<int:id>/', supplier.SupplierUpdateView.as_view(), name='suppliers-update'),

]

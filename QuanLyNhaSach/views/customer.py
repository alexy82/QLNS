from django.shortcuts import reverse, get_object_or_404, render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from QuanLyNhaSach.serializers.customer import CustomerTypeSerializer, CustomerSerializer
from QuanLyNhaSach.models.customer import Customer, CustomerType
from QuanLyNhaSach.views.base import BaseITSAdminView, BaseAPIView
from QuanLyNhaSach.models.stock_transfer_out import StockTransferOut
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class CustomerListView(BaseITSAdminView):
    def __init__(self):
        super(CustomerListView, self).__init__()
        self.template_name = 'pages/customer_list.html'
        self.set_context_data(customer_type=CustomerType.objects.all())


class CustomerAddView(BaseITSAdminView):
    def __init__(self):
        super(CustomerAddView, self).__init__()
        self.template_name = 'pages/customer_detail.html'
        self.set_context_data(action='Add', url='/api/customers/', btn_content='Create')


class CustomerUpdateView(BaseITSAdminView):
    def __init__(self):
        super(CustomerUpdateView, self).__init__()
        self.template_name = 'pages/customer_detail.html'
        self.set_context_data(action='Update', btn_content='Save')

    def get(self, request, id, **params):
        customer = get_object_or_404(Customer, pk=id)
        self.extra.update({"customer": customer,
                           "url": '/api/customers/{}/'.format(id),
                           "note_out_list": StockTransferOut.objects.filter(customer__id=id)}
                          )
        params.update(self.extra)
        return render(request, self.template_name, params)


class CustomerTypeAddView(BaseITSAdminView):
    def __init__(self):
        super(CustomerTypeAddView, self).__init__()
        self.template_name = 'pages/customer_type_detail.html'
        self.set_context_data(action='Add', url='/api/customers-type/', btn_content='Create')


class CustomerTypeUpdateView(BaseITSAdminView):
    def __init__(self):
        super(CustomerTypeUpdateView, self).__init__()
        self.template_name = 'pages/customer_type_detail.html'
        self.set_context_data(action='Update', btn_content='Save')

    def get(self, request, id, **params):
        _type = get_object_or_404(CustomerType, pk=id)
        self.extra.update({"type": _type,
                           "url": '/api/customers-type/{}/'.format(id)})
        params.update(self.extra)
        return render(request, self.template_name, params)


class CustomerTypeListView(BaseITSAdminView):
    def __init__(self):
        super(CustomerTypeListView, self).__init__()
        self.template_name = 'pages/customer_type_list.html'


class Auth(BaseAPIView):
    """
    Check in stock of products by products SKU
    """
    http_method_names = ['post']

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"Invalid username or password"}, status=404)
        customer = Customer.objects.filter(user_id=user.id).first()
        if customer is None:
            return Response({"Invalid username or password"}, status=404)
        response = {
            'data': customer.as_dict(),
        }
        headers = {
            'charset': self.charset,
        }
        return Response(response, content_type=self.content_type, headers=headers)


class Customers(BaseAPIView):
    http_method_names = ['post']

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        name = data.get('name', None)
        phone = data.get('phone', None)
        email = data.get('email', "")
        address = data.get('address', "")
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"username is existed"}, status=409)
        user = User.objects.create_user(username=username, password=password)
        customer = Customer.objects.create(name=name, phone=phone, email=email, address=address, user_id=user.id)
        response = {
            'data': customer.as_dict(),
        }
        headers = {
            'charset': self.charset,
        }
        return Response(response, content_type=self.content_type, headers=headers)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerTypeViewSet(ModelViewSet):
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer

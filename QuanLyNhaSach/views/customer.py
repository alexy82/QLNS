from django.shortcuts import reverse, get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from QuanLyNhaSach.serializers.customer import CustomerTypeSerializer, CustomerSerializer
from QuanLyNhaSach.models.customer import Customer, CustomerType
from QuanLyNhaSach.views.base import BaseITSAdminView


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
                           "url": '/api/customers/{}/'.format(id)})
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


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerTypeViewSet(ModelViewSet):
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer

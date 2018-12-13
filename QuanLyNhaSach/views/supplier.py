from datetime import datetime
from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from QuanLyNhaSach.serializers.supplier import SupplierSerializer
from QuanLyNhaSach.models.supplier import Supplier
from QuanLyNhaSach.views.base import BaseITSAdminView


class SupplierListView(BaseITSAdminView):
    def __init__(self):
        super(SupplierListView, self).__init__()
        self.template_name = 'pages/supplier_list.html'


class SupplierAddView(BaseITSAdminView):
    def __init__(self):
        super(SupplierAddView, self).__init__()
        self.template_name = 'pages/supplier_detail.html'
        self.set_context_data(action='Add', url='/api/suppliers/', btn_content='Create')


class SupplierUpdateView(BaseITSAdminView):
    def __init__(self):
        super(SupplierUpdateView, self).__init__()
        self.template_name = 'pages/supplier_detail.html'
        self.set_context_data(action='Update', btn_content='Save')

    def get(self, request, id, **params):
        supplier = get_object_or_404(Supplier, pk=id)
        self.extra.update({"supplier": supplier,
                           "url": '/api/suppliers/{}/'.format(id)})
        params.update(self.extra)
        return render(request, self.template_name, params)


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

import json
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from django.shortcuts import get_object_or_404, render
from datetime import datetime
from QuanLyNhaSach.serializers.stock_transfer_in import StockTransferInDetailSerializer, StockTransferInSerializer
from QuanLyNhaSach.models.stock_transfer_in import StockTransferInDetail, StockTransferIn
from QuanLyNhaSach.models.merchandise import Merchandise
from QuanLyNhaSach.models.supplier import Supplier
from QuanLyNhaSach.views.base import BaseITSAdminView
from QLNS.middleware import get_current_user


class StockTransferInListView(BaseITSAdminView):
    def __init__(self):
        super(StockTransferInListView, self).__init__()
        self.template_name = 'pages/stock_transfer_in.html'
        self.set_context_data(supplier_list=Supplier.objects.all(), user_list=User.objects.all())


class StockTransferInAddView(BaseITSAdminView):
    def __init__(self):
        super(StockTransferInAddView, self).__init__()
        self.template_name = 'pages/stock_transfer_in_detail.html'
        self.set_context_data(books=Merchandise.objects.filter(merchandise_type=1),
                              stationeries=Merchandise.objects.filter(merchandise_type=0),
                              suppliers=Supplier.objects.all())


class StockTransferInDetailView(BaseITSAdminView):
    def __init__(self):
        super(StockTransferInDetailView, self).__init__()
        self.template_name = 'pages/stock_transfer_in_detail.html'

    def get(self, request, id, **params):
        note = get_object_or_404(StockTransferIn, pk=id)
        self.extra.update({"note": note,
                           "note_details": StockTransferInDetail.objects.filter(inside=note)})
        params.update(self.extra)
        return render(request, self.template_name, params)


"""
Phiếu nhập kho:
+Thêm
Tồn kho tăng lên
+Xóa
Tồn kho giảm xuống
+Sửa 
Tồn kho có thể giảm xuống hoặc tăng lên
"""


class StockTransferInViewSet(ModelViewSet):
    queryset = StockTransferIn.objects.all()
    serializer_class = StockTransferInSerializer

    def create(self, request, *args, **kwargs):
        data = request.POST.dict()
        data['created_by'] = get_current_user().id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(created_at=datetime.now())


class StockTransferInDetailViewSet(ModelViewSet):
    queryset = StockTransferInDetail.objects.all()
    serializer_class = StockTransferInDetailSerializer

    def create(self, request, *args, **kwargs):
        data = request.POST.get("items")
        data = json.loads(data)
        for item in data:
            id_unit = item['unit']
            unit = Merchandise.objects.get(pk=id_unit)
            unit.available_count += item['count']
            unit.save()

        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()

    def perform_update(self, serializer):
        if serializer.is_valid():
            id_detail = self.request.POST['id']
            detail = StockTransferInDetail.objects.get(pk=id_detail)
            old_unit = detail.unit
            old_unit.available_count -= detail.count
            old_unit.save()
            id_unit = self.request.POST['unit']
            unit = Merchandise.objects.get(pk=id_unit)
            unit.available_count += int(self.request.POST['count'])
            unit.save()
            if detail.unit_id != id_unit:
                price = unit.price
                serializer.save(price=price)
            else:
                serializer.save()

    def perform_destroy(self, instance):
        unit = Merchandise.objects.get(pk=instance.pk)
        unit -= instance.count
        unit.save()

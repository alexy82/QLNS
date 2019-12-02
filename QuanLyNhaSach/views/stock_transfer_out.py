from rest_framework.viewsets import ModelViewSet
from QuanLyNhaSach.serializers.stock_transfer_out import StockTransferOutDetailSerializer, StockTransferOutSerializer
from QuanLyNhaSach.models.stock_transfer_out import StockTransferOutDetail, StockTransferOut
from datetime import datetime
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
from QuanLyNhaSach.models.customer import Customer
from QLNS.middleware import get_current_user
from QuanLyNhaSach.models.merchandise import Merchandise
from QuanLyNhaSach.models.promotion import Promotion
from QuanLyNhaSach.views.base import BaseITSAdminView


class StockTransferOutListView(BaseITSAdminView):
    def __init__(self):
        super(StockTransferOutListView, self).__init__()
        self.template_name = 'pages/stock_transfer_out.html'
        self.set_context_data(customer_list=Customer.objects.all(), user_list=User.objects.all(),
                              promotion_list=Promotion.objects.filter(is_used=True))


class StockTransferOutAddView(BaseITSAdminView):
    def __init__(self):
        super(StockTransferOutAddView, self).__init__()
        self.template_name = 'pages/stock_transfer_out_detail.html'
        self.set_context_data(books=Merchandise.objects.filter(merchandise_type=1, available_count__gt=0),
                              stationeries=Merchandise.objects.filter(merchandise_type=0, available_count__gt=0),
                              customers=Customer.objects.all())


class StockTransferOutDetailView(BaseITSAdminView):
    def __init__(self):
        super(StockTransferOutDetailView, self).__init__()
        self.template_name = 'pages/stock_transfer_out_detail.html'

    def get(self, request, id, **params):
        note = get_object_or_404(StockTransferOut, pk=id)
        self.extra.update({"note": note,
                           "note_details": StockTransferOutDetail.objects.filter(inside=note)})
        params.update(self.extra)
        return render(request, self.template_name, params)


"""
Phiếu xuất kho:
+Thêm
Tồn kho giảm xuống
+Xóa
Tồn kho tăng lên
+Sửa 
Tồn kho có thể giảm xuống hoặc tăng lên
"""


class StockTransferOutViewSet(ModelViewSet):
    queryset = StockTransferOut.objects.all()
    serializer_class = StockTransferOutSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        __promotion = data.get('promotion','')
        if __promotion != '':
            promotion = Promotion.objects.get(pk=__promotion)
            promotion.is_used = True
            promotion.save()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(created_at=datetime.now())


class StockTransferOutDetailViewSet(ModelViewSet):
    queryset = StockTransferOutDetail.objects.all()
    serializer_class = StockTransferOutDetailSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.get("items")
        for item in data:
            id_unit = item['unit']
            unit = Merchandise.objects.get(pk=id_unit)
            price = unit.price
            unit.available_count -= item['count']
            unit.save()
            customer = StockTransferOut.objects.get(pk=item['inside']).customer
            customer.point += (unit.price * int(item['count'])) // 10000
            customer.save()
            item['price'] = price

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
            detail = StockTransferOutDetail.objects.get(pk=id_detail)
            old_unit = detail.unit
            old_unit.available_count += detail.count
            old_unit.save()
            id_unit = self.request.POST['unit']
            unit = Merchandise.objects.get(pk=id_unit)
            unit.available_count -= int(self.request.POST['count'])
            unit.save()
            if detail.unit_id != id_unit:
                price = unit.price
                serializer.save(price=price)
            else:
                serializer.save()

    def perform_destroy(self, instance):
        unit = Merchandise.objects.get(pk=instance.pk)
        unit += instance.count
        unit.save()

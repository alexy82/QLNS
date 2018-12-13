from rest_framework.viewsets import ModelViewSet
from QuanLyNhaSach.serializers.stock_transfer_in import StockTransferInDetailSerializer, StockTransferInSerializer
from QuanLyNhaSach.models.stock_transfer_in import StockTransferInDetail, StockTransferIn
from datetime import datetime
from QuanLyNhaSach.models.merchandise import Merchandise

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

    def perform_create(self, serializer):
        serializer.save(created_at=datetime.now())


class StockTransferInDetailViewSet(ModelViewSet):
    queryset = StockTransferInDetail.objects.all()
    serializer_class = StockTransferInDetailSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            id_unit = self.request.POST['unit']
            unit = Merchandise.objects.get(pk=id_unit)
            price = unit.price
            unit.available_count += int(self.request.POST['count'])
            unit.save()
            serializer.save(price=price)

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

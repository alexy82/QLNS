from rest_framework import fields
from rest_framework.serializers import ModelSerializer
from QuanLyNhaSach.models.stock_transfer_in import StockTransferIn, StockTransferInDetail
from QuanLyNhaSach.serializers.mechandise import MerchandiseSerializer
from QuanLyNhaSach.serializers.supplier import SupplierSerializer


class StockTransferInDetailSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    price = fields.IntegerField(read_only=True)
    amount = fields.IntegerField(read_only=True)
    unit_detail = MerchandiseSerializer(read_only=True, source='unit')

    class Meta:
        model = StockTransferInDetail
        fields = '__all__'


class StockTransferInSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    detail = StockTransferInDetailSerializer(source='list_detail', many=True, read_only=True)
    created_at = fields.DateTimeField(read_only=True)
    total = fields.IntegerField(read_only=True)
    dept = fields.IntegerField(read_only=True)
    supplier_detail = SupplierSerializer(read_only=True, source='supplier')

    class Meta:
        model = StockTransferIn
        fields = '__all__'

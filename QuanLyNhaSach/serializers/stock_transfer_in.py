from django.contrib.auth.models import User
from rest_framework import fields
from rest_framework.serializers import ModelSerializer, RelatedField
from QuanLyNhaSach.models.stock_transfer_in import StockTransferIn, StockTransferInDetail
from QuanLyNhaSach.serializers.mechandise import MerchandiseSerializer
from QuanLyNhaSach.serializers.supplier import SupplierSerializer
from QuanLyNhaSach.views.user import UserSerializer


class StockTransferInDetailSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    amount = fields.IntegerField(read_only=True)
    unit_detail = MerchandiseSerializer(read_only=True, source='unit')
    inside__created_at = fields.DateTimeField(read_only=True)

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
    created_by_detail = UserSerializer(read_only=True, source='created_by')
    created_by__id = fields.CharField(read_only=True)
    supplier__id = fields.CharField(read_only=True)

    class Meta:
        model = StockTransferIn
        fields = '__all__'

from rest_framework import fields
from rest_framework.serializers import ModelSerializer, ValidationError
from QuanLyNhaSach.models.stock_transfer_out import StockTransferOut, StockTransferOutDetail
from QuanLyNhaSach.models.promotion import Promotion
from QuanLyNhaSach.serializers.promotion import PromotionSerializer
from QuanLyNhaSach.serializers.mechandise import MerchandiseSerializer
from QuanLyNhaSach.serializers.customer import CustomerSerializer
from QuanLyNhaSach.business_layer.merchandise import MerchandiseHelper


class StockTransferOutDetailSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    price = fields.IntegerField(read_only=True)
    amount = fields.IntegerField(read_only=True)
    unit_detail = MerchandiseSerializer(read_only=True, source='unit')
    count = fields.IntegerField(required=True)

    def validate_count(self, count):
        unit = MerchandiseHelper.get_unit_safety(self.initial_data['unit'])
        if unit is None:
            return None
        if unit.available_count < count:
            raise ValidationError('available-count is not enough ')
        return count

    class Meta:
        model = StockTransferOutDetail
        fields = '__all__'


class StockTransferOutSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    detail = StockTransferOutDetailSerializer(source='list_detail', many=True, read_only=True)
    created_at = fields.DateTimeField(read_only=True)
    total = fields.IntegerField(read_only=True)
    dept = fields.IntegerField(read_only=True)
    promotion = fields.IntegerField(required=False, read_only=True)
    promotion_detail = PromotionSerializer(read_only=True, source='promotion')
    customer_detail = CustomerSerializer(read_only=True, source='customer')
    promotion_code = fields.CharField(required=False)

    def validate_promotion_code(self, promotion_code):
        if promotion_code is None or promotion_code == "":
            return None
        promotions = Promotion.objects.filter(code=promotion_code)
        if promotions.count() == 0:
            raise ValidationError('promotion does not exist')
        if promotions[0].is_used:
            raise ValidationError('promotion is used')
        return promotion_code

    class Meta:
        model = StockTransferOut
        fields = '__all__'

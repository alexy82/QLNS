from rest_framework import fields
from rest_framework.serializers import ModelSerializer
from QuanLyNhaSach.models.promotion import Promotion


class PromotionSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    is_used = fields.BooleanField(read_only=True)

    class Meta:
        model = Promotion
        fields = '__all__'

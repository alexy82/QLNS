from rest_framework import fields
from rest_framework.serializers import ModelSerializer, RelatedField
from QuanLyNhaSach.models.merchandise import Merchandise, MerchandiseType


class MerchandiseTypeSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    type_for = fields.IntegerField(read_only=True)
    description = fields.CharField(required=False, allow_blank=True)

    class Meta:
        model = MerchandiseType
        fields = '__all__'


class MerchandiseSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    type_detail = MerchandiseTypeSerializer(source='type', read_only=True)
    merchandise_type = fields.IntegerField(read_only=True)
    available_count = fields.IntegerField(read_only=True)

    class Meta:
        model = Merchandise
        fields = '__all__'

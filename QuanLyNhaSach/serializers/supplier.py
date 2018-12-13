from rest_framework import fields
from rest_framework.serializers import ModelSerializer
from QuanLyNhaSach.models.supplier import Supplier


class SupplierSerializer(ModelSerializer):
    id = fields.CharField(required=False)

    class Meta:
        model = Supplier
        fields = '__all__'

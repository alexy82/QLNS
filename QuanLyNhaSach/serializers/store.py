from rest_framework import fields
from rest_framework.serializers import ModelSerializer
from QuanLyNhaSach.models.store import Store


class StoreSerializer(ModelSerializer):
    id = fields.CharField(required=False)

    class Meta:
        model = Store
        fields = '__all__'

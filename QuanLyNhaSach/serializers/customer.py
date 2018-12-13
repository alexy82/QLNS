from rest_framework import fields
from rest_framework.serializers import ModelSerializer, ValidationError
from QuanLyNhaSach.models.customer import Customer, CustomerType


class CustomerTypeSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    min = fields.IntegerField(default=0)
    max = fields.IntegerField(default=0)
    type = fields.CharField(max_length=64)
    descriptions = fields.CharField(max_length=256)

    class Meta:
        model = CustomerType
        fields = '__all__'


class CustomerSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    name = fields.CharField(required=True)
    point = fields.IntegerField(read_only=True)
    phone = fields.CharField(required=False, max_length=10)
    email = fields.EmailField(required=False)
    address = fields.CharField(required=False)
    type = CustomerTypeSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

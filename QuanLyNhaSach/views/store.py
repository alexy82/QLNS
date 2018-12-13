from rest_framework.viewsets import ModelViewSet
from QuanLyNhaSach.serializers.store import StoreSerializer
from QuanLyNhaSach.models.store import Store


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

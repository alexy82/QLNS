from rest_framework.viewsets import ModelViewSet
from QuanLyNhaSach.serializers.promotion import PromotionSerializer
from QuanLyNhaSach.models.promotion import Promotion


class PromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

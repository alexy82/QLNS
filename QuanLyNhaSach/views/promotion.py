import json
import uuid
from QuanLyNhaSach.views.base import BaseITSAdminView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet
from QuanLyNhaSach.serializers.promotion import PromotionSerializer
from QuanLyNhaSach.models.promotion import Promotion


class PromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    def create(self, request, *args, **kwargs):
        data = request.POST.get("items")
        data = json.loads(data)
        for d in data:
            d['code'] = uuid.uuid4().hex[:16].upper()
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class PromotionListView(BaseITSAdminView):
    def __init__(self):
        super(PromotionListView, self).__init__()
        self.template_name = 'pages/promotion_list.html'

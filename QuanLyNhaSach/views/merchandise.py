from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from QuanLyNhaSach.serializers.mechandise import MerchandiseTypeSerializer, MerchandiseSerializer
from QuanLyNhaSach.models.merchandise import Merchandise, MerchandiseType
from QuanLyNhaSach.views.base import BaseITSAdminView


class BookListView(BaseITSAdminView):
    def __init__(self):
        super(BookListView, self).__init__()
        self.template_name = 'pages/book_list.html'
        self.set_context_data(book_type=MerchandiseType.objects.filter(type_for=1).all())


class BookAddView(BaseITSAdminView):
    def __init__(self):
        super(BookAddView, self).__init__()
        self.template_name = 'pages/book_detail.html'
        self.set_context_data(book_type=MerchandiseType.objects.filter(type_for=1).all(), action="Add",
                              url='/api/books/', btn_content="Create")


class BookUpdateView(BaseITSAdminView):
    def __init__(self):
        super(BookUpdateView, self).__init__()
        self.template_name = 'pages/book_detail.html'
        self.set_context_data(action='Update', btn_content='Save',
                              book_type=MerchandiseType.objects.filter(type_for=1).all())

    def get(self, request, id, **params):
        book = get_object_or_404(Merchandise, pk=id)
        self.extra.update({"book": book,
                           "url": '/api/books/{}/'.format(id)})
        params.update(self.extra)
        return render(request, self.template_name, params)


class BookTypeListView(BaseITSAdminView):
    def __init__(self):
        super(BookTypeListView, self).__init__()
        self.template_name = 'pages/book_type_list.html'


class BookTypeUpdateView(BaseITSAdminView):
    def __init__(self):
        super(BookTypeUpdateView, self).__init__()
        self.template_name = 'pages/book_type_detail.html'
        self.set_context_data(action='Update', btn_content='Save')

    def get(self, request, id, **params):
        type = get_object_or_404(MerchandiseType, pk=id)
        self.extra.update({"type": type,
                           "url": '/api/books-type/{}/'.format(id)})
        params.update(self.extra)
        return render(request, self.template_name, params)


class BookTypeAddView(BaseITSAdminView):
    def __init__(self):
        super(BookTypeAddView, self).__init__()
        self.template_name = 'pages/book_type_detail.html'
        self.set_context_data(action="Add", url='/api/books-type/', btn_content="Create")


class StationeryListView(BaseITSAdminView):
    def __init__(self):
        super(StationeryListView, self).__init__()
        self.template_name = 'pages/stationery_list.html'
        self.set_context_data(stationery_type=MerchandiseType.objects.filter(type_for=0).all())


class StationeryAddView(BaseITSAdminView):
    def __init__(self):
        super(StationeryAddView, self).__init__()
        self.template_name = 'pages/stationery_detail.html'
        self.set_context_data(stationery_type=MerchandiseType.objects.filter(type_for=0).all(), action="Add",
                              url='/api/stationeries/', btn_content="Create")


class StationeryUpdateView(BaseITSAdminView):
    def __init__(self):
        super(StationeryUpdateView, self).__init__()
        self.template_name = 'pages/stationery_detail.html'
        self.set_context_data(action='Update', btn_content='Save',
                              book_type=MerchandiseType.objects.filter(type_for=0).all())

    def get(self, request, id, **params):
        book = get_object_or_404(Merchandise, pk=id)
        self.extra.update({"book": book,
                           "url": '/api/stationeries/{}/'.format(id)})
        params.update(self.extra)
        return render(request, self.template_name, params)


class StationeryTypeListView(BaseITSAdminView):
    def __init__(self):
        super(StationeryTypeListView, self).__init__()
        self.template_name = 'pages/stationery_type_list.html'


class StationeryTypeUpdateView(BaseITSAdminView):
    def __init__(self):
        super(StationeryTypeUpdateView, self).__init__()
        self.template_name = 'pages/stationery_type_detail.html'
        self.set_context_data(action='Update', btn_content='Save')

    def get(self, request, id, **params):
        type = get_object_or_404(MerchandiseType, pk=id)
        self.extra.update({"type": type,
                           "url": '/api/stationeries-type/{}/'.format(id)})
        params.update(self.extra)
        return render(request, self.template_name, params)


class StationeryTypeAddView(BaseITSAdminView):
    def __init__(self):
        super(StationeryTypeAddView, self).__init__()
        self.template_name = 'pages/stationery_type_detail.html'
        self.set_context_data(action="Add", url='/api/stationeries-type/', btn_content="Create")


class BookViewSet(ModelViewSet):
    queryset = Merchandise.objects.filter(merchandise_type=1).all()
    serializer_class = MerchandiseSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(merchandise_type=1, available_count=0)


class BookTypeViewSet(ModelViewSet):
    queryset = MerchandiseType.objects.filter(type_for=1).all()
    serializer_class = MerchandiseTypeSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(type_for=1)


class StationeryViewSet(ModelViewSet):
    queryset = Merchandise.objects.filter(merchandise_type=0).all()
    serializer_class = MerchandiseSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(merchandise_type=0, available_count=0)


class StationeryTypeViewSet(ModelViewSet):
    queryset = MerchandiseType.objects.filter(type_for=0).all()
    serializer_class = MerchandiseTypeSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(type_for=0)

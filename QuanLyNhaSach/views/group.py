from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group, Permission
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from rest_framework import fields
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework.viewsets import ModelViewSet
from QuanLyNhaSach.views.base import BaseITSAdminView, BaseCheckPermission

"""
View Group
include Base View, Group view
"""


class GroupListView(BaseITSAdminView):
    """
    List Group View
    """

    def __init__(self):
        super(GroupListView, self).__init__()
        self.template_name = 'pages/group_list.html'


class GroupAddView(BaseITSAdminView):
    """
    Add Group View
    """
    actions = ['add']

    def __init__(self):
        """
        Template required group:Group, url:str, editable: bool, deleteable:bool
        """
        super(GroupAddView, self).__init__()
        self.template_name = 'pages/group_detail.html'
        self.add_context_data()

    def add_context_data(self):
        unselected_permissions = Permission.objects.filter(Q(content_type__app_label='QuanLyNhaSach') | Q(
            content_type__app_label='auth'))
        self.extra.update({'unselected_permissions': unselected_permissions, 'url': '/api/groups/', 'is_addnew': True})


class GroupEditView(BaseITSAdminView):
    """
    Update Group View
    """

    def __init__(self):
        """
        Template required group:Group, url:str, editable: bool, deleteable:bool
        """
        super(GroupEditView, self).__init__()
        self.template_name = 'pages/group_detail.html'

    @method_decorator(csrf_protect)
    def get(self, request, group_id, **params):
        group = Group.objects.get(pk=group_id)
        selected_permissions = Permission.objects.filter(Q(group=group), Q(content_type__app_label='QuanLyNhaSach') | Q(
            content_type__app_label='auth'))
        unselected_permissions = Permission.objects.exclude(group=group).filter(
            Q(content_type__app_label='QuanLyNhaSach') | Q(
                content_type__app_label='auth'))

        self.extra.update({'selected_permissions': selected_permissions,
                           'unselected_permissions': unselected_permissions,
                           'group': group,
                           'url': '/api/groups/{}/'.format(group_id)
                           }
                          )
        params.update(self.extra)
        return render(request, self.template_name, params)


"""
API Group
include: Serializer class, Permission class, ModelViewSet class
"""


class GroupSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    name = fields.CharField(required=True)
    permissions_ids = PrimaryKeyRelatedField(many=True, read_only=False, queryset=Permission.objects.filter(
        Q(content_type__app_label='QuanLyNhaSach') | Q(content_type__app_label='auth')),
                                             source='permissions')

    class Meta:
        model = Group
        fields = (
            'id', 'name', 'permissions_ids')
        databases_always_serialize = (
            'id', 'name', 'permissions_ids')


class GroupListViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

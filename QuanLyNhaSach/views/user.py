from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group, Permission
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db.models import Q
from rest_framework import fields
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework.viewsets import ModelViewSet

from QuanLyNhaSach.views.base import BaseITSAdminView


class ProfileView(BaseITSAdminView):
    """
    Profile View (Information my account)
    """

    def __init__(self):
        super(ProfileView, self).__init__()
        self.template_name = 'pages/profile.html'


class UserListView(BaseITSAdminView):
    """
    List users view
    """

    def __init__(self):
        super(UserListView, self).__init__()
        self.template_name = 'pages/user_list.html'


class UserEditView(BaseITSAdminView):
    """
    Update users view
    """

    def __init__(self):
        super(UserEditView, self).__init__()
        self.template_name = 'pages/user_edit.html'

    @method_decorator(csrf_protect)
    def get(self, request, user_id, **params):
        user = User.objects.get(pk=user_id)
        selected_permissions = Permission.objects.filter(Q(user=user), Q(content_type__app_label='QuanLyNhaSach') | Q(
            content_type__app_label='auth'))
        unselected_permissions = Permission.objects.exclude(user=user).filter(
            Q(content_type__app_label='QuanLyNhaSach') | Q(
                content_type__app_label='auth'))
        selected_groups = Group.objects.filter(user=user)
        unselected_groups = Group.objects.exclude(user=user)
        self.extra.update({'selected_permissions': selected_permissions,
                           'unselected_permissions': unselected_permissions,
                           'selected_groups': selected_groups,
                           'unselected_groups': unselected_groups,
                           'user_selected': user,
                           }
                          )
        params.update(self.extra)
        return render(request, self.template_name, params)


class UserAddView(BaseITSAdminView):
    """
    Add user view
    """

    def __init__(self):
        super(UserAddView, self).__init__()
        self.template_name = 'pages/user_add.html'

    @method_decorator(csrf_protect)
    def post(self, request, **kwargs):
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_exist = User.objects.filter(email=email, username=email).count()
        if user_exist:
            messages.warning(request, 'Your email was exist please use another')
            return redirect('QuanLyNhaSach:users_add')

        user = User(username=email, email=email, first_name=first_name,
                    last_name=last_name)
        user.save()
        user.username = user.id
        user.save()
        unselected_permissions = Permission.objects.filter(Q(content_type__app_label='QuanLyNhaSach') | Q(
            content_type__app_label='auth'))
        unselected_groups = Group.objects.all()
        self.extra.update({'unselected_permissions': unselected_permissions,
                           'unselected_groups': unselected_groups,
                           'user_selected': user,
                           }
                          )

        return render(request, 'pages/user_edit.html', self.extra)


class ErrorView(BaseITSAdminView):
    def __init__(self):
        super(ErrorView, self).__init__()
        self.template_name = 'pages/error.html'


"""
API users
include: Serializer class, Permission class, ModelViewSet class
"""


class UserSerializer(ModelSerializer):
    id = fields.CharField(required=False)
    email = fields.EmailField(required=False)
    username = fields.CharField(required=False)
    first_name = fields.CharField(required=False, allow_blank=True, allow_null=True)
    last_name = fields.CharField(required=False, allow_blank=True, allow_null=True)
    last_login = fields.DateTimeField(required=False)
    date_joined = fields.DateTimeField(required=False)
    is_active = fields.BooleanField(required=False, default=True)
    is_staff = fields.BooleanField(required=False, default=True)
    is_superuser = fields.BooleanField(required=False, default=True)
    groups_ids = PrimaryKeyRelatedField(required=False, many=True, read_only=False, queryset=Group.objects.all(),
                                        source='groups')
    permissions_ids = PrimaryKeyRelatedField(required=False, many=True, read_only=False,
                                             queryset=Permission.objects.filter(
                                                 Q(content_type__app_label='QuanLyNhaSach') | Q(
                                                     content_type__app_label='auth')),
                                             source='user_permissions')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active',
            'groups_ids', 'permissions_ids', 'is_staff', 'is_superuser')
        databases_always_serialize = (
            'id', 'username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active',
            'groups_ids', 'permissions_ids', 'is_staff', 'is_superuser')


class UserListViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

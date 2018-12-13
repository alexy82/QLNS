from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from rest_framework.permissions import BasePermission
from QLNS.middleware import get_current_user


class BaseITSAdminView(View):
    """
    Base View ITS admin
    """
    actions = None

    def __init__(self, **extra):
        """
        Check permissions and render navigation before response
        :param extra:
        """
        super(BaseITSAdminView, self).__init__()
        # self.check_permission()
        self.extra = extra
        self.template_name = 'layout/main.html'

    @method_decorator(csrf_protect)
    def get(self, request, **params):
        params.update(self.extra)
        return render(request, self.template_name, params)

    def get_context_data(self, **kwargs):
        context = super(BaseITSAdminView, self).get_context_data(**kwargs)  # get the default context data
        return context

    def set_context_data(self, **kwargs):
        self.extra.update(kwargs)

    def action_allow(self):
        if self.label is None:
            return
        user = get_current_user()
        deleteable = user.has_perm(self.label.format('delete'))
        updateable = user.has_perm(self.label.format('change'))
        if deleteable:
            self.extra.update({"deleteable": True})
        if updateable:
            self.extra.update({"updateable": True})

    def check_permission(self):
        """
        Check permission by label and action
        :return: PermissionDenied Exception
        """
        permission_required = (self.label.format(action) for action in self.actions) if self.actions else None
        if permission_required is not None:
            if not get_current_user().has_perms(permission_required):
                self.handle_no_permission()
                raise PermissionDenied

    def handle_no_permission(self):
        pass


class BaseCheckPermission(BasePermission):
    """
    Check permission for API
    """
    permissions_allow = {"GET": "view", "POST": "add", "PUT": "change", "PATCH": "change", "DELETE": "delete"}

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method not in self.permissions_allow:
            return False
        if not request.user.has_perm(self.label.format(self.permissions_allow[request.method])):
            return False
        return True

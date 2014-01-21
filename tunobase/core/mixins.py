"""
CORE APP

This module is used to additional functionality provided to the app.

"""
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.paginator import Paginator
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from tunobase.core import utils as core_utils

class AjaxMorePaginationMixin(object):
    """View mixin that returns JSON paginated data."""

    partial_template_name = None

    def dispatch(self, request, *args, **kwargs):
        """Handle request and return response."""

        if self.partial_template_name is None:
            raise ImproperlyConfigured(
                _("'AjaxMorePaginationMixin' requires "
                "'partial_template_name' attribute to be set.")
            )

        page = request.GET.get('page', None)

        if page is not None:
            if hasattr(self, 'get_object'):
                self.object = self.get_object()
            self.queryset = self.get_queryset()
            paginate_by = request.GET.get('paginate_by', self.paginate_by)
            paginator = Paginator(self.queryset, paginate_by)
            object_list= paginator.page(page)
            has_previous = object_list.has_previous()
            has_next = object_list.has_next()

            return core_utils.respond_with_json({
                'success': True,
                'content': render_to_string(
                    self.partial_template_name,
                    RequestContext(
                        request, {
                            'object_list': object_list
                        }
                    )
                ),
                'has_previous': has_previous,
                'has_next': has_next,
                'previous_page_number': object_list.previous_page_number() \
                        if has_previous else 0,
                'next_page_number': object_list.next_page_number() \
                        if has_next else 0,
                'page_number': object_list.number,
                'start_index': object_list.start_index(),
                'end_index': object_list.end_index()
            })

        return super(AjaxMorePaginationMixin, self)\
                .dispatch(request, *args, **kwargs)


class DeterministicLoginRequiredMixin(object):
    """Handle user login."""

    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth
    deterministic_function = None

    def dispatch(self, request, *args, **kwargs):
        """Handle request and return response."""

        if self.deterministic_function is None:
            raise ImproperlyConfigured(
                _("'DeterministicLoginRequiredMixin' requires "
                "'deterministic_function' attribute to be set.")
            )

        if not request.user.is_authenticated() \
                and not self.deterministic_function():  # Standard user,
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return redirect_to_login(request.get_full_path(),
                    self.login_url,
                    self.redirect_field_name)

        return super(DeterministicLoginRequiredMixin, self)\
                .dispatch(request, *args, **kwargs)


class LoginRequiredMixin(object):
    """
    View mixin which verifies that the user has authenticated.

    NOTE:
        This should be the left-most mixin of a view.

    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self)\
                .dispatch(request, *args, **kwargs)


class GroupRequiredMixin(object):
    """Mixin allows you to require a user in certain Groups."""
    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth
    groups_required = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Handle request and return response."""

        if self.groups_required == None:
            raise ImproperlyConfigured(
                _("'GroupRequiredMixin' requires "
                "'groups_required' attribute to be set.")
            )

        if request.user.is_admin or request.user.groups\
                .filter(name__in=self.groups_required).exists():
            group_meets_requirements = True
        else:
            group_meets_requirements = False

        if not group_meets_requirements:
            if self.raise_exception:
                raise PermissionDenied
            else:
                return redirect_to_login(request.get_full_path(),
                    self.login_url,
                    self.redirect_field_name)

        return super(GroupRequiredMixin, self)\
                .dispatch(request, *args, **kwargs)


class PermissionRequiredMixin(object):
    """
    View mixin which verifies that the logged in user has the specified
    permission.

    Class Settings
    `permission_required` - the permission to check for.
    `login_url` - the login url of site
    `redirect_field_name` - defaults to "next"
    `raise_exception` - defaults to False - raise 403 if set to True

    Example Usage

        class SomeView(PermissionRequiredMixin, ListView):
            ...
            # required
            permission_required = "app.permission"

            # optional
            login_url = "/signup/"
            redirect_field_name = "hollaback"
            raise_exception = True
            ...
    """
    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    permission_required = None  # Default required perms to none
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    def dispatch(self, request, *args, **kwargs):
        # Make sure that a permission_required is set on the view,
        # and if it is, that it only has two parts (app.action_model)
        # or raise a configuration error.
        if self.permission_required == None or len(
            self.permission_required.split(".")) != 2:
            raise ImproperlyConfigured(
                    _("'PermissionRequiredMixin' requires "
                    "'permission_required' attribute to be set.")
            )

        # Check to see if the request's user has the required permission.
        has_permission = request.user.has_perm(self.permission_required)

        if not has_permission:  # If the user lacks the permission
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return redirect_to_login(request.get_full_path(),
                    self.login_url,
                    self.redirect_field_name)

        return super(PermissionRequiredMixin, self).dispatch(request,
            *args, **kwargs)


class PermissionOrCreatorRequiredMixin(object):
    """
    View mixin which verifies that the logged in user has the specified
    permission.

    Class Settings
    `permission_required` - the permission to check for.
    `login_url` - the login url of site
    `redirect_field_name` - defaults to "next"
    `raise_exception` - defaults to False - raise 403 if set to True

    Example Usage

        class SomeView(PermissionRequiredMixin, ListView):
            ...
            # required
            permission_required = "app.permission"

            # optional
            login_url = "/signup/"
            redirect_field_name = "hollaback"
            raise_exception = True
            ...
    """
    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    permission_required = None  # Default required perms to none
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    def get(self, request, *args, **kwargs):
        # Make sure that a permission_required is set on the view,
        # and if it is, that it only has two parts (app.action_model)
        # or raise a configuration error.
        if self.permission_required == None or len(
            self.permission_required.split(".")) != 2:
            raise ImproperlyConfigured(
                    _("'PermissionOrCreatorRequiredMixin' requires "
                    "'permission_required' attribute to be set.")
            )

        # Check to see if the request's user has the required permission.
        has_permission = request.user.has_perm(self.permission_required)
        user_created = request.user == self.get_object().created_by

        # If the user lacks the permission
        if not has_permission and not user_created:
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return redirect_to_login(request.get_full_path(),
                    self.login_url,
                    self.redirect_field_name)

        return super(PermissionOrCreatorRequiredMixin, self)\
                .get(request, *args, **kwargs)


class AdminRequiredMixin(object):
    """
    Mixin allows you to require a user with `is_superuser` set to True.
    """
    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:  # If the user is a standard user,
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return redirect_to_login(request.get_full_path(),
                    self.login_url,
                    self.redirect_field_name)

        return super(AdminRequiredMixin, self)\
                .dispatch(request, *args, **kwargs)


class MultiplePermissionsRequiredMixin(object):
    """
    View mixin which allows you to specify two types of permission
    requirements. The `permissions` attribute must be a dict which
    specifies two keys, `all` and `any`. You can use either one on
    it's own or combine them. Both keys values are required be a list or
    tuple of permissions in the format of
    <app label>.<permission codename>

    By specifying the `all` key, the user must have all of
    the permissions in the passed in list.

    By specifying The `any` key , the user must have ONE of the set
    permissions in the list.

    Class Settings
        `permissions` - This is required to be a dict with one or both
            keys of `all` and/or `any` containing a list or tuple of
            permissions in the format of <app label>.<permission codename>
        `login_url` - the login url of site
        `redirect_field_name` - defaults to "next"
        `raise_exception` - defaults to False - raise 403 if set to True

    Example Usage
        class SomeView(MultiplePermissionsRequiredMixin, ListView):
            ...
            #required
            permissions = {
                "all": (blog.add_post, blog.change_post),
                "any": (blog.delete_post, user.change_user)
            }

            #optional
            login_url = "/signup/"
            redirect_field_name = "hollaback"
            raise_exception = True
    """
    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    permissions = None  # Default required perms to none
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    def dispatch(self, request, *args, **kwargs):
        self._check_permissions_attr()

        perms_all = self.permissions.get('all') or None
        perms_any = self.permissions.get('any') or None

        self._check_permissions_keys_set(perms_all, perms_any)
        self._check_perms_keys("all", perms_all)
        self._check_perms_keys("any", perms_any)

        # If perms_all, check that user has all permissions in the list/tuple
        if perms_all:
            if not request.user.has_perms(perms_all):
                if self.raise_exception:
                    raise PermissionDenied
                return redirect_to_login(request.get_full_path(),
                    self.login_url,
                    self.redirect_field_name)

        # If perms_any, check that user has at least one in the list/tuple
        if perms_any:
            has_one_perm = False
            for perm in perms_any:
                if request.user.has_perm(perm):
                    has_one_perm = True
                    break

            if not has_one_perm:
                if self.raise_exception:
                    raise PermissionDenied
                return redirect_to_login(request.get_full_path(),
                    self.login_url,
                    self.redirect_field_name)

        return super(MultiplePermissionsRequiredMixin, self)\
                .dispatch(request, *args, **kwargs)

    def _check_permissions_attr(self):
        """
        Check permissions attribute is set and that it is a dict.
        """
        if self.permissions is None or not isinstance(self.permissions, dict):
            raise ImproperlyConfigured(
                    _("'PermissionsRequiredMixin' requires "
                    "'permissions' attribute to be set to a dict.")
            )

    def _check_permissions_keys_set(self, perms_all=None, perms_any=None):
        """
        Check to make sure the keys `any` or `all` are not both blank.
        If both are blank either an empty dict came in or the wrong keys
        came in. Both are invalid and should raise an exception.
        """
        if perms_all is None and perms_any is None:
            raise ImproperlyConfigured(
                    _("'PermissionsRequiredMixin' requires"
                    "'permissions' attribute to be set to a dict and the "
                    "'any' or 'all' key to be set.")
            )

    def _check_perms_keys(self, key=None, perms=None):
        """
        If the permissions list/tuple passed in is set, check to make
        sure that it is of the type list or tuple.
        """
        if perms and not isinstance(perms, (list, tuple)):
            raise ImproperlyConfigured(
                    _("'MultiplePermissionsRequiredMixin' "
                    "requires permissions dict '%s' value to be a list "
                    "or tuple." % key)
            )


class FilterMixin(object):
    """
    Mixin allows you to filter by keys in the GET request.
    """
    def get_queryset_filters(self):
        filters = {}
        for item in self.allowed_filters:
            if item in self.request.GET and self.request.GET[item]:
                filters[self.allowed_filters[item]] = self.request.GET[item]

        return filters

    def get_queryset(self):
        return super(FilterMixin, self).get_queryset()\
            .filter(**self.get_queryset_filters())

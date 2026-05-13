"""
core/decorators.py

Reusable authorization decorators for FinTrack.

Usage in function-based views:

    from core.decorators import admin_required, operator_required

    @admin_required
    def my_view(request):
        ...

    @operator_required
    def another_view(request):
        ...

For class-based views, use mixins from core.mixins instead.
"""

from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .utils import is_admin, is_operator


def admin_required(view_func):
    """
    Decorator that restricts a view to Admin group members only.

    Behaviour:
    - Unauthenticated users are redirected to the login page.
    - Authenticated users who are NOT in the Admin group receive
      a 403 access denied response.
    - Admin users proceed to the view normally.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not is_admin(request.user):
            messages.error(
                request,
                "You do not have permission to access that page. "
                "Admin access is required."
            )
            return redirect('core:access_denied')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def operator_required(view_func):
    """
    Decorator that restricts a view to Operator or Admin group members.

    Behaviour:
    - Unauthenticated users are redirected to the login page.
    - Authenticated users who are NOT in Admin or Operator groups
      receive a 403 access denied response.
    - Admin and Operator users proceed to the view normally.

    Note: Admin is a superset of Operator. An Admin user passes
    this check successfully.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not is_operator(request.user):
            messages.error(
                request,
                "You do not have permission to access that page."
            )
            return redirect('core:access_denied')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

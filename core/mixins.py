"""
core/mixins.py

Reusable authorization mixins for FinTrack class-based views (CBVs).

Usage:

    from core.mixins import AdminRequiredMixin, OperatorRequiredMixin
    from django.views.generic import CreateView

    class SupplierCreateView(AdminRequiredMixin, CreateView):
        model = Supplier
        ...

IMPORTANT: The mixin must appear BEFORE the base view class in the
inheritance list. Python reads MRO (Method Resolution Order) left to
right. The mixin's dispatch() must execute before the view's dispatch().

Correct:   class MyView(AdminRequiredMixin, CreateView)
Incorrect: class MyView(CreateView, AdminRequiredMixin)
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from .utils import is_admin, is_operator


class AdminRequiredMixin(LoginRequiredMixin):
    """
    Mixin that restricts a CBV to Admin group members only.

    Behaviour mirrors the @admin_required decorator.
    Inherits from LoginRequiredMixin to enforce authentication first.
    """

    def dispatch(self, request, *args, **kwargs):
        # LoginRequiredMixin.dispatch() handles unauthenticated users
        response = super().dispatch(request, *args, **kwargs)

        # If super() already redirected (unauthenticated), return that
        if response.status_code == 302:
            return response

        # Now check Admin group membership
        if not is_admin(request.user):
            messages.error(
                request,
                "You do not have permission to access that page. "
                "Admin access is required."
            )
            return redirect('core:access_denied')

        return response


class OperatorRequiredMixin(LoginRequiredMixin):
    """
    Mixin that restricts a CBV to Operator or Admin group members.

    Behaviour mirrors the @operator_required decorator.
    Inherits from LoginRequiredMixin to enforce authentication first.
    """

    def dispatch(self, request, *args, **kwargs):
        # LoginRequiredMixin.dispatch() handles unauthenticated users
        response = super().dispatch(request, *args, **kwargs)

        # If super() already redirected (unauthenticated), return that
        if response.status_code == 302:
            return response

        # Now check Operator/Admin group membership
        if not is_operator(request.user):
            messages.error(
                request,
                "You do not have permission to access that page."
            )
            return redirect('core:access_denied')

        return response

"""
core/utils.py

Security utility functions for FinTrack.

These functions are the single source of truth for role checking.
Both decorators (core/decorators.py) and mixins (core/mixins.py)
import from here. This means role logic is defined once and only once.

If the group names ever change (they should not), only this file
needs to be updated.

Usage anywhere in the project:

    from core.utils import is_admin, is_operator

    if is_admin(request.user):
        # show admin-only UI elements

    if is_operator(request.user):
        # show operator-accessible UI elements
"""

from django.contrib.auth.models import User


def is_admin(user: User) -> bool:
    """
    Returns True if the user belongs to the 'Admin' group.

    Admins have full system access: all CRUD, user management,
    Django admin, export, deactivation, cancellation.

    This does NOT return True for superusers who are not in the
    Admin group. Superuser status is for Django admin access only.
    For business logic, group membership is the authority.
    """
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name='Admin').exists()


def is_operator(user: User) -> bool:
    """
    Returns True if the user belongs to the 'Operator' OR 'Admin' group.

    Admin is a superset of Operator. An Admin user passes all
    operator-level permission checks.

    Operators can: add/edit purchases, view all pages, generate
    statements, add credit sales.

    Operators cannot: manage users, deactivate suppliers/products,
    cancel purchases, create schemes.
    """
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name__in=['Admin', 'Operator']).exists()


def get_user_role(user: User) -> str:
    """
    Returns a human-readable string describing the user's role.
    Useful for display in templates and admin UIs.

    Returns:
        'Admin'      — if user is in Admin group
        'Operator'   — if user is in Operator group (but not Admin)
        'No Role'    — if user is authenticated but in neither group
        'Anonymous'  — if user is not authenticated
    """
    if not user or not user.is_authenticated:
        return 'Anonymous'
    if is_admin(user):
        return 'Admin'
    if user.groups.filter(name='Operator').exists():
        return 'Operator'
    return 'No Role'

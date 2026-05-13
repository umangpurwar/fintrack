"""
core/templatetags/auth_extras.py

Custom Django template filters for role-based rendering.

Usage in templates:

    {% load auth_extras %}

    {% if user|is_admin_filter %}
        <!-- Admin-only content -->
    {% endif %}

    {{ user|user_role_filter }}
    <!-- Outputs: 'Admin', 'Operator', or 'No Role' -->
"""

from django import template
from core.utils import is_admin, is_operator, get_user_role

register = template.Library()


@register.filter(name='is_admin_filter')
def is_admin_filter(user):
    """
    Template filter that returns True if the user is in the Admin group.

    Usage:
        {% if user|is_admin_filter %}
            <!-- admin-only block -->
        {% endif %}
    """
    return is_admin(user)


@register.filter(name='is_operator_filter')
def is_operator_filter(user):
    """
    Template filter that returns True if the user is in Admin or Operator group.

    Usage:
        {% if user|is_operator_filter %}
            <!-- operator-accessible block -->
        {% endif %}
    """
    return is_operator(user)


@register.filter(name='user_role_filter')
def user_role_filter(user):
    """
    Template filter that returns the user's role as a display string.

    Usage:
        {{ user|user_role_filter }}
        <!-- Outputs: 'Admin', 'Operator', 'No Role', or 'Anonymous' -->
    """
    return get_user_role(user)

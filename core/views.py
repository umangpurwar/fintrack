"""
core/views.py

Core application views for FinTrack.

Currently contains only the access_denied view. Future security
infrastructure views (if any) will also live here.
"""

from django.shortcuts import render


def access_denied(request,exception):
    """
    Renders the 403 access denied page.

    This view is called by the @admin_required and @operator_required
    decorators (and their mixin equivalents) when an authenticated user
    attempts to access a resource they do not have permission for.

    Returns HTTP 403 status code so that browsers and logs correctly
    identify this as a permission error, not a page not found.
    """
    return render(request, '403.html', status=403)

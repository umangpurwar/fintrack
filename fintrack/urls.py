"""
FinTrack Root URL Configuration
---------------------------------
This file is the entry point for ALL URL routing in FinTrack.
Django reads ROOT_URLCONF = 'fintrack.urls' in settings.py
and routes every request through the patterns defined here.

Module URL files will be included here as each module is built:
  - suppliers.urls  (Module 1)
  - purchases.urls  (Module 2)
  - reports.urls    (Module 4)
  - credit.urls     (Module 5)
  - pnl.urls        (Module 6)
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [

    # ── Admin Panel ──────────────────────────────────────────────
    path('admin/', admin.site.urls),
    # Django's built-in admin panel.
    # After running createsuperuser, log in at http://127.0.0.1:8000/admin/
    # The admin panel gives you CRUD on all models out of the box.
    # Superusers can manage users, groups, and (later) all business data.

    # ── Authentication ────────────────────────────────────────────
    path('accounts/', include('django.contrib.auth.urls')),
    # This single line wires up ALL of Django's built-in auth views:
    #   /accounts/login/           → LoginView
    #   /accounts/logout/          → LogoutView
    #   /accounts/password_change/ → PasswordChangeView
    #   /accounts/password_reset/  → PasswordResetView
    # Django looks for templates in templates/registration/ for these views.
    # We only need to create the template files — the view logic is provided by Django.

    # ── Root Redirect ─────────────────────────────────────────────
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    # Visiting the root URL (/) redirects to the login page.
    # permanent=False means HTTP 302 (temporary redirect) — not HTTP 301 (permanent).
    # Use 302 during development so browsers don't cache the redirect.
    # In Module 6, this will be replaced with the dashboard view for logged-in users.

    # ── Future Module URLs (add as modules are built) ─────────────
    # path('suppliers/', include('suppliers.urls')),
    # path('purchases/', include('purchases.urls')),
    # path('reports/', include('reports.urls')),
    # path('credit/', include('credit.urls')),
    # path('pnl/', include('pnl.urls')),
]

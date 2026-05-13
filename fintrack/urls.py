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

    # ── Authentication ────────────────────────────────────────────
    path('accounts/', include('django.contrib.auth.urls')),
    # This single line wires up ALL of Django's built-in auth views:

    # Core app — security infrastructure (access denied, etc.)
    path('core/', include('core.urls', namespace='core')),

    # ── Root Redirect ─────────────────────────────────────────────
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    # Visiting the root URL (/) redirects to the login page.

    # ── Future Module URLs (add as modules are built) ─────────────
    # path('suppliers/', include('suppliers.urls')),
    # path('purchases/', include('purchases.urls')),
    # path('reports/', include('reports.urls')),
    # path('credit/', include('credit.urls')),
    # path('pnl/', include('pnl.urls')),
]

# Custom error handlers
handler403 = 'core.views.access_denied'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    Dashboard, 
    AboutView,
    change_theme, 
    chart_data, 
    login_view, 
    otp_view, 
    logout_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Dashboard.as_view(), name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('otp/', otp_view, name='otp'),
    path('about/', AboutView.as_view(), name='about'),
    path('chart-data/', chart_data, name='data'),
    path('switch/', change_theme, name='change'),   
    path('books/', include('books.urls',namespace='books')),
    path('rentals/', include('rentals.urls',namespace='rentals')),
    path('__reload__/', include('django_browser_reload.urls')), #used for autoreload with django_browser_reload
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Book Rental Administration'
admin.site.index_title = 'Manage the Book Rental System'
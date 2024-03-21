from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import home_view, change_theme

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('switch/', change_theme, name='change'),   
    path('books/', include('books.urls',namespace='books')),
    path('__reload__/', include('django_browser_reload.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Book Rental Administration'
admin.site.index_title = 'Manage the Book Rental System'
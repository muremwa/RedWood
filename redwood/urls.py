from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # admin/
    path('admin/', admin.site.urls),

    # watch/
    path('watch/', include('watch.urls')),

    # accounts/
    path('accounts/', include('accounts.urls')),

    # staff/
    path('staff/', include('staff.urls')),

    # # media  | comment out when debug is true
    # re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # # static  | comment out when debug is true
    # re_path('^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


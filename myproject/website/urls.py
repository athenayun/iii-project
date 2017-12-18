from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        url(r'^$', views.post_list, name='post_list'),
        url(r'^ir_upload', views.go_upload, name='go_upload'),
        #url(r'^product$', views.go_product, name='go_product'),
        url(r'^make_query', views.make_query, name='make_query'),
        url(r'^product', views.posting_garbage, name='posting_garbage'),

        
        ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

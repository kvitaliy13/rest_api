from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from mpass.views import MPassViewset

mpass_list = MPassViewset.as_view({
    'post': 'create'
})
mpass_detail = MPassViewset.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})
mpass_list_filtered = MPassViewset.as_view({
    'get': 'list',
})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submitData', mpass_list, name='mpass-list'),
    path('submitData/<int:pk>', mpass_detail, name='mpass-detail'),
    path('submitData/', mpass_list_filtered, name='mpass-list-filtered'),
    path('swagger-ui/', TemplateView.as_view(template_name="swagger-ui.html")),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),
]

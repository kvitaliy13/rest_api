from django.db.utils import OperationalError
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.views import exception_handler

from .exceptions import DBConnectException, ObjectStatusException
from .models import AddedMPass
from .serializers import MPassSerializer


class MPassViewset(viewsets.ModelViewSet):
    serializer_class = MPassSerializer

    def get_queryset(self):
        user_email = self.request.query_params.get('user_email')
        if user_email:
            queryset = AddedMPass.objects.filter(user__email=user_email)
        else:
            path = self.request.get_full_path()
            if path == '/submitData/':
                queryset = AddedMPass.objects.none()
            else:
                queryset = AddedMPass.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            response.status_code = 200
        response_data = {
            'status': response.status_code,
            'message': response.status_text,
            'id': response.data['id'] if response.status_code == 200 else None,
        }
        response.data = response_data
        return response

    def retrieve(self, request, *args, **kwargs):
        try:
            if not AddedMPass.objects.filter(id=kwargs['pk']).exists():
                raise NotFound
            return super().retrieve(request, *args, **kwargs)
        except OperationalError:
            raise DBConnectException()

    def partial_update(self, request, *args, **kwargs):
        try:
            queryset = AddedMPass.objects.filter(id=kwargs['pk'])
            if not queryset.exists():
                raise NotFound
            query_object = queryset.first()
            if not query_object.status == 'new':
                raise ObjectStatusException
            response = super().partial_update(request, *args, **kwargs)
            response.data = {
                'status': response.status_code,
                'message': response.status_text,
                'state': 1,
            }
            return response
        except OperationalError:
            raise DBConnectException()


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context['request']
    path = request.get_full_path()
    pk = context['kwargs'].get('pk', '')
    if response is not None:
        response.data = {
            'status': response.status_code,
            'message': exc.detail,
        }
        if path == '/submitData':
            response.data['id'] = None
        elif path == f'/submitData/{pk}' and request.method == 'PATCH':
            response.data['state'] = 0

    return response

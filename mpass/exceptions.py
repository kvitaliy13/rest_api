from rest_framework.exceptions import APIException


class EncodeDecodeException(APIException):
    status_code = 500
    default_detail = 'Image encode/decode error'


class DBConnectException(APIException):
    status_code = 500
    default_detail = 'Database error'


class ObjectStatusException(APIException):
    status_code = 403
    default_detail = 'Object status forbids changes'

from rest_framework import status
from rest_framework.exceptions import APIException


class Conflict(APIException):
    default_code = 'conflict'
    default_detail = 'The resource already exists'
    status_code = status.HTTP_409_CONFLICT

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CustomResponse(Response):
    def __init__(self, data=None, status=status.HTTP_200_OK,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super().__init__(data, status=status, template_name=template_name,
                         headers=headers, exception=exception,
                         content_type=content_type)
        self.data = {
            'data': self.data,
            'app_version': '1.0.0'
        }


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'data': response.data,
            'app_version': '1.0.0',
            'status_code': response.status_code
        }

    return response


class CustomNotFound(NotFound):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found.'
    default_code = 'not_found'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        self.detail = {
            'data': {'detail': detail},
            'app_version': '1.0.0'
        }

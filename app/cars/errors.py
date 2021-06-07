from django.http import JsonResponse
from rest_framework.views import exception_handler


def has_build_in_exceptions(response, dict_key):
    if response.data.get(dict_key):
        return True
    return False


def get_build_in_exceptions(response, dict_key):
    errors = response.data.get(dict_key)
    errors_msg = ''
    if errors:
        for error in errors:
            errors_msg += str(error)
    return errors_msg


def handle_build_in_exceptions(response):
    error_keys = ['non_field_errors', 'detail']
    caught_errors = ''
    for error_key in error_keys:
        caught_errors += get_build_in_exceptions(response, error_key)
    return caught_errors


def error_handler(exc, context):
    caught_errors = None
    response = exception_handler(exc, context)

    # Custom front-end friendly error messages
    if isinstance(exc, InvalidApiUsage):
        return response_error(exc)

    # Change django build-in errors for custom front-end friendly
    if response:
        caught_errors = handle_build_in_exceptions(response)
    if caught_errors:
        return response_manual(caught_errors, response.status_code)

    return response


class InvalidApiUsage(Exception):
    params = None
    code = 400

    def __init__(self, message=None, code=None, params=None):
        if message:
            self.message = message
        if code:
            self.code = code
        if params:
            self.params = params
        super().__init__(self.message, self.code)

    def return_error(self):
        return response_error(self)


def response_error(e):
    return JsonResponse({'message': e.message}, status=e.code)


def response_manual(message, code):
    return JsonResponse({'message': message}, status=code)


class CarApiErrors:
    class ExternalApiCarNotFound(InvalidApiUsage):
        message = 'Car not found'

    class CarNotUnique(InvalidApiUsage):
        message = 'The fields make, model must make a unique set.'

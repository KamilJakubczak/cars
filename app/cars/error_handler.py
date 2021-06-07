from django.http import JsonResponse
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


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


def has_build_in_exceptions(response, dict_key):
    if response.data.get(dict_key):
        return True
    return False


def get_build_in_exceptions(response, dict_key):
    errors = response.data.get(dict_key)
    errors_msg = ''
    if errors:
        errors_msg = ''.join([str(error) for error in errors])
    return errors_msg


def handle_build_in_exceptions(response):
    error_keys = ['non_field_errors', 'detail']
    caught_errors = ''.join(
        get_build_in_exceptions(response, ek) for ek in error_keys)
    return caught_errors


def handle_invalid_api_usage(exc):
    return response_error(exc)


def handle_validation_error(exc):
    message = ''
    keys = [key for key in exc.detail.keys()]
    for key in keys:
        message += ''.join(str(ex) for ex in exc.detail[key])
    return response_manual(message, exc.status_code)


def handle_rest_errors(response):
    caught_errors = handle_build_in_exceptions(response)
    if caught_errors:
        return response_manual(caught_errors, response.status_code)
    return None


def error_handler(exc, context):
    response = exception_handler(exc, context)

    # Custom front-end friendly error messages
    if isinstance(exc, InvalidApiUsage):
        return handle_invalid_api_usage(exc)
    if isinstance(exc, ValidationError):
        return handle_validation_error(exc)
    if response:
        return handle_rest_errors(response)

    return response


def response_error(e):
    return JsonResponse({'message': e.message}, status=e.code)


def response_manual(message, code):
    return JsonResponse({'message': message}, status=code)

def exceptions_handler_for_requests(error: Exception) -> str:
    from googleapiclient.errors import HttpError

    class CustomError(Exception):
        pass

    class ForbiddenError(CustomError):
        def __str__(self):
            return 'Forbidden error: service email does not have access to the table'

    class NotFoundError(CustomError):
        def __str__(self):
            return 'Not found error: the requested resource was not found'

    class UnauthorizedError(CustomError):
        def __str__(self):
            return 'Unauthorized error: invalid credentials'

    class BadRequestError(CustomError):
        def __str__(self):
            return 'Bad request error: the request was invalid or cannot be otherwise served'

    class InternalServerError(CustomError):
        def __str__(self):
            return 'Internal server error: the server encountered an error and could not complete your request'

    class TooManyRequestsError(CustomError):
        def __str__(self):
            return 'Too many requests error: the user has sent too many requests in a given amount of time'

    class ServiceUnavailableError(CustomError):
        def __str__(self):
            return ('Service unavailable error: the server is currently unavailable '
                    '(because it is overloaded or down for maintenance)')

    if isinstance(error, HttpError):
        status = error.status_code
        if status == 400:
            raise BadRequestError()
        elif status == 401:
            raise UnauthorizedError()
        elif status == 403:
            raise ForbiddenError()
        elif status == 404:
            raise NotFoundError()
        elif status == 429:
            raise TooManyRequestsError()
        elif status == 500:
            raise InternalServerError()
        elif status == 503:
            raise ServiceUnavailableError()
        else:
            return f'http_error_{status}'
    else:
        return str(error)

import datetime


class CPPotifyException(Exception):
    def __init__(self, message):
        super.__init__(message)

    def __str__(self):
        return "Exception found in CPPotify call"


class SpotifyArgException(CPPotifyException):
    def __init__(self, message, method, timestamp: datetime.datetime):
        super.__init__(message)
        self.method = method
        self.timestamp = self.timestamp

    def __str__(self):
        return """Exception found in call to method {0} at {1}"""


class SpotifyResponseException(CPPotifyException):
    def __init__(self, message, response: dict, obj, request_url, timestamp: datetime.datetime):
        super.__init__(message)
        self.response = response
        self.obj = obj
        self.request_url = request_url
        self.timestamp = self.timestamp

    def __str__(self):
        return "Exception found in arguments made to CPPotify call. Retry the method using the correct argumnets"

    
'''[def _parse_errors(self, response: dict, obj, request_url, timestamp: datetime):
        """
        Returns a more detailed error object

        :param response: The response being parse for an error
        :param obj: Spotify object that generated the response
        :param timestamp: Timestamp of the request 
        @return error_obj: Detailed error object containing error code, error reason, error message, Spotify object, Spotify request URL and timestamp
        """
        response_map = {
            '200': 'OK',
            '201': 'Created',
            '202': 'Accepted',
            '204': 'No Content',
            '304': 'Not Modified',
            '400': 'Bad Request',
            '401': 'Unauthorized',
            '403': 'Forbidden',
            '404': 'Not Found',
            '429': 'Too Many Requests - Rate limiting has been applied.',
            '500': 'Internal Server Error',
            '502': 'Bad Gateway',
            '503': 'Service Unavailable'
        }
        try:
            if 'error' in response.keys():
                try:
                    print("""Found error in response. \n
                             URL: {} \n
                             Code: {} \n
                             Reason: {} \n
                             Message: {} \n """.\
                        format(request_url,
                            str(response['error']['status']), 
                            response_map[str(response['error']['status'])],
                            response['error']['message']))

                    return {'error': str(response['error']['status']),
                            'reason': response_map[str(response['error']['status'])],
                            'message': response['error']['message'],
                            'request_obj': obj,
                            'request_url': request_url, 
                            'time': str(timestamp)}
                except:
                    warnings.warn("Unexpected error occured")
                    return response 
            else:
                return response
        except:
            return response'''
import datetime

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

    def __init__(self, response: dict, obj, request_url, timestamp: datetime.datetime, message = ''):
        self.response = response
        self.obj = obj
        self.request_url = request_url
        self.timestamp = self.timestamp
        self.message = """Found error in response. \n
                          URL: {} \n
                          Spotify Object: {} \n
                          Code: {} \n
                          Reason: {} \n
                          Message: {} \n 
                          Timestamp: {} \n""".\
                          format(self.request_url,
                                 self.obj,
                                 str(self.response['error']['status']), 
                                 response_map[str(self.response['error']['status'])],
                                 self.response['error']['message'],
                                 str(self.timestamp))
        super().__init__(self.message)

    def __str__(self):
        return "Exception found in arguments made to CPPotify call. Retry the method using the correct argumnets"

    


class InvalidOperation(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidOperationArguments(Exception):
    def __init__(self, message):
        super().__init__(message)
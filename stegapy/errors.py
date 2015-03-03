from stegapy.models.error import Error


class InputError(Error):
    """Exception raised for errors in the input.

    Arguments:

        message – explanation of the error
    """

    def __init__(self, message='Unsupported format'):
        self.message = message


class ContainerError(Error):
    """Exception raised for errors in the container.

    Arguments:

        message – explanation of the error
    """

    def __init__(self, message='Unsupported format'):
        self.message = message

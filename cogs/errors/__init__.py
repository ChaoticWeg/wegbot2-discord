""" Custom exceptions """

class WegbotException(Exception):
    """ Custom Wegbot exception. Should be used more as a warning, in lieu of "if ... return". """

    def __init__(self, message):
        super().__init__(message)
        self.message = message

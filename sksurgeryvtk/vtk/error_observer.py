""" Classes for handling vtk errors """

class ErrorObserver:
    """
    A class to detect VTK errors
    """

    def __init__(self):
        self.__error_occurred = False
        self.__error_message = None
        self.call_data_type = 'string0'

    def __call__(self, obj, event, message):
        self.__error_occurred = True
        self.__error_message = message

    def error_occurred(self):
        """
	return True if error occurred
	"""
        occ = self.__error_occurred
        self.__error_occurred = False
        return occ

    def error_message(self):
        """
	return error message
	"""
        return self.__error_message

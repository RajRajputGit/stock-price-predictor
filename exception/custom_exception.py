import sys

class CustomException(Exception):
    """
    Custom exception class to give detailed error information
    """

    def __init__(self, error_message, error_detail: sys):
        # Call parent Exception class
        super().__init__(error_message)

        # Store detailed error message
        self.error_message = self.get_detailed_error_message(
            error_message, error_detail
        )

    def get_detailed_error_message(self, error_message, error_detail: sys):
        """
        Extracts line number, file name and error message
        """
        _, _, exc_tb = error_detail.exc_info()

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        return f"""
        Error occurred in python script: [{file_name}]
        Line number: [{line_number}]
        Error message: [{error_message}]
        """

    def __str__(self):
        return self.error_message
    


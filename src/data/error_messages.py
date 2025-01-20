"""
Common error messages included by the different Value errors, raised during validation of the number to be transformed into text.
"""

from .constants import MAX_SUPPORTED_NUMBER_LENGTH

FLOATING_POINT_ERROR_MESSAGE = "Floating point numbers are not supported"

NUMBER_IS_NOT_DIGITS_ONLY = "is not a valid number. It should contain digits only."

NUMBER_TOO_LARGE = f"Number is too large. The maximum number length is {MAX_SUPPORTED_NUMBER_LENGTH} digits"

import data.constants as dc
import data.error_messages as err


class NumberToText:
    """
    A class to convert numerical values into their corresponding textual representations.

    This class takes a number (integer or string representation of a number) and converts
    it into its textual format, breaking down large numbers with readable suffixes (thousands, millions, etc.).
    The class also handles negative numbers, formatting them appropriately.
    Internal caching implemented for faster retrieval of repeating numbers (123 123 123 for example).

    Attributes:
        numerical_value (str | int): The validated numerical input.
        numerical_split_value (str): The formatted version of the number, split into groups of three digits.
        is_negative_number (bool): A flag to indicate whether the number is negative.
        _cached_values (dict): Dictionary for storing repeating three digit groups during conversion into text.
        _text_value (str): The final textual representation of the number.
    """

    @classmethod
    def validate_number(cls, number: str | int) -> str:
        """
        Validates the given number to ensure it is a valid integer or string representation of an integer.

        Args:
            number (str | int): The number to be validated.

        Raises:
            ValueError: If the number is a floating point, too large, or contains non-digit characters.

        Returns:
            str: The validated number.
        """
        if isinstance(number, float):
            raise ValueError(err.FLOATING_POINT_ERROR_MESSAGE)

        if isinstance(number, str) and not number.strip().lstrip("-").isdigit():
            raise ValueError(f"'{number}' {err.NUMBER_IS_NOT_DIGITS_ONLY}")

        if isinstance(number, str) and len(number) > dc.MAX_SUPPORTED_NUMBER_LENGTH:
            raise ValueError(err.NUMBER_TOO_LARGE)

        if isinstance(number, int) and number > dc.MAX_SUPPORTED_NUMBER:
            raise ValueError(err.NUMBER_TOO_LARGE)

        return str(number).strip()

    def __init__(self, number: str | int) -> None:
        """
        Initializes the NumberToText object and converts the number into text format.

        Args:
            number (str | int): The input number (either as an integer or string) to be converted.

        Returns:
            None
        """
        self.numerical_value: str = NumberToText.validate_number(number)
        self.numerical_split_value: str | None = None
        self.is_negative_number: bool = False
        self._cached_values: dict[str, str] = {}
        self._text_value: str = self._read_number()

    def __repr__(self) -> str:
        """
        Returns:
            str: The textual representation of the number.
        """
        return self._text_value

    def _read_number(self) -> str:
        """
        Converts the numerical value into its textual representation.

        Returns:
            str: The textual representation of the number.
        """
        if int(self.numerical_value) == 0:
            return dc.ZERO[0]

        if int(self.numerical_value) < 0:
            self.is_negative_number = True

        if self.is_negative_number:
            self.numerical_split_value = "-" + self._format_number_string(
                str(self.numerical_value).lstrip("-")
            ).strip(" ")
        else:
            self.numerical_split_value = self._format_number_string(
                str(self.numerical_value).lstrip("-")
            ).strip(" ")

        words_as_numbers_list: list[str] = self._create_text_from_number(
            self.numerical_split_value.lstrip("-")
        )

        return self._final_format(
            words_as_numbers_list, self.numerical_split_value.lstrip("-").split()
        )

    def _final_format(
        self, words_as_numbers_list: list[str], digit_groups_list: list[str]
    ):
        """
        Adds suffixes like 'thousand', 'million', etc. to the words list based on the number's magnitude.

        Beautifies the final string, adding 'and', removing or adding ',' (comma).

        Also handles the addition of 'minus' for negative numbers.

        Args:
            words_as_numbers_list (list[str]): The list of words representing each digit group.
            digits_list (list[str]): The list of digit groups (each containing up to 3 digits).

        Returns:
            str: The final formatted text.
        """
        additions = set()

        for index in range(len(words_as_numbers_list)):
            grade = len(words_as_numbers_list) - index
            plural = int(digit_groups_list[index]) > 1

            if (
                grade > 1
                and (
                    dc.LARGE[grade] + "s" not in additions
                    and dc.LARGE[grade] not in additions
                )
                and not self._all_digits_are_zeros(digit_groups_list[index])
            ):
                suffix_to_add = (
                    dc.LARGE[grade]
                    if not plural or grade == 2
                    else dc.LARGE[grade] + "s"
                )

                words_as_numbers_list[index] = (
                    words_as_numbers_list[index].strip(" ") + suffix_to_add
                )
                additions.add(suffix_to_add)

        temp_result = [
            non_empty_str
            for non_empty_str in (
                number_to_add_prefix_to.replace(
                    number_to_add_prefix_to, f"and {number_to_add_prefix_to}"
                )
                if (
                    number_to_add_prefix_to in dc.SINGLES.values()
                    or number_to_add_prefix_to in dc.UNIQUES.values()
                )
                and number_to_add_prefix_to != ""
                and len(words_as_numbers_list) > 1
                and words_as_numbers_list[0] != ""
                else number_to_add_prefix_to
                for number_to_add_prefix_to in words_as_numbers_list
            )
            if non_empty_str != ""
        ]

        if len(temp_result) >= 2:
            result = ", ".join((x.removesuffix(" ") for x in temp_result))
        else:
            result = " ".join(temp_result).strip()

        result = result.replace(", and", " and")

        if self.is_negative_number:
            return f"{dc.MINUS}, {result}"

        return result

    def _format_number_string(self, number_string: str) -> str:
        """
        Formats a given string of digits by inserting spaces after every third digit
        from the right (i.e., similar to how large numbers are formatted for readability).

        Args:
            number_string (str): The input string containing only digits.

        Returns:
            str: The formatted string where every third digit from the right is
                preceded by a space (except at the start of the string).

        Example:
            format_number_string("123456789")
            -> "123 456 789"

            format_number_string("1000000")
            -> "1 000 000"
        """

        result = [
            f" {number_string[len(number_string) - digit]}"
            if digit % 3 == 0
            else number_string[len(number_string) - digit]
            for digit in range(1, len(number_string) + 1)
        ]

        return "".join(result[::-1])

    def _create_text_from_number(self, number_text: str):
        """
        Converts a formatted number string (split into digit groups) into corresponding words.

        Args:
            number_text (str): The formatted number string with spaces separating each group of three digits.

        Returns:
            list[str]: A list of words representing each digit group.
        """
        result = []
        temp_result = number_text.split(" ")

        for substring_idx in range(len(temp_result)):
            if temp_result[substring_idx] in self._cached_values:
                result.append(self._cached_values[temp_result[substring_idx]])
            else:
                text_from_digits = self._format_digits(temp_result[substring_idx])
                self._cached_values[temp_result[substring_idx]] = text_from_digits

                result.append(text_from_digits)

        return result

    def _format_digits(self, numbers: str):
        """
        Converts a group of digits (up to 3 digits) into words.

        Args:
            numbers (str): A string representing a group of up to 3 digits.

        Returns:
            str: The textual representation of the digit group.
        """
        result = []

        if self._all_digits_are_zeros(numbers):
            return ""

        result.append(self._add_hundreds(numbers))

        return " ".join(result)

    def _all_digits_are_zeros(self, three_digit_string: str):
        """
        Checks if all digits in a string of 3 digits are zero.

        Args:
            three_digit_string (str): A string representing a group of 3 digits.

        Returns:
            bool: True if all digits are zero, False otherwise.
        """

        return len(three_digit_string) == 3 and all(
            int(digit) == 0 for digit in three_digit_string
        )

    def _add_hundreds(self, numbers: str):
        """
        Adds the word for hundreds and processes the rest of the digits (tens and ones).

        Args:
            numbers (str): A string representing up to 3 digits.

        Returns:
            str: The textual representation of the hundreds place and any remaining digits.
        """
        result: list[str] = []
        numbers = numbers.lstrip("0")

        if len(numbers) == 3:
            result.append(f"{dc.SINGLES[int(numbers[-3])]} {dc.HUNDRED}")
            result.append(self._add_decimals(numbers))
        elif len(numbers) == 2:
            result.append(self._add_decimals(numbers))
        elif len(numbers) == 1:
            result.append(self._add_singles(numbers))

        if result[0].endswith("hundred") and len(result) > 1 and result[1] != "":
            result[0] += " and"

        return " ".join(result)

    def _add_decimals(self, numbers: str):
        """
        Adds the words for the tens and ones digits.

        Args:
            numbers (str): A string representing the tens and ones digits (up to 2 digits).

        Returns:
            str: The textual representation of the tens and ones digits.
        """
        result = []
        try:
            result.append(dc.UNIQUES[int(numbers[-2:])])

        except KeyError:
            try:
                result.append(dc.DOUBLES[int(numbers[-2:])])

            except KeyError:
                try:
                    result.append(dc.DOUBLES[int(f"{numbers[-2]}0")])

                    result.append(self._add_singles(numbers))
                except Exception:
                    result.append(self._add_singles(numbers))

        finally:
            return " ".join(result)

    def _add_singles(self, numbers: str):
        """
        Adds the word for a single digit (ones place).

        Args:
            numbers (str): A string representing the ones place.

        Returns:
            str: The textual representation of the ones digit.
        """

        return dc.SINGLES[int(numbers[-1])]

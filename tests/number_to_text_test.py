import unittest
from src.number_to_text import NumberToText
from data import constants


class NumberToTextShould(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        return super().setUp()

    def test_validateNumber_raises_ValueError_withInvalidInputs(self):
        # Arrange
        invalid_numbers = [
            3.14,
            "3.14",
            constants.MAX_SUPPORTED_NUMBER + 1,
            str(constants.MAX_SUPPORTED_NUMBER + 1),
        ]

        # Act & Assert
        for number in invalid_numbers:
            with self.assertRaises(ValueError):
                _ = NumberToText(number)

    def test_numberToText_returns_correctResult_withValidStringOrInteger(self):
        # Arrange
        test_input = ["100", 100]
        expected_result = "one hundred"

        # Act & Assert
        for input in test_input:
            self.assertEqual(str(NumberToText(input)), expected_result)

    def test_numberToText_returns_correctString_for_negativeNumbers(self):
        # Arrange
        test_input = [-100, "-100"]
        expected_result = "minus, one hundred"

        # Act & Assert
        for input in test_input:
            self.assertEqual(str(NumberToText(input)), expected_result)

    def test_numberToText_returns_correctString_for_millionNumbers(self):
        # Arrange
        million_singular = constants.LARGE[3]
        million_plural = million_singular + "s"
        test_input = list(range(1000000, 10000000, 1000000))

        # Act & Assert
        for input in test_input:
            actual_result = NumberToText(input)

            if input == 1000000:
                self.assertNotIn(million_plural, str(actual_result))
                self.assertIn(million_singular, str(actual_result))
            else:
                self.assertIn(million_plural, str(actual_result))

    def test_numberToText_returns_correctString_for_billionNumbers(self):
        # Arrange
        billion_singular = constants.LARGE[4]
        billion_plural = billion_singular + "s"
        test_input = list(range(1000000000, 10000000000, 1000000000))

        # Act & Assert
        for input in test_input:
            actual_result = NumberToText(input)

            if input == 1000000000:
                self.assertNotIn(billion_plural, str(actual_result))
                self.assertIn(billion_singular, str(actual_result))
            else:
                self.assertIn(billion_plural, str(actual_result))

    def test_numberToText_returns_correctString_for_complexNumbers(self):
        # Arrange
        test_input = [9876543210, 1234567890123456789]
        expected_results = [
            "nine billions, eight hundred and seventy six millions, five hundred and forty three thousand, two hundred and ten",
            "one quintillion, two hundred and thirty four quadrillions, five hundred and sixty seven trillions, eight hundred and ninety billions, one hundred and twenty three millions, four hundred and fifty six thousand, seven hundred and eighty nine",
        ]

        # Act & Assert
        for i, input in enumerate(test_input):
            self.assertEqual(str(NumberToText(input)), expected_results[i])

    def test_numberToText_returns_correctString_for_edgeCases(self):
        # Arrange
        test_input = [101, 110, 1001, 1000001, 1100001, -1101001]
        expected_results = [
            "one hundred and one",
            "one hundred and ten",
            "one thousand and one",
            "one million and one",
            "one million, one hundred thousand and one",
            "minus, one million, one hundred and one thousand and one",
        ]

        # Act & Assert
        for i, input in enumerate(test_input):
            self.assertEqual(str(NumberToText(input)), expected_results[i])

    def test_numberToText_returns_correctString_for_negativeLargeNumbers(self):
        # Arrange
        test_input = [-123, -987654321]
        expected_results = [
            "minus, one hundred and twenty three",
            "minus, nine hundred and eighty seven millions, six hundred and fifty four thousand, three hundred and twenty one",
        ]

        # Act & Assert
        for i, input in enumerate(test_input):
            self.assertEqual(str(NumberToText(input)), expected_results[i])

    def test_numberToText_returns_correctString_for_teens_and_tens(self):
        # Arrange
        test_input = [11, 15, 19, 20, 30, 99]
        expected_results = [
            "eleven",
            "fifteen",
            "nineteen",
            "twenty",
            "thirty",
            "ninety nine",
        ]

        # Act & Assert
        for i, input in enumerate(test_input):
            self.assertEqual(str(NumberToText(input)), expected_results[i])

    def test_numberToText_returns_correctString_for_hundredsAndThousands(self):
        # Arrange
        test_input = [300, 4567, 789012]
        expected_results = [
            "three hundred",
            "four thousand, five hundred and sixty seven",
            "seven hundred and eighty nine thousand and twelve",
        ]

        # Act & Assert
        for i, input in enumerate(test_input):
            self.assertEqual(str(NumberToText(input)), expected_results[i])

    def test_numberToText_handles_numbers_withLeadingZeros_andSpaces(self):
        # Arrange
        test_input = ["000123", "  456  ", "   -456   ", "000123000"]
        expected_results = [
            "one hundred and twenty three",
            "four hundred and fifty six",
            "minus, four hundred and fifty six",
            "one hundred and twenty three thousand",
        ]

        # Act & Assert
        for i, input in enumerate(test_input):
            self.assertEqual(str(NumberToText(input)), expected_results[i])

    def test_numberToText_returns_correctString_for_maximumSupportedNumber(self):
        # Arrange
        max_supported_number = constants.MAX_SUPPORTED_NUMBER
        expected_result = "nine hundred and ninety nine septillions, nine hundred and ninety nine sextillions, nine hundred and ninety nine quintillions, nine hundred and ninety nine quadrillions, nine hundred and ninety nine trillions, nine hundred and ninety nine billions, nine hundred and ninety nine millions, nine hundred and ninety nine thousand, nine hundred and ninety nine"
        expected_negative_result = f"{constants.MINUS}, {expected_result}"
        # Act
        actual_result = NumberToText(max_supported_number)
        actual_negative_result = NumberToText(-max_supported_number)

        # Assert
        self.assertEqual(expected_result, str(actual_result))
        self.assertEqual(expected_negative_result, str(actual_negative_result))

    def test_numberToText_returns_correctString_for_smallNumbers(self):
        # Arrange
        test_input = [0, "0", -1, "-1", -0]
        expected_results = ["zero", "zero", "minus, one", "minus, one", "zero"]

        # Act & Assert
        for i, input in enumerate(test_input):
            self.assertEqual(str(NumberToText(input)), expected_results[i])

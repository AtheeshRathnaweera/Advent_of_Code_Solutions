import re

LETTER_NUMS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


class Main:
    def __init__(self):
        self.input_file_path = "input.txt"

    def get_the_two_digit_num(self, nums_info):
        nums_info.sort(key=lambda x: x[0])

        first_digit = nums_info[0][1]
        second_digit = nums_info[-1][1]

        return int(f"{first_digit}{second_digit}")

    def find_the_digits_with_index(self, text):
        pattern = r"\d{1}"
        matches = re.finditer(pattern, text)
        results = []

        for match in matches:
            index = match.start()
            number = int(match.group())
            results.append((index, number))

        return results

    def find_the_letter_nums_with_index(self, text):
        results = []
        for letter_num, num in LETTER_NUMS.items():
            pattern = f"{letter_num}"
            matches = re.finditer(pattern, text)

            for match in matches:
                index = match.start()
                number = int(num)
                results.append((index, number))

        return results

    def process_the_input_file(self):
        sum_of_digits = 0
        with open(self.input_file_path, "r", encoding="utf-8") as file:
            for line in file:
                formatted_text = line.strip().lower()
                nums_info = []

                digits_info = self.find_the_digits_with_index(formatted_text)
                letter_nums_info = self.find_the_letter_nums_with_index(formatted_text)

                nums_info.extend(digits_info)
                nums_info.extend(letter_nums_info)

                two_digit_number = self.get_the_two_digit_num(nums_info)

                sum_of_digits += two_digit_number

        return sum_of_digits

    def main(self):
        sum_of_digits = self.process_the_input_file()
        print("Sum of all of the calibration values: ", sum_of_digits)


if __name__ == "__main__":
    main = Main()
    main.main()

import json


class Main:
    def __init__(self):
        self.input_file_path = "input.txt"
        self.lines = []
        self.line_length = 0
        self.lines_info = []
        self.gears = []
        self.unique_gears = []

    def is_star_adjacent_to_number(
        self,
        star_index,
        line_of_stars,
        indices_around,
        checking_num_info,
        first_num_info,
    ):
        if star_index in indices_around:
            return {
                "first_num": {
                    "value": first_num_info["number"],
                    "starting_index": first_num_info["starting_index"],
                    "line_index": first_num_info["line_index"],
                },
                "second_num": {
                    "value": checking_num_info["number"],
                    "starting_index": checking_num_info["starting_index"],
                    "line_index": checking_num_info["line_index"],
                },
                "star_index": {"index": star_index, "line_index": line_of_stars},
            }
        return None

    def get_total_of_gears(self):
        self.find_gears()
        self.find_unique_gears()

        # get the total
        total = 0
        for gear in self.unique_gears:
            # print(f"{gear['first_num']['value']} * {gear['second_num']['value']}")
            total += int(gear["first_num"]["value"]) * int(gear["second_num"]["value"])

        return total

    def find_unique_gears(self):
        # order the first num and the second num of the gear by line and starting index
        for gear in self.gears:
            # get the first num
            first_num = gear["first_num"]
            second_num = gear["second_num"]

            if first_num["line_index"] > second_num["line_index"]:
                gear["first_num"] = second_num
                gear["second_num"] = first_num
            elif first_num["line_index"] == second_num["line_index"] and (
                first_num["starting_index"] > second_num["starting_index"]
            ):
                gear["first_num"] = second_num
                gear["second_num"] = first_num

        # remove duplicates
        seen_entries = set()
        for gear in self.gears:
            gear_hash = hash(json.dumps(gear))

            if gear_hash not in seen_entries:
                seen_entries.add(gear_hash)
                self.unique_gears.append(gear)

    def is_star_adjacent_to_number_on_another_line(
        self,
        next_line_index,
        first_num_info,
        stars_indices,
        line_of_stars,
        positions_to_check,
    ):
        found_nums = []
        for star_index in stars_indices:
            nums_in_next_line = self.lines_info[next_line_index]["nums"]
            for num_info in nums_in_next_line:
                for position in positions_to_check:
                    found_num = self.is_star_adjacent_to_number(
                        star_index,
                        line_of_stars,
                        num_info["indices_around"][position],
                        num_info,
                        first_num_info,
                    )
                    if found_num is not None:
                        found_nums.append(found_num)
        return found_nums

    def is_star_adjacent_to_number_on_side(
        self, first_num_info, stars_indices, line_of_stars, num_info_to_check, position
    ):
        for star_index in stars_indices:
            return self.is_star_adjacent_to_number(
                star_index,
                line_of_stars,
                num_info_to_check["indices_around"][position],
                num_info_to_check,
                first_num_info,
            )
        return None

    def find_gears(self):
        for line_index, line_info in enumerate(self.lines_info):
            for num_index, num_info in enumerate(line_info["nums"]):
                num_on_left = None
                num_on_right = None
                top_line_index = None
                second_top_line_index = None
                bottom_line_index = None
                second_bottom_line_index = None

                if num_index - 1 > -1:
                    num_on_left = line_info["nums"][num_index - 1]

                if num_index + 1 < len(line_info["nums"]):
                    num_on_right = line_info["nums"][num_index + 1]

                if line_index - 1 > -1:
                    top_line_index = line_index - 1

                if line_index + 1 < len(self.lines_info):
                    bottom_line_index = line_index + 1

                if line_index - 2 > -1:
                    second_top_line_index = line_index - 2

                if line_index + 2 < len(self.lines_info):
                    second_bottom_line_index = line_index + 2

                # indices on sides
                side_indices = num_info["indices_around"]["current_line"]
                star_indices_on_sides = set(side_indices) & set(
                    line_info["star_indices"]
                )

                # indices on sides - numbers in the current line
                if num_on_left is not None:
                    found_left_num_data = self.is_star_adjacent_to_number_on_side(
                        num_info,
                        star_indices_on_sides,
                        line_index,
                        num_on_left,
                        "current_line",
                    )
                    if found_left_num_data is not None:
                        self.gears.append(found_left_num_data)

                if num_on_right is not None:
                    found_right_num_data = self.is_star_adjacent_to_number_on_side(
                        num_info,
                        star_indices_on_sides,
                        line_index,
                        num_on_right,
                        "current_line",
                    )
                    if found_right_num_data is not None:
                        self.gears.append(found_right_num_data)

                # indices on sides - bottom of top line number
                if top_line_index is not None:
                    found_nums = self.is_star_adjacent_to_number_on_another_line(
                        top_line_index,
                        num_info,
                        star_indices_on_sides,
                        line_index,
                        ["bottom_line"],
                    )
                    if found_nums is not None:
                        self.gears.extend(found_nums)

                # indices on sides - top of bottom line number
                if bottom_line_index is not None:
                    found_nums = self.is_star_adjacent_to_number_on_another_line(
                        bottom_line_index,
                        num_info,
                        star_indices_on_sides,
                        line_index,
                        ["top_line"],
                    )
                    if found_nums is not None:
                        self.gears.extend(found_nums)

                # indices on top
                top_indices = num_info["indices_around"]["top_line"]

                if top_line_index is not None:
                    star_indices_on_top = set(top_indices) & set(
                        self.lines_info[top_line_index]["star_indices"]
                    )

                    # indices on top - top of the left number
                    if num_on_left is not None:
                        found_left_num_data = self.is_star_adjacent_to_number_on_side(
                            num_info,
                            star_indices_on_top,
                            top_line_index,
                            num_on_left,
                            "top_line",
                        )
                        if found_left_num_data is not None:
                            self.gears.append(found_left_num_data)

                    # indices on top - top of the right number
                    if num_on_right is not None:
                        found_right_num_data = self.is_star_adjacent_to_number_on_side(
                            num_info,
                            star_indices_on_top,
                            top_line_index,
                            num_on_right,
                            "top_line",
                        )
                        if found_right_num_data is not None:
                            self.gears.append(found_right_num_data)

                    # indices on top - sides of top line number
                    found_nums = self.is_star_adjacent_to_number_on_another_line(
                        top_line_index,
                        num_info,
                        star_indices_on_top,
                        top_line_index,
                        ["current_line"],
                    )
                    if found_nums is not None:
                        self.gears.extend(found_nums)

                # indices on top - bottom of second top line number
                if second_top_line_index is not None:
                    star_indices_on_top = set(top_indices) & set(
                        self.lines_info[top_line_index]["star_indices"]
                    )
                    found_nums = self.is_star_adjacent_to_number_on_another_line(
                        second_top_line_index,
                        num_info,
                        star_indices_on_top,
                        top_line_index,
                        ["bottom_line"],
                    )
                    if found_nums is not None:
                        self.gears.extend(found_nums)

                # indices on bottom
                bottom_indices = num_info["indices_around"]["bottom_line"]

                if bottom_line_index is not None:
                    star_indices_on_bottom = set(bottom_indices) & set(
                        self.lines_info[bottom_line_index]["star_indices"]
                    )

                    # indices on bottom - bottom of the left number
                    if num_on_left is not None:
                        found_left_num_data = self.is_star_adjacent_to_number_on_side(
                            num_info,
                            star_indices_on_bottom,
                            bottom_line_index,
                            num_on_left,
                            "bottom_line",
                        )
                        if found_left_num_data is not None:
                            self.gears.append(found_left_num_data)

                    # indices on bottom - bottom of the right number
                    if num_on_right is not None:
                        found_right_num_data = self.is_star_adjacent_to_number_on_side(
                            num_info,
                            star_indices_on_bottom,
                            bottom_line_index,
                            num_on_right,
                            "bottom_line",
                        )
                        if found_right_num_data is not None:
                            self.gears.append(found_right_num_data)

                    # indices on bottom - sides of bottom line number
                    found_nums_sob = self.is_star_adjacent_to_number_on_another_line(
                        bottom_line_index,
                        num_info,
                        star_indices_on_bottom,
                        bottom_line_index,
                        ["current_line"],
                    )
                    if found_nums_sob is not None:
                        self.gears.extend(found_nums_sob)

                # indices on bottom - top of second bottom line number
                if second_bottom_line_index is not None:
                    star_indices_on_bottom = set(bottom_indices) & set(
                        self.lines_info[bottom_line_index]["star_indices"]
                    )
                    found_nums = self.is_star_adjacent_to_number_on_another_line(
                        second_bottom_line_index,
                        num_info,
                        star_indices_on_bottom,
                        bottom_line_index,
                        ["top_line"],
                    )
                    if found_nums is not None:
                        self.gears.extend(found_nums)

                # print(str(num_info))

    def is_symbols_present(self, line_info, indices_to_check):
        if line_info is None:
            return False

        for check_index in indices_to_check:
            if check_index in line_info["symbol_indices"]:
                return True

        return False

    def find_line_info_by_index(self, index):
        for line_info in self.lines_info:
            if line_info["index"] == index:
                return line_info
        return None

    def get_total_of_part_numbers(self):
        part_num_total = 0
        part_num_count = 0

        for line_info in self.lines_info:
            # loop through nums
            for num_info in line_info["nums"]:
                indices_for_check = num_info["indices_around"]

                # checking for symbols
                # on top row
                top_row_index = line_info["index"] - 1
                top_line_info = self.find_line_info_by_index(top_row_index)
                symbol_in_top_line = self.is_symbols_present(
                    top_line_info, indices_for_check["top_line"]
                )
                if symbol_in_top_line:
                    part_num_total += int(num_info["number"])
                    part_num_count += 1
                    continue

                # on bottom row
                bottom_row_index = line_info["index"] + 1
                bottom_line_info = self.find_line_info_by_index(bottom_row_index)
                symbol_in_bottom_line = self.is_symbols_present(
                    bottom_line_info, indices_for_check["bottom_line"]
                )
                if symbol_in_bottom_line:
                    part_num_total += int(num_info["number"])
                    part_num_count += 1
                    continue

                # sides
                symbol_in_current_line = self.is_symbols_present(
                    line_info, indices_for_check["current_line"]
                )
                if symbol_in_current_line:
                    part_num_total += int(num_info["number"])
                    part_num_count += 1
                    continue

        return part_num_total

    def find_indices_to_check(self, starting_index, ending_index, number):
        num_length = len(number)
        top_bottom_line_range = num_length + 2

        indices_for_check = {
            "top_line": [],
            "current_line": [],
            "bottom_line": [],
        }

        # get indices on top row
        for top_bottom_index in range(top_bottom_line_range):
            pos = top_bottom_index - 1
            index = starting_index + pos
            indices_for_check["top_line"].append(index)
            indices_for_check["bottom_line"].append(index)

        # sides
        left_side_index = starting_index - 1
        right_side_index = ending_index + 1
        indices_for_check["current_line"].extend([left_side_index, right_side_index])

        return indices_for_check

    def prepare_num_info_dict(self, line_index, starting_index, ending_index, number):
        return {
            "line_index": line_index,
            "starting_index": starting_index,
            "ending_index": ending_index,
            "number": number,
            "indices_around": self.find_indices_to_check(
                starting_index, ending_index, number
            ),
        }

    def is_star(self, char):
        return char == "*"

    # Function to check if a character is a symbol (excluding periods)
    def is_symbol(self, char):
        # Check if the character is neither alphabetic nor numeric, and is not a period
        return not (char.isalpha() or char.isnumeric() or char == "." or char == "\n")

    def get_symbols_and_nums_in_each_line(self):
        lines = []
        for line_index, line_txt in enumerate(self.lines):
            line_info = {
                "index": line_index,
                "symbol_indices": [],
                "nums": [],
                "star_indices": [],
            }
            is_prev_numeric = False
            is_current_numeric = False
            starting_index = None
            ending_index = None
            current_number = ""

            for char_index, char in enumerate(line_txt):
                if self.is_symbol(char):
                    line_info["symbol_indices"].append(char_index)

                    if self.is_star(char):
                        line_info["star_indices"].append(char_index)

                    is_current_numeric = False
                elif char.isnumeric():
                    if not is_prev_numeric:
                        is_prev_numeric = True
                        starting_index = char_index

                    ending_index = char_index
                    is_current_numeric = True
                    current_number += char
                else:
                    is_current_numeric = False

                if current_number != "" and not is_current_numeric:
                    line_info["nums"].append(
                        self.prepare_num_info_dict(
                            line_index, starting_index, ending_index, current_number
                        )
                    )
                    is_prev_numeric = False
                    is_current_numeric = False
                    starting_index = None
                    ending_index = None
                    current_number = ""

            if current_number != "":
                line_info["nums"].append(
                    self.prepare_num_info_dict(
                        line_index, starting_index, ending_index, current_number
                    )
                )

            lines.append(line_info)

        return lines

    def get_lines_of_the_file(self):
        with open(self.input_file_path, "r", encoding="utf-8") as file:
            # Read all lines from the file and strip newline characters
            return [line.rstrip() for line in file]

    def main(self):
        self.lines.extend(self.get_lines_of_the_file())
        self.line_length = len(self.lines[0])
        self.lines_info.extend(self.get_symbols_and_nums_in_each_line())

        sum_part_nums = self.get_total_of_part_numbers()
        sum_gears = self.get_total_of_gears()

        print(f"total lines: {len(self.lines)} | line length: {self.line_length}")
        print("PART 01: " + str(sum_part_nums))
        print("PART 02: " + str(sum_gears))


if __name__ == "__main__":
    main = Main()
    main.main()

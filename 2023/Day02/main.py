import re

class Main:
    def __init__(self):
        self.input_file_path = "input.txt"
        self.games_info = []

    def get_part_02_results(self):
        # get the power of fewest numbers of cubes to a possible game
        total_of_powers = 0

        for game_info in self.games_info:
            highest_values = [0, 0, 0]

            for record in game_info["records"]:
                for index, value in enumerate(record):
                    if value is not None and value > highest_values[index]:
                        highest_values[index] = value

            # get the multiplication
            result = 1
            for value in highest_values:
                if value != 0:
                    result = result * value

            total_of_powers += result

        print("Part 02 results: " + str(total_of_powers))

    def get_part_01_results(self):
        # get the total of IDs of possible games.
        expected_config = [12, 13, 14]
        total_of_ids = 0

        for game_info in self.games_info:
            possible_game = True

            for record in game_info["records"]:
                go_to_next_record = True
                for index, _ in enumerate(record):
                    if (
                        record[index] is not None
                        and record[index] > expected_config[index]
                    ):
                        go_to_next_record = False
                        possible_game = False
                        break

                if not go_to_next_record:
                    break

            if possible_game:
                total_of_ids += int(game_info["game_id"])

        print("Part 01 results: " + str(total_of_ids))

    def get_sets_info(self, record_text):
        results = []
        colors = ["red", "green", "blue"]

        sets_text = record_text.split(";")

        for set_text in sets_text:
            cubes_text = set_text.split(",")
            set_record = [None, None, None]

            for cube_text in cubes_text:
                cube_record_index = None
                # identify the color
                for index, color in enumerate(colors):
                    if color in cube_text:
                        cube_record_index = index
                        break

                if cube_record_index is not None:
                    # get the amount
                    amount = re.findall(r"\d+", cube_text)
                    set_record[cube_record_index] = int(amount[0])

            results.append(set_record)
        return results

    def get_the_game_id(self, text):
        numbers = re.findall(r"\d+", text)
        return int(numbers[0])

    def process(self):
        with open(self.input_file_path, "r", encoding="utf-8") as file:
            for line in file:
                stripped_text = line.strip()
                main_parts = stripped_text.split(":")

                game_id = self.get_the_game_id(main_parts[0])
                sets_record = self.get_sets_info(main_parts[1])

                self.games_info.append({"game_id": game_id, "records": sets_record})

    def main(self):
        self.process()
        self.get_part_01_results()
        self.get_part_02_results()
        # print(self.games_info)
        # print("Sum of all of the calibration values: ", sum_of_ids)


if __name__ == "__main__":
    main = Main()
    main.main()

import re


class Main:
    def __init__(self):
        self.input_file_path = "input.txt"
        self.cards_info = []
        self.cards_and_copies = []

    def get_sum_of_scratch_cards_amount(self):
        return sum(card[1] for card in self.cards_and_copies)

    def increment_total_cards_amount(self, starting_index, ending_index, amount):
        for index in range(starting_index, ending_index):
            self.cards_and_copies[index][1] += amount

    def prepare_the_cards_copies_list(self):
        for card_info in self.cards_info:
            self.cards_and_copies.append([card_info["id"], 1])

    def calculate_total_scratch_cards(self):
        self.prepare_the_cards_copies_list()
        for card_index, card_info in enumerate(self.cards_info):
            matchings_count = card_info["matchings_count"]
            current_amount = self.cards_and_copies[card_index][1]
            next_index = card_index + 1
            self.increment_total_cards_amount(
                next_index, next_index + matchings_count, current_amount
            )
        return self.get_sum_of_scratch_cards_amount()

    def calculate_the_card_total(self):
        total_points = 0
        for card_info in self.cards_info:
            card_points = 0
            matching_count = 0
            for num in card_info["card_nums"]:
                if num in card_info["winning_nums"]:
                    if card_points == 0:
                        card_points = 1
                    else:
                        card_points *= 2
                    matching_count += 1
            card_info["matchings_count"] = matching_count
            total_points += card_points
        return total_points

    def get_nums_from_space_separated_string(self, num_string):
        nums_list = [int(num) for num in num_string.split()]
        return tuple(nums_list)

    def get_winninng_and_card_nums(self, num_part):
        all_num_parts = num_part.split("|")

        winning_nums = self.get_nums_from_space_separated_string(all_num_parts[0])
        card_nums = self.get_nums_from_space_separated_string(all_num_parts[1])

        return winning_nums, card_nums

    def get_the_card_id(self, text):
        numbers = re.findall(r"\d+", text)
        return int(numbers[0])

    def read_the_input_file(self):
        with open(self.input_file_path, "r", encoding="utf-8") as file:
            for line in file:
                stripped_text = line.strip()
                card_parts = stripped_text.split(":")

                card_id = self.get_the_card_id(card_parts[0])
                winning_nums, card_nums = self.get_winninng_and_card_nums(card_parts[1])

                self.cards_info.append(
                    {
                        "id": card_id,
                        "winning_nums": winning_nums,
                        "card_nums": card_nums,
                        "matchings_count": 0,
                    }
                )

    def main(self):
        self.read_the_input_file()
        total_points = self.calculate_the_card_total()

        total_cards = self.calculate_total_scratch_cards()
        print(f"\nPART 01: {str(total_points)}")
        print(f"PART 02: {str(total_cards)}")


if __name__ == "__main__":
    main = Main()
    main.main()

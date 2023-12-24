import time
from collections import Counter


class Main:
    def __init__(self):
        self.input_file_name = "inputs/input.txt"
        self.cards = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        self.input = []
        self.grouped = {
            "high_card": [],
            "one_pair": [],
            "two_pair": [],
            "three_of_a_kind": [],
            "full_house": [],
            "four_of_kind": [],
            "five_of_kind": [],
        }
        self.card_strengths = {}

    def get_sorted_group(self, group):
        return sorted(group, key=lambda x: x[1])

    def get_total_winnings(self):
        considered_items = 0
        total_winnings = 0
        for key, group_vals in self.grouped.items():
            sorted_group = self.get_sorted_group(group_vals)

            for index, (_, _, bid) in enumerate(
                sorted_group, start=considered_items
            ):
                total_winnings += bid * (index + 1)

            considered_items += len(sorted_group)

        return total_winnings

    def get_strength_mapping_for_hand(self, hand):
        return tuple(self.card_strengths[char] for char in hand)

    def find_the_type(self, value, apply_joker_rule):
        hand, bid = value
        unique_char_length = len(set(hand.lower()))
        letter_counts = Counter(c.lower() for c in hand)
        sorted_letter_counts = sorted(letter_counts.values(), reverse=True)
        strength_mapping = self.get_strength_mapping_for_hand(hand)

        # applying joker rule
        if apply_joker_rule and "j" in letter_counts:
            # new_letter_counts = letter_counts.copy()
            # print(f"\nletter counts: {letter_counts}")
            # get the highest key
            most_common_key, count = letter_counts.most_common(1)[0]
            j_count = letter_counts["j"]
            j_replacement = None
            new_j_count = 0

            if most_common_key == "j":
                if unique_char_length == 1:
                    j_replacement = "a"
                    # add a new key with the strongest card
                    new_j_count = j_count
                else:
                    # get the second most common
                    (
                        second_most_common_key,
                        second_key_count,
                    ) = letter_counts.most_common(2)[1]
                    j_replacement = second_most_common_key
                    new_j_count = second_key_count + j_count
            else:
                j_replacement = most_common_key
                new_j_count = count + j_count

            letter_counts[j_replacement] = new_j_count

            # remove 'j' from the new counter
            del letter_counts["j"]
            # print(f"updated counter: {letter_counts}")
            # update the hand
            updated_hand = hand.replace("J", j_replacement.upper())
            # print(f"updated hand: {updated_hand}")
            # update the unique_char_length, sorted_letter_counts
            unique_char_length = len(set(updated_hand.lower()))
            # print(f"updated unique_char_length: {unique_char_length}")
            sorted_letter_counts = sorted(letter_counts.values(), reverse=True)
            # print(f"updated sorted letter counts: {sorted_letter_counts}")
            strength_mapping = self.get_strength_mapping_for_hand(hand)

        if unique_char_length == 1:
            hand_type = "five_of_kind"
        elif unique_char_length == 2 and sorted_letter_counts == [4, 1]:
            hand_type = "four_of_kind"
        elif unique_char_length == 2 and sorted_letter_counts == [3, 2]:
            hand_type = "full_house"
        elif unique_char_length == 3 and sorted_letter_counts == [3, 1, 1]:
            hand_type = "three_of_a_kind"
        elif unique_char_length == 3 and sorted_letter_counts == [2, 2, 1]:
            hand_type = "two_pair"
        elif unique_char_length == 4 and sorted_letter_counts == [2, 1, 1, 1]:
            hand_type = "one_pair"
        else:
            hand_type = "high_card"

        return [hand_type, (hand, strength_mapping, bid)]

    def group_input_data(self, apply_joker_rule):
        for item in self.input:
            type_data = self.find_the_type(item, apply_joker_rule)
            # print(f"rec type data: {type_data}")
            self.grouped[type_data[0]].append(type_data[1])

    def populate_card_strength_dict(self):
        self.card_strengths = {card: index + 2 for index, card in enumerate(self.cards)}

    def read_input_files(self):
        with open(self.input_file_name, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.split()
                self.input.append((parts[0], int(parts[1])))

    def get_part_02_res(self):
        # update strengths
        self.card_strengths["J"] = 1
        print(f"\ncard strengths: {self.card_strengths}")
        # empty the grouped data
        for key, item in self.grouped.items():
            item.clear()
        self.group_input_data(True)
        part_02_res = self.get_total_winnings()
        print(f"\nPart 02 -> {part_02_res}")

    def get_part_01_res(self):
        print(f"card strengths: {self.card_strengths}")
        self.group_input_data(False)
        part_01_res = self.get_total_winnings()
        print(f"\nPart 01 -> {part_01_res}")

    def main(self):
        self.read_input_files()
        self.populate_card_strength_dict()
        self.get_part_01_res()
        self.get_part_02_res()


if __name__ == "__main__":
    start_time = time.time()
    main = Main()
    main.main()
    end_time = time.time()
    print("\nExecution time(s): ", end_time - start_time)

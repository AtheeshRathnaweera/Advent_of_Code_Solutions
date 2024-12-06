from collections import Counter
import re
from typing import List


class Main:
    def __init__(self, input_file_path: str = "input.txt"):
        self.input_file_path = input_file_path
        self.left_list: List[int] = []
        self.right_list: List[int] = []
        self.right_list_counts: Counter[int] = Counter()

    def get_similarity_score(self) -> int:
        """Calculate the similarity score based on occurrences in the right list."""
        # count right list elements
        self.right_list_counts.update(self.right_list)
        # calculate the number of occurences in the right list
        return sum(
            left_item * self.right_list_counts.get(left_item, 0)
            for left_item in self.left_list
        )

    def get_total_distance(self) -> int:
        """Calculate the total distance between corresponding items in the lists."""
        # as both the lists are same in size
        return sum(
            abs(right_item - left_item)
            for left_item, right_item in zip(self.left_list, self.right_list)
        )

    def process_the_input_file(self) -> None:
        """Read and process the input file, populating and sorting the lists."""
        with open(self.input_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # read each line
                trimmed_line = re.sub(r"\s+", " ", line.strip())
                values = list(map(int, trimmed_line.split(" ")))

                # populate the lists
                if len(values) >= 2:
                    self.left_list.append(values[0])
                    self.right_list.append(values[1])

        # sort the lists separately
        self.left_list.sort()
        self.right_list.sort()

    def main(self) -> None:
        """Main execution method."""
        self.process_the_input_file()

        total = self.get_total_distance()
        print(f"Q01 Result: {total}")

        score = self.get_similarity_score()
        print(f"Q02 Result: {score}")

if __name__ == '__main__':
    main = Main()
    main.main()

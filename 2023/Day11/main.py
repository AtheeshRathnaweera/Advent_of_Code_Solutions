import time
import pandas as pd


class Main:
    def __init__(self):
        self.input_file = "inputs/original.txt"
        self.universe_df = None
        self.empty = {"rows": [], "columns": []}
        self.galaxies_pairs = []
        self.galaxies_pairs_with_empty_counts = []

    def find_empty_counts_within_pairs(self):
        for element_01, element_02 in self.galaxies_pairs:
            # count empty rows between the rows
            # rows_range = [element_01[0], element_02[0]]
            min_row = min(element_01[0], element_02[0])
            max_row = max(element_01[0], element_02[0])
            rows_count = sum(
                min_row <= value <= max_row for value in self.empty["rows"]
            )
            # count empty columns between the columns
            min_column = min(element_01[1], element_02[1])
            max_column = max(element_01[1], element_02[1])
            columns_count = sum(
                min_column <= value <= max_column for value in self.empty["columns"]
            )
            # print(f"{element_01, element_02} -> {rows_count, columns_count}")
            self.galaxies_pairs_with_empty_counts.append(
                ((element_01, element_02), rows_count, columns_count)
            )

        # print(self.galaxies_pairs_with_empty_counts)

    def find_shortest_paths(self, expansion_scale):
        total_shortest_steps = 0
        for (
            (element_01, element_02),
            empty_rows,
            empty_columns,
        ) in self.galaxies_pairs_with_empty_counts:
            rows_diff = abs(element_02[0] - element_01[0])
            columns_diff = abs(element_02[1] - element_01[1])

            rows_diff = rows_diff + (empty_rows * (expansion_scale - 1))
            columns_diff = columns_diff + (empty_columns * (expansion_scale - 1))

            nav_max_columns = 0
            nav_remaining_steps = 0
            total_steps = 0

            if rows_diff == 0:
                total_steps = columns_diff
            elif columns_diff == 0:
                total_steps = rows_diff
            else:
                nav_max_columns = min(rows_diff, columns_diff)
                nav_remaining_steps = max(rows_diff, columns_diff) - nav_max_columns
                total_steps = (nav_max_columns * 2) + nav_remaining_steps

            # print((element_01, element_02), empty_rows, empty_columns)

            # shortest_steps.append(total_steps)
            total_shortest_steps += total_steps
            # print(f"{element_01, element_02} -> {total_steps}")

        # print(shortest_steps)
        # print(f"\ntotal shorted steps: {total_shortest_steps}")
        return total_shortest_steps

    def find_pairs(self):
        indices_of_hash = (
            self.universe_df.stack().where(lambda x: x == "#").dropna().index
        )
        for index, coords in enumerate(indices_of_hash):
            for inner_coord in indices_of_hash[index + 1 :]:
                self.galaxies_pairs.append((coords, inner_coord))

        # find the pairs
        print(f"\npairs length: {len(self.galaxies_pairs)}\n")

    def find_empty_row_columns_indices(self):
        # get the row indices which don't have any galaxies
        rows_without_hash = list(
            self.universe_df[
                ~self.universe_df.applymap(lambda x: "#" == x).any(axis=1)
            ].index
        )
        # print(f"\nRow indices without '#': \n{rows_without_hash}\n")
        self.empty["rows"].extend(rows_without_hash)

        columns_without_hash = self.universe_df.columns[
            ~(self.universe_df == "#").any()
        ]
        # print("\nColumn indices without '#':", columns_without_hash)
        self.empty["columns"].extend(columns_without_hash)

    def read_input_files(self):
        with open(self.input_file, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
        self.universe_df = pd.DataFrame([list(line) for line in lines])

    def main(self):
        self.read_input_files()
        print(self.universe_df)
        self.find_empty_row_columns_indices()
        self.find_pairs()
        self.find_empty_counts_within_pairs()
        part_01_res = self.find_shortest_paths(2)
        print(f"Part 01 -> {part_01_res}")
        part_02_res = self.find_shortest_paths(1000000)
        print(f"Part 02 -> {part_02_res}")


if __name__ == "__main__":
    start_time = time.time()
    main = Main()
    main.main()
    end_time = time.time()
    print("\nExecution time(s): ", end_time - start_time)

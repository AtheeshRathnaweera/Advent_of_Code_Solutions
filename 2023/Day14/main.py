import time
import pandas as pd


class Main:
    def __init__(self):
        self.input_file = "inputs/original.txt"
        self.platform_df = None

    def get_col_load_sum(self, range_start, range_end, row_count):
        col_load_sum = 0
        # indices of 0s after slided to north
        for zero_index in range(range_start, range_end):
            print(f"{zero_index} -> {row_count - zero_index}")
            col_load_sum += row_count - zero_index

        return col_load_sum

    def get_indices_range_between_hash(self, indices_of_hash, total_rows):
        ranges = []
        prev_index = -1

        for index in indices_of_hash:
            ranges.append((prev_index + 1, index))
            prev_index = index

        # set the range of the last element
        ranges.append((prev_index + 1, total_rows - 1))
        return ranges

    def process(self):
        print("\n")
        row_count = len(self.platform_df)
        load_sum = 0
        for col_name, col_data in self.platform_df.items():
            print("----------------------------------")
            print(col_data)
            indices_of_hash = col_data.index[col_data == "#"].tolist()
            ranges = None
            col_load_sum = 0

            if len(indices_of_hash) > 0:
                ranges = self.get_indices_range_between_hash(indices_of_hash, row_count)
                print(ranges)
                print("\nrows in range")

                # find no of 0s between the ranges
                for indices_range in ranges:
                    print(f"\n{indices_range}")
                    rows_in_range = self.platform_df.loc[
                        indices_range[0] : indices_range[1], col_name
                    ]
                    print(rows_in_range)
                    # get num of 0s
                    zero_count = (rows_in_range == "O").sum()
                    print(f"zero count: {zero_count}")

                    col_load_sum += self.get_col_load_sum(
                        indices_range[0], indices_range[0] + zero_count, row_count
                    )
            else:
                print("no hash found")
                zero_count = (col_data == "O").sum()
                print(f"found zero count: {zero_count}")

                col_load_sum += self.get_col_load_sum(0, zero_count, row_count)

            print(f"\nCol load sum: {col_load_sum}")

            load_sum += col_load_sum

            # print(indices_of_hash)
        print(f"Part 01: {load_sum}")

    def read_input_file(self):
        with open(self.input_file, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            self.platform_df = pd.DataFrame([list(line) for line in lines])
        print(self.platform_df)

    def main(self):
        print("Started")
        self.read_input_file()
        self.process()


if __name__ == "__main__":
    # pd.set_option("display.max_columns", None)
    # pd.set_option("display.width", 900)
    start_time = time.time()
    main = Main()
    main.main()
    end_time = time.time()
    print("\nExecution time(s): ", end_time - start_time)

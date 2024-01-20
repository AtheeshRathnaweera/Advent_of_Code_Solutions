import time
import pandas as pd


class Main:
    def __init__(self):
        self.input_file = "inputs/original.txt"
        self.patterns = []

    def calculate_results(self, results, original_df, expected_df, index):
        flat_original_df = original_df.values.flatten()
        flat_expected_df = expected_df.values.flatten()
        unmatching_count = (flat_original_df != flat_expected_df).sum().sum()

        if unmatching_count == 0:
            results[0] = index

        if unmatching_count == 1:
            results[1] = index

    def is_horizontal_reflect(self, df):
        num_rows = len(df)
        results = [None, None]

        for row_index in range(1, num_rows):
            # divide the df into two parts
            top_df = df.iloc[:row_index]
            bottom_df = df.iloc[row_index:]

            top_df_size = len(top_df)
            bottom_df_size = len(bottom_df)

            # update the row indices of the bottom df to start from 0
            bottom_df.reset_index(drop=True, inplace=True)

            original_df = None
            expected_df = None

            if top_df_size <= bottom_df_size:
                original_df = top_df
                expected_df = bottom_df.iloc[:top_df_size]
                # reverse the rows order
                expected_df = expected_df.iloc[::-1]
            else:
                original_df = bottom_df
                expected_df = top_df.iloc[top_df_size - bottom_df_size :]
                # reverse the rows order
                expected_df = expected_df.iloc[::-1]

            self.calculate_results(results, original_df, expected_df, row_index)

            if results[0] is not None and results[1] is not None:
                return results

        return results

    def is_vertical_reflect(self, df):
        num_columns = len(df.columns)
        results = [None, None]

        for column_index in range(1, num_columns):
            # divide the df into two parts
            left_df = df.iloc[:, :column_index]
            right_df = df.iloc[:, column_index:]

            left_df_size = len(left_df.columns)
            right_df_size = len(right_df.columns)

            # update the column headers of right df to start from 0
            right_df.columns = range(len(right_df.columns))

            original_df = None
            expected_df = None

            if left_df_size <= right_df_size:
                original_df = left_df
                # get the subset from the right side df to match the size of left side df
                expected_df = right_df.iloc[:, :left_df_size]
                expected_df = expected_df.iloc[:, ::-1]
            else:
                original_df = right_df
                expected_df = left_df.iloc[:, right_df_size * -1 :]
                expected_df = expected_df.iloc[:, ::-1]

            self.calculate_results(results, original_df, expected_df, column_index)

            if results[0] is not None and results[1] is not None:
                return results

        return results

    def process(self):
        part_01_res = 0
        part_02_res = 0
        for index, pattern in enumerate(self.patterns):
            print(f"\npattern started: {index}")

            v_results = self.is_vertical_reflect(pattern)
            print(f"is_vertical_reflect: {v_results}")

            if v_results[0] is not None:
                part_01_res += v_results[0]

            if v_results[1] is not None:
                part_02_res += v_results[1]

            if v_results[0] is not None and v_results[1] is not None:
                continue

            h_results = self.is_horizontal_reflect(pattern)
            print(f"is_horizontal_reflect: {h_results}")

            if h_results[0] is not None:
                part_01_res += h_results[0] * 100

            if h_results[1] is not None:
                part_02_res += h_results[1] * 100

        print(f"\nPart 01: {part_01_res}")
        print(f"Part 02: {part_02_res}")

    def read_input_file(self):
        with open(self.input_file, "r", encoding="utf-8") as file:
            current_df = None
            for line in file:
                trimmed_line = line.strip()

                if trimmed_line == "":
                    self.patterns.append(current_df)
                    current_df = None
                    continue

                char_list = list(trimmed_line)

                if current_df is None:
                    current_df = pd.DataFrame(
                        columns=[i for i in range(len(char_list))]
                    )

                current_df.loc[len(current_df)] = char_list

            self.patterns.append(current_df)

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

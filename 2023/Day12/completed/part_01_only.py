import time
import pandas as pd
import re
import numpy as np
import sys
import multiprocessing


class Main:
    def __init__(self):
        self.input_file = "../inputs/original-half.txt"
        self.springs_records_df = None

    def get_sum_of_arrangements(self):
        return self.springs_records_df["arrangements"].sum()

    def generate_binary_inputs(self, n):
        for i in range(2**n):
            binary_digits = [int(bit) for bit in format(i, "0{}b".format(n))]
            yield tuple(binary_digits)

    def process_row(self, row):
        record_items = np.array(list(row["cleaned_record"]))
        record_items_copy = record_items.copy()
        question_mark_indices = np.where(record_items == "?")[0]
        considered_arrangement = set()
        arrangements_count = 0

        for binary_sequence in self.generate_binary_inputs(len(question_mark_indices)):
            # check if min required 1 are present
            if binary_sequence.count(1) != row["req_hash_count"]:
                continue

            binary_sequence_np = np.array(binary_sequence)
            poss_arr = np.where(binary_sequence_np == 1)[0]

            # replace question marks with .
            record_items_copy[record_items == "?"] = "."

            # get qmarks indices to replace with #
            qmarks_indices_to_replace = question_mark_indices[poss_arr]
            record_items_copy[qmarks_indices_to_replace] = "#"
            arrangement = "".join(record_items_copy)

            formatted_arr = self.remove_extra_dots(arrangement)
            arr_str = ""
            # get the groups
            groups_in_arr = formatted_arr.split(".")

            if len(groups_in_arr) == row["pattern_groups_count"]:
                for part in groups_in_arr:
                    arr_str += str(part.count("#")) + ","

                arr_str = arr_str.strip(",")
                # print(grouped_arr)

                if (
                    row["pattern_groups_count"] == len(groups_in_arr)
                    and row["pattern"] == arr_str
                ):
                    # print(f"min groups count found and matched found: {arr_str}")
                    arrangements_count += 1

                considered_arrangement.add(arrangement)

        return arrangements_count

    def process_records_wrapper(self, args):
        row_index, row = args
        arrangements = self.process_row(row)
        return (row_index, arrangements)

    def process_records_para(self):
        with multiprocessing.Pool(processes=8) as pool:
            args_list = [
                (index, row) for index, row in self.springs_records_df.iterrows()
            ]
            processed_data = pool.map(self.process_records_wrapper, args_list)

        for data in processed_data:
            self.springs_records_df.loc[data[0], "arrangements"] = data[1]

    def remove_extra_dots(self, record):
        # remove leading and trailing dots
        record = record.strip(".")
        record = re.sub(r"\.+", ".", record)
        return record

    def read_input_files(self):
        columns = [
            "record",
            "pattern",
            "cleaned_record",
            "pattern_groups",
            "record_groups",
            "pattern_groups_count",
            "req_hash_count",
            "arrangements",
        ]
        self.springs_records_df = pd.DataFrame(columns=columns)
        with open(self.input_file, "r", encoding="utf-8") as file:
            for line in file:
                df_row = []
                row_values = line.strip().split()

                df_row.append(row_values[0])
                df_row.append(row_values[1])

                # clean the record
                cleaned_record = self.remove_extra_dots(row_values[0])
                df_row.append(cleaned_record)

                # get groups from pattern
                groups = [int(part) for part in row_values[1].split(",")]
                df_row.append(groups)

                # get groups from the record
                given_groups = []
                if "." in cleaned_record:
                    given_groups = cleaned_record.split(".")

                df_row.append(given_groups)
                df_row.append(len(groups))

                # calculate min hash count
                df_row.append(sum(groups) - cleaned_record.count("#"))

                df_row.append(None)

                self.springs_records_df.loc[len(self.springs_records_df)] = df_row

    def main(self):
        print("Started")
        self.read_input_files()
        self.process_records_para()

        print()
        print(self.springs_records_df)
        sum_of_arrangements = self.get_sum_of_arrangements()
        print(f"\nPart 01: {sum_of_arrangements}\n")


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 900)
    # sys.setrecursionlimit(15000)
    start_time = time.time()
    main = Main()
    main.main()
    end_time = time.time()
    print("\nExecution time(s): ", end_time - start_time)

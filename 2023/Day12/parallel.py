import time
import pandas as pd
import re
import numpy as np
import sys
import multiprocessing


class Main:
    def __init__(self):
        self.input_file = "inputs/test.txt"
        self.springs_records_df = None
        self.record_indices_for_later = []

    def get_repeating_part_for_qmarks_endings(self, row):
        row_copy = row.copy()

        first_dot_index = row_copy["record"].find(".")
        first_hash_index = row_copy["record"].find("#")

        if first_dot_index > -1 and first_hash_index > -1:
            min_index_of_dot_or_hash = min(first_dot_index, first_hash_index)
        else:
            if first_dot_index > -1:
                min_index_of_dot_or_hash = first_dot_index
            else:
                min_index_of_dot_or_hash = first_hash_index

        # find the max number of ? avaiable in the next record
        # min_index_of_dot_or_has = min(
        #     (row_copy["record"].find(char) for char in ".#"), default=-1
        # )
        # print(f"min_index_of_dot_or_has: {min_index_of_dot_or_has}")
        # qmarks_part = row_copy["record"].split("#")[0]
        # row_copy["record"] = row_copy["record"] + qmarks_part
        if min_index_of_dot_or_hash > -1:
            row_copy["record"] = row_copy["record"] + ("?" * min_index_of_dot_or_hash)
        else:
            # print("-1 received")
            row_copy["record"] = row_copy["record"] + row_copy["record"]

        # clean the record
        cleaned_record = self.remove_extra_dots(row_copy["record"])
        row_copy["cleaned_record"] = cleaned_record

        # get groups from the record
        given_groups = []
        if "." in cleaned_record:
            given_groups = cleaned_record.split(".")
        row_copy["record_groups"] = given_groups

        return row_copy

    def get_repeating_part(self, row, last_char):
        row_copy = row.copy()

        # update the record
        if last_char == ".":
            row_copy["record"] = "?" + row_copy["record"]
        else:
            row_copy["record"] = row_copy["record"] + "?" + row_copy["record"]
            row_copy["pattern"] = row_copy["pattern"] + "," + row_copy["pattern"]

            # get groups from pattern
            groups = [int(part) for part in row_copy["pattern"].split(",")]
            row_copy["pattern_groups"] = groups
            row_copy["pattern_groups_count"] = len(groups)

        # clean the record
        cleaned_record = self.remove_extra_dots(row_copy["record"])
        row_copy["cleaned_record"] = cleaned_record

        # get groups from the record
        given_groups = []
        if "." in cleaned_record:
            given_groups = cleaned_record.split(".")
        row_copy["record_groups"] = given_groups

        return row_copy

    def get_sum_of_arrangements_part_02(self):
        return self.springs_records_df["arrangements_part_02"].sum()

    def get_sum_of_arrangements(self):
        return self.springs_records_df["arrangements"].sum()

    def generate_binary_inputs(self, n):
        for i in range(2**n):
            binary_digits = [int(bit) for bit in format(i, "0{}b".format(n))]
            yield tuple(binary_digits)

    def process_row(self, row, initial_arr_count=0, added_qmarks_amount=None):
        record_items = np.array(list(row["cleaned_record"]))
        record_items_copy = record_items.copy()
        question_mark_indices = np.where(record_items == "?")[0]
        considered_arrangement = set()
        arrangements_count = initial_arr_count

        for binary_sequence in self.generate_binary_inputs(len(question_mark_indices)):
            # check if min required 1 are present
            if binary_sequence.count(1) != row["req_hash_count"]:
                continue

            # check if the repeating part is 0
            if added_qmarks_amount is not None:
                added_tuple = tuple([0] * added_qmarks_amount)
                # check if repeating part is all 0
                if binary_sequence[-added_qmarks_amount:] == added_tuple:
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

    def calc_part_2_for_qmarks_endings(
        self, row_index, row, part_01_res, is_parallel_task
    ):
        repeating_row = self.get_repeating_part_for_qmarks_endings(row)
        newly_added_qmarks_count = len(repeating_row["record"]) - len(row["record"])
        print(
            f"repeating row: {repeating_row['record']} | newly added: {newly_added_qmarks_count}"
        )

        if not is_parallel_task and newly_added_qmarks_count > 8:
            self.record_indices_for_later.append(row_index)
            return

        arrangement_for_repeating_row = self.process_row(
            repeating_row, part_01_res, newly_added_qmarks_count
        )

        return part_01_res * arrangement_for_repeating_row**4

    def process_records(self):
        for index, row in self.springs_records_df.iterrows():
            print(f"\n{index}: {row['record']} -> {row['pattern']}")
            # calculate arrangements for part 01
            arrangements = self.process_row(row)
            self.springs_records_df.loc[index, "arrangements"] = arrangements
            # print(f"arrangements calculated: {arrangements}")

            # get the last char
            last_char = row["record"][-1]
            arrangements_of_unfolded = 0
            if last_char == "#":
                arrangements_of_unfolded = arrangements * arrangements**4
            elif last_char == ".":
                repeating_row = self.get_repeating_part(row, last_char)
                print(f"--original row: {row['record']}")
                print(f"--repeating row: {repeating_row['record']}")
                arrangement_for_repeating_row = self.process_row(repeating_row)
                arrangements_of_unfolded = (
                    arrangements * arrangement_for_repeating_row**4
                )
            elif last_char == "?":
                arrangements_of_unfolded = self.calc_part_2_for_qmarks_endings(
                    index, row, arrangements, False
                )

            self.springs_records_df.loc[
                index, "arrangements_part_02"
            ] = arrangements_of_unfolded

    def remove_extra_dots(self, record):
        # remove leading and trailing dots
        record = record.strip(".")
        record = re.sub(r"\.+", ".", record)
        return record

    def unfold_records(self, row_values):
        # update the record
        updated_row_values = row_values.copy()
        for _ in range(4):
            updated_row_values[0] = updated_row_values[0] + "?" + row_values[0]
            updated_row_values[1] = updated_row_values[1] + "," + row_values[1]

        return updated_row_values

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
            "arrangements_part_02",
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
                df_row.append(None)

                self.springs_records_df.loc[len(self.springs_records_df)] = df_row

    def wrapper_to_calc_part_two_val_for_large_records(self, args):
        record_index, row = args
        current_process = multiprocessing.current_process()
        print(f"\nProcess [{current_process.name}] started: {record_index}")
        result_for_chunk = self.calc_part_2_for_qmarks_endings(
            record_index, row, row["arrangements"], True
        )
        # result_for_chunk = record_index * 100
        # time.sleep(record_index / 50)
        print(
            f"\n---> Process [{current_process.name}] completed: {record_index} result: {result_for_chunk}"
        )
        return (record_index, result_for_chunk)

    def process_cycle_02(self):
        print("\nprocess cycle 02 started")

        # self.record_indices_for_later = [404, 351, 360, 379, 440]

        # print(f"df size: {self.springs_records_df.shape}")

        # indices stored for process later:
        print(
            f"number of records for process later: {len(self.record_indices_for_later)}"
        )
        with multiprocessing.Pool(processes=8) as pool:
            args_list = [
                (row_index, self.springs_records_df.iloc[row_index])
                for row_index in self.record_indices_for_later
            ]
            processed_data = pool.map(
                self.wrapper_to_calc_part_two_val_for_large_records, args_list
            )

        for data in processed_data:
            print(f"\nresult set : {str(data)}")
            self.springs_records_df.loc[data[0], "arrangements_part_02"] = data[1]

    def process_cycle_01(self):
        self.process_records()

    def main(self):
        self.read_input_files()
        self.process_cycle_01()
        self.process_cycle_02()

        print()
        print(self.springs_records_df)
        sum_of_arrangements = self.get_sum_of_arrangements()
        print(f"\nPart 01: {sum_of_arrangements}\n")
        sum_of_arrangements_part_02 = self.get_sum_of_arrangements_part_02()
        print(f"\nPart 02: {sum_of_arrangements_part_02}\n")


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 900)
    sys.setrecursionlimit(15000)
    start_time = time.time()
    main = Main()
    main.main()
    end_time = time.time()
    print("\nExecution time(s): ", end_time - start_time)
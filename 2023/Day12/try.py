import time
import pandas as pd
import math


class Main:
    def __init__(self):
        self.input_file = "inputs/test.txt"
        self.springs_records_df = None

    def handle_equal_groups(self, row, row_index):
        print(f"\n{row['record']}")
        # given groups by removing additional dots
        filtered_given_groups = [item for item in row["given_groups"] if bool(item)]
        expected_groups = row["groups"]
        spaces_springs_map = []
        arrangements = []
        total_arrangements = 1

        # find spaces for each group
        for index, group in enumerate(expected_groups):
            expected_group = "#" * int(group)
            given_group = filtered_given_groups[index]

            springs_to_add = expected_group.count("#") - given_group.count("#")
            available_qmarks = given_group.count("?")

            if springs_to_add > 0:
                spaces_springs_map.append((springs_to_add, available_qmarks))

        # remove (1,1) from the map
        filtered_ss_map = [tup for tup in spaces_springs_map if tup != (1, 1)]

        # if len(filtered_ss_map) > 0:
        #     total_arrangements = 0

        for ss_map in filtered_ss_map:
            spaces_after_grouping = ss_map[1] - (ss_map[0] - 1)
            # total_arrangements += spaces_after_grouping
            arrangements.append(spaces_after_grouping)

        # get the total arrangement
        for arrangement in arrangements:
            total_arrangements *= arrangement

        print(f"map: {spaces_springs_map}\n")
        print(f"filtered map: {filtered_ss_map}\n")

        return total_arrangements

    def get_factorial_sum(self, factorial):
        if factorial == 0:
            return 0
        else:
            return factorial + self.get_factorial_sum(factorial - 1)

    def get_sum_of_arrangements(self):
        return self.springs_records_df["arrangements"].sum()

    def process_records(self):
        for index, row in self.springs_records_df.iterrows():
            springs_total = sum(row["groups"])
            required_groups_total = row["no_of_groups"]
            min_dots = max(required_groups_total - 1, 0)

            given_groups_total = row["no_of_given_groups"]
            qmarks_total = row["record"].count("?")
            given_dots_total = row["record"].count(".")
            given_springs_total = row["record"].count("#")

            # calcs
            remaining_qmarks_total = qmarks_total - min_dots
            springs_to_fill = max(springs_total - given_springs_total, 0)

            if given_groups_total > required_groups_total:
                # print(
                #     "\n\nGiven groups amount is greater than the required groups amounts"
                # )
                # print(
                #     f"record: {row['record']} | total qmarks: {qmarks_total} | min dots: {min_dots}"
                # )
                # print(
                #     f"\nrequired groups: {required_groups_total} \ngiving groups: {given_groups_total}"
                # )
                # print(
                #     f"\nsprings total: {springs_total} \ngiving springs: {given_springs_total} \nsprings to fill: {springs_to_fill}"
                # )
                # print(f"\nremaining qmarks after dots: {remaining_qmarks_total}")

                remaining_qmarks_after_grouping = remaining_qmarks_total - (
                    springs_to_fill - 1
                )
                # print(
                #     f"remaining qmarks after grouping : {remaining_qmarks_after_grouping}\n"
                # )
                arrangements = self.get_factorial_sum(
                    max(remaining_qmarks_after_grouping - 1, 1)
                )
                self.springs_records_df.loc[index, "arrangements"] = arrangements
                # print(f"{self.springs_records_df.loc[index]}")
            elif given_groups_total == required_groups_total:
                # print("\n\n- - --Given groups and required groups amounts are equal")
                # print(f"\nremaining qmarks after dots: {remaining_qmarks_total}")
                arrangements = self.handle_equal_groups(row, index)
                self.springs_records_df.loc[index, "arrangements"] = arrangements
            else:
                remaining_qmarks_after_grouping = remaining_qmarks_total - (
                    springs_to_fill - 1
                )
                arrangements = self.get_factorial_sum(
                    max(remaining_qmarks_after_grouping - 1, 1)
                )
                self.springs_records_df.loc[index, "arrangements"] = arrangements
                # print(f"{self.springs_records_df.loc[index]}")

            # print(f"{self.springs_records_df.loc[index]}")

    def read_input_files(self):
        columns = [
            "record",
            "pattern",
            "groups",
            "no_of_groups",
            "given_groups",
            "no_of_given_groups",
            "arrangements",
        ]
        self.springs_records_df = pd.DataFrame(columns=columns)
        with open(self.input_file, "r", encoding="utf-8") as file:
            for line in file:
                row_values = line.strip().split()

                # get groups from pattern
                groups = [int(part) for part in row_values[1].split(",")]
                row_values.append(groups)
                row_values.append(len(groups))

                # get groups from the record
                given_groups = []
                if "." in row_values[0]:
                    given_groups = row_values[0].split(".")

                row_values.append(given_groups)
                row_values.append(len([s for s in given_groups if s]))

                row_values.append(None)

                self.springs_records_df.loc[len(self.springs_records_df)] = row_values

    def main(self):
        self.read_input_files()
        self.process_records()
        print(self.springs_records_df)
        sum_of_arrangements = self.get_sum_of_arrangements()
        print(f"\nSum: {sum_of_arrangements}")


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 900)
    start_time = time.time()
    main = Main()
    main.main()
    end_time = time.time()
    print("\nExecution time(s): ", end_time - start_time)

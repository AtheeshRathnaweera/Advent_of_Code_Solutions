import time
from functools import cache


class Main:
    def __init__(self):
        self.input_file = "../inputs/original.txt"

    @cache
    def process(self, pattern, groups):
        if (pattern == "" or set(pattern) <= {"?", "."}) and len(groups) == 0:
            return 1

        if pattern == "" or len(groups) == 0:
            return 0

        # get the first char
        first_char = pattern[0]
        # create groups list
        groups_list = list(map(int, groups.split(",")))

        if first_char == ".":
            return self.process(pattern[1:], groups)
        elif first_char == "#":
            group_size = groups_list[0]
            if len(pattern) >= group_size:
                current_record = pattern[:group_size]

                if len(pattern) > group_size and pattern[group_size] not in [".", "?"]:
                    return 0

                # replace ? with #
                updated_record = current_record.replace("?", "#")
                expected_record = "#" * group_size

                if updated_record == expected_record:
                    new_groups = groups_list[1:]
                    return self.process(
                        pattern[group_size + 1 :], ",".join(map(str, new_groups))
                    )
        elif first_char == "?":
            return self.process("#" + pattern[1:], groups) + self.process(
                "." + pattern[1:], groups
            )

        return 0

    def part_01(self, pattern, groups):
        # remove leading and trailing .
        stripped_pattern = pattern.strip(".")
        return self.process(stripped_pattern, groups)

    def part_02(self, pattern, groups):
        # create the pattern for part 02
        new_pattern = "?".join([pattern] * 5)
        new_groups = ",".join([groups] * 5)

        # remove leading and trailing .
        stripped_pattern = new_pattern.strip(".")
        return self.process(stripped_pattern, new_groups)

    def main(self):
        part_01_total = 0
        part_02_total = 0

        with open(self.input_file, "r", encoding="utf-8") as file:
            for line in file:
                # get the pattern and groups
                pattern, groups = line.split()

                part_01_total += self.part_01(pattern, groups)
                part_02_total += self.part_02(pattern, groups)

        print(f"\npart 01: {part_01_total}")
        print(f"part 02: {part_02_total}")


if __name__ == "__main__":
    start_time = time.time()
    main = Main()
    main.main()
    end_time = time.time()
    print("\nExecution time(s): ", end_time - start_time)

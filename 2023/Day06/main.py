import time


class Main:
    def __init__(self):
        self.input_file_name = "inputs/input.txt"
        # list of tuples. (duration (ms), currenct record (mm))
        self.races_info = []

    def find_ways_to_beat_record_second(self):
        result = 0
        for race_info in self.races_info:
            duration = race_info[0]
            record = race_info[1]
            ways_to_win = 0
            # store the times of min and max hold times to break the record. (min, max)
            lowest_and_highest_time_info = [0, 0]
            # store whether the min and max hold times are found. (min, max)
            lowest_and_highest_val_found = [False, False]

            for btn_hold_time in range(duration + 1):
                lowest_speed = btn_hold_time
                traveling_time_of_lowest = duration - btn_hold_time

                highest_speed = duration - btn_hold_time
                traveling_time_of_higest = btn_hold_time

                if record < lowest_speed * traveling_time_of_lowest:
                    lowest_and_highest_time_info[0] = btn_hold_time
                    lowest_and_highest_val_found[0] = True

                if record < highest_speed * traveling_time_of_higest:
                    lowest_and_highest_time_info[1] = duration - btn_hold_time
                    lowest_and_highest_val_found[1] = True

                if lowest_and_highest_val_found[0] and lowest_and_highest_val_found[1]:
                    break

            # calculate ways amount
            ways_to_win = (
                lowest_and_highest_time_info[1] - lowest_and_highest_time_info[0] + 1
            )

            if ways_to_win > 0:
                if result == 0:
                    result = ways_to_win
                else:
                    result *= ways_to_win

        return result

    def find_ways_to_beat_record(self):
        result = 0
        for race_info in self.races_info:
            print(f"\nrace info: {race_info}")
            duration = race_info[0]
            record = race_info[1]
            ways_to_win = 0

            for btn_hold_time in range(duration + 1):
                speed = btn_hold_time
                traveling_time = duration - btn_hold_time
                max_distance = speed * traveling_time

                if record < max_distance:
                    ways_to_win += 1

            print(f"ways found: {ways_to_win}")

            if ways_to_win > 0:
                if result == 0:
                    result = ways_to_win
                else:
                    result *= ways_to_win

        return result

    def read_input_files(self, isPartTwo):
        with open(self.input_file_name, "r", encoding="utf-8") as file:
            data = []
            for line in file:
                main_parts = line.split(":")
                nums = []

                if isPartTwo:
                    nums = main_parts[1].replace(" ", "").split()
                else:
                    nums = main_parts[1].split()

                for index, num in enumerate(nums):
                    if main_parts[0] == "Time":
                        data.append([int(num)])
                    elif main_parts[0] == "Distance":
                        data[index].append(int(num))
            self.races_info = [tuple(race) for race in data]

    def proces_part_02(self):
        self.read_input_files(True)
        print(f"\npart 02 source data: {self.races_info}")
        res = self.find_ways_to_beat_record_second()
        print(f"Part 02: result -> {res}")

    def proces_part_01(self):
        self.read_input_files(False)
        print(f"part 01 source data: {self.races_info}")
        res = self.find_ways_to_beat_record_second()
        print(f"Part 01: result -> {res}")

    def main(self):
        self.proces_part_01()
        self.proces_part_02()


if __name__ == "__main__":
    start_time = time.time()
    main = Main()
    main.main()
    end_time = time.time()
    print("\nExecution time(s): ", end_time - start_time)

# from pprint import pprint
import time

# import pandas as pd
import multiprocessing


class Main:
    def __init__(self):
        self.input_file_path = "inputs/"
        self.input_file_names = [
            {"mapping_name": "seed-to-soil", "file_name": "seed-to-soil-map.txt"},
            {
                "mapping_name": "soil-to-fertilizer",
                "file_name": "soil-to-fertilizer-map.txt",
            },
            {
                "mapping_name": "fertilizer-to-water",
                "file_name": "fertilizer-to-water-map.txt",
            },
            {
                "mapping_name": "water-to-light",
                "file_name": "water-to-light-map.txt",
            },
            {
                "mapping_name": "light-to-temperature",
                "file_name": "light-to-temperature-map.txt",
            },
            {
                "mapping_name": "temperature-to-humidity",
                "file_name": "temperature-to-humidity-map.txt",
            },
            {
                "mapping_name": "humidity-to-location",
                "file_name": "humidity-to-location-map.txt",
            },
        ]
        self.seeds = []
        self.mappings = {
            "seed-to-soil": [],
            "soil-to-fertilizer": [],
            "fertilizer-to-water": [],
            "water-to-light": [],
            "light-to-temperature": [],
            "temperature-to-humidity": [],
            "humidity-to-location": [],
        }
        # self.mappings_source_ranges = {}
        self.mapped_seeds = []
        self.seeds_with_range = []
        # self.seeds_with_range_df = None

    def is_seed_exist_in_range(self, val):
        for seed_range in self.seeds_with_range:
            diff = val - seed_range[0]
            if diff >= 0 and diff < seed_range[1]:
                return True

    def get_part_02_results_parallel(self):
        hum_to_loc_mappings = self.mappings["humidity-to-location"]
        for mapping in hum_to_loc_mappings:
            print(f"\nstarted the search for: {mapping}")
            # calculate the range
            dest_val = mapping[0]
            val_range = mapping[2]

            result = self.find_seed_vals_for_location_range_parallel(
                dest_val, dest_val + val_range
            )
            print(f"completed the search for: {mapping} result: {result}")
            if result is not None and len(result) > 0:
                return min(result)

    def get_part_02_results(self):
        hum_to_loc_mappings = self.mappings["humidity-to-location"]
        for mapping in hum_to_loc_mappings:
            print(f"\nstarted the search for: {mapping}\n")
            # calculate the range
            dest_val = mapping[0]
            val_range = mapping[2]

            result = self.find_seed_vals_for_location_range(
                dest_val, dest_val + val_range
            )
            print(f"\ncompleted the search for: {mapping} result: {result}")
            if result is not None:
                return result

    def worker_function(self, chunk_start, chunk_end, mappings_keys_order, queue):
        current_process = multiprocessing.current_process()
        for val in range(chunk_start, chunk_end):
            prev_source_val = val
            source_vals = []

            for mappings_key in mappings_keys_order:
                found_source_val = prev_source_val

                for mapping in self.mappings[mappings_key]:
                    diff = prev_source_val - mapping[0]
                    if diff >= 0 and diff < mapping[2]:
                        found_source_val = mapping[1] + diff
                        break

                prev_source_val = found_source_val
                source_vals.append(prev_source_val)

            if self.is_seed_exist_in_range(source_vals[-1]):
                print(f"Process {current_process.name} is value found: {val}")
                queue.put(val)
                return

    def find_seed_vals_for_location_range_parallel(self, starting_point, range_length):
        # calculate seed values for lowest location dest range
        mappings_keys_order = [
            "humidity-to-location",
            "temperature-to-humidity",
            "light-to-temperature",
            "water-to-light",
            "fertilizer-to-water",
            "soil-to-fertilizer",
            "seed-to-soil",
        ]
        num_processes = 10
        chunk_size = range_length // num_processes
        processes = []
        queue = multiprocessing.Queue()

        if range_length == -1:
            return

        for i in range(num_processes):
            chunk_start = starting_point + i * chunk_size
            chunk_end = min(chunk_start + chunk_size, starting_point + range_length)
            p = multiprocessing.Process(
                target=self.worker_function,
                args=(chunk_start, chunk_end, mappings_keys_order, queue),
            )
            processes.append(p)
            p.start()

        results = []
        for p in processes:
            p.join()
            try:
                result = queue.get(block=False)  # Attempt to retrieve a result
                results.append(result)
            except Exception as e:
                print(f"Exception occurred: {e}")
                pass  # No result available yet, continue

        return results  # No value found

    def find_seed_vals_for_location_range(self, starting_point, range_length):
        # calculate seed values for lowest location dest range
        mappings_keys_order = [
            "humidity-to-location",
            "temperature-to-humidity",
            "light-to-temperature",
            "water-to-light",
            "fertilizer-to-water",
            "soil-to-fertilizer",
            "seed-to-soil",
        ]
        result = None

        if range_length == -1:
            return

        for val in range(starting_point, starting_point + range_length):
            prev_source_val = val
            source_vals = []

            for mappings_key in mappings_keys_order:
                # print(f"\nmapping key: {mappings_key}")
                found_source_val = prev_source_val

                for mapping in self.mappings[mappings_key]:
                    # print(f"mapping: {mapping}")
                    diff = prev_source_val - mapping[0]
                    if diff >= 0 and diff < mapping[2]:
                        found_source_val = mapping[1] + diff
                        break

                prev_source_val = found_source_val
                source_vals.append(prev_source_val)

            if self.is_seed_exist_in_range(source_vals[-1]):
                return val

        return result

    def prepare_pair_of_seeds(self):
        for index, seed in enumerate(self.seeds):
            if index % 2 == 0:
                self.seeds_with_range.append((seed, self.seeds[index + 1]))

    # check if the mappings of "humidity-to-location" is connected. The source values are considered.
    # If not add the missing mappings.
    def enhance_humidity_to_location_mappings(self):
        # get the humidity-to-location mappings
        mappings = self.mappings["humidity-to-location"]
        # sort the mappings to ascending order base on the source value
        sorted_mappings = sorted(mappings, key=lambda x: x[1], reverse=False)
        new_mappings = []
        # check if the first element is starting from 0
        if sorted_mappings[0][1] != 0:
            new_mappings.append((0, 0, sorted_mappings[0][1]))

        for index, current_item in enumerate(sorted_mappings):
            new_mappings.append(current_item)
            next_item_index = index + 1

            if next_item_index < len(sorted_mappings):
                next_item = sorted_mappings[next_item_index]
                correct_next_item_starting_point = current_item[1] + current_item[2]
                if correct_next_item_starting_point != next_item[1]:
                    new_mappings.append(
                        (
                            correct_next_item_starting_point,
                            correct_next_item_starting_point,
                            next_item[1] - correct_next_item_starting_point,
                        )
                    )
            else:
                new_mappings.append(
                    (
                        current_item[1] + current_item[2],
                        current_item[1] + current_item[2],
                        -1,
                    )
                )

        # sort the mappings based on destination values to ascending order
        sorted_mappings_on_dest = sorted(
            new_mappings, key=lambda x: x[0], reverse=False
        )
        self.mappings["humidity-to-location"] = sorted_mappings_on_dest

    def sort_mappings_by_destination(self):
        for key, value in self.mappings.items():
            sorted_list = sorted(value, key=lambda x: x[0], reverse=False)
            self.mappings[key] = sorted_list

    def read_the_input_files(self):
        # get mappings
        for file_name in self.input_file_names:
            with open(
                self.input_file_path + file_name["file_name"], "r", encoding="utf-8"
            ) as file:
                for line in file:
                    nums = line.split()
                    self.mappings[file_name["mapping_name"]].append(
                        tuple(map(int, nums))
                    )

        # get seeds
        with open(self.input_file_path + "seeds.txt", "r", encoding="utf-8") as file:
            for line in file:
                nums = line.split()
                self.seeds.extend(map(int, nums))

    def get_lowest_location_of_seeds(self):
        self.read_the_input_files()
        self.sort_mappings_by_destination()
        self.enhance_humidity_to_location_mappings()
        self.prepare_pair_of_seeds()

        print(f"seeds: {self.seeds}")
        print(f"seeds with ranges: {self.seeds_with_range}\n")
        for key, value in self.mappings.items():
            print(f"{key} : {value}")

        return self.get_part_02_results_parallel()
        # return self.get_part_02_results()

    def main(self):
        lowest_location_num = self.get_lowest_location_of_seeds()
        print(f"\nPart 02: {lowest_location_num}")


if __name__ == "__main__":
    start_time = time.time()
    main = Main()
    main.main()
    end_time = time.time()
    print("Execution time(s): ", end_time - start_time)


# Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
# Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
# Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
# Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

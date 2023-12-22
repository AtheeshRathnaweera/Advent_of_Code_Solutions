from pprint import pprint
import time
import multiprocessing


class Main:
    def __init__(self):
        self.input_file_path = "test-inputs/"
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

    def find_the_lowest_location_for_a_seed(self, seed_range):
        lowest_location = None
        for index in range(seed_range[1]):
            seed_num = seed_range[0] + index
            mapped_vals = self.find_mapping_for_seed_num(seed_num)
            print(f"mapped values value for: {seed_num} -> {mapped_vals}")
            if lowest_location is None or lowest_location > mapped_vals[7]:
                lowest_location = mapped_vals[7]
            # print(f"{seed_num} -> {lowest_location}")
            # print(f"\ncompleted the range: {seed_range}")
        return (seed_range, lowest_location)

    def find_the_lowest_location_from_ranges(self):
        lowest_location = None
        for seed_range in self.seeds_with_range:
            lowest_location = self.find_the_lowest_location_for_a_seed(seed_range)
        return lowest_location

    def prepare_pair_of_seeds(self):
        for index, seed in enumerate(self.seeds):
            if index % 2 == 0:
                self.seeds_with_range.append((seed, self.seeds[index + 1]))

    def get_the_lowest_location(self):
        lowest_location = None
        for mapped_seed in self.mapped_seeds:
            if lowest_location is None or lowest_location > mapped_seed[7]:
                lowest_location = mapped_seed[7]
        return lowest_location

    def find_mapping_for_seed_num(self, seed_num):
        mapped_vals = [seed_num]
        last_cat_mapped_val = seed_num

        for key, value in self.mappings.items():
            # identify the source range
            found_map_line = None
            diff = 0
            mapped_val = last_cat_mapped_val
            # source_range = self.mappings_source_ranges[key]

            # check if the seed num is in the range
            # if (
            #     last_cat_mapped_val >= source_range[0]
            #     and last_cat_mapped_val <= source_range[1]
            # ):
            #     for map_line in value:
            #         diff = last_cat_mapped_val - map_line[1]
            #         if diff >= 0 and diff <= map_line[2]:
            #             found_map_line = map_line
            #             break

            for map_line in value:
                diff = last_cat_mapped_val - map_line[1]
                if diff >= 0 and diff <= map_line[2]:
                    found_map_line = map_line
                    break

            if found_map_line is not None:
                mapped_val = found_map_line[0] + diff
                last_cat_mapped_val = mapped_val

            mapped_vals.append(mapped_val)

        return mapped_vals

    def process_mappings(self):
        for seed in self.seeds:
            mapped_vals = self.find_mapping_for_seed_num(seed)
            self.mapped_seeds.append(tuple(mapped_vals))

    def order_the_mappings(self):
        # mappings are ordering in descending order
        for key, value in self.mappings.items():
            sorted_list = sorted(value, key=lambda x: x[1], reverse=True)

            # get the starting and ending point
            # starting_point = sorted_list[-1][1]
            # ending_point = sorted_list[0][1] + (sorted_list[0][2] - 1)

            # self.mappings_source_ranges[key] = (starting_point, ending_point)
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

    def get_lowest_from_range_of_seeds(self):
        print("get_lowest_from_range_of_seeds started")
        self.prepare_pair_of_seeds()
        return self.find_the_lowest_location_from_ranges()

    def get_lowest_location_of_seeds(self):
        self.read_the_input_files()
        self.order_the_mappings()
        self.process_mappings()
        return self.get_the_lowest_location()

    def main(self):
        lowest_location_num = self.get_lowest_location_of_seeds()
        # lowest_location_num_from_range = self.get_lowest_from_range_of_seeds()

        for key, value in self.mappings.items():
            print(f"{key}: {value}")

        print("\n")

        for mapped_seed in self.mapped_seeds:
            print(mapped_seed)

        # print("\n")
        # print(self.mappings_source_ranges)
        print("\n")
        print(self.seeds)

        print(f"PART 01: {lowest_location_num}\n")
        # print(f"PART 02: {lowest_location_num_from_range}")


# def wrapper_find_mapping(data_set):
#     # mappings = mainClassIns.mappings
#     # print("wrapper: ", mappings)
#     current_thread = threading.current_thread()
#     print(f"{current_thread} rec: {str(data_set)}")
#     mapped_vals = ["test"]
#     # Call the original function with the seed number and mappings from the instance
#     # mapped_vals = mainClassIns.find_mapping_for_seed_num(seed_num, mappings)
#     return mapped_vals


def wrapper_find_lowest_location_for_ranges(args):
    data_chunk, main_class_inst = args
    current_process = multiprocessing.current_process()
    print(
        f"\nProcess {current_process.name} is processing for the seed range: {data_chunk}"
    )
    result_for_chunk = main_class_inst.find_the_lowest_location_for_a_seed(data_chunk)
    print(
        f"\nProcess {current_process.name} completed: {data_chunk} result: {result_for_chunk}"
    )
    return result_for_chunk


if __name__ == "__main__":
    start_time = time.time()
    NUM_OF_PROCESSES = 10

    main = Main()
    main.main()

    main.prepare_pair_of_seeds()
    print(f"seeds with ranges: {main.seeds_with_range}")
    new_seeds_with_range = main.seeds_with_range
    print(f"new seeds with ranges: {new_seeds_with_range}")

    with multiprocessing.Pool(processes=NUM_OF_PROCESSES) as pool:
        args_list = [(data_chunk, main) for data_chunk in new_seeds_with_range]
        processed_data = pool.map(wrapper_find_lowest_location_for_ranges, args_list)

    result = [item for chunk in processed_data for item in chunk]
    print(result)

    # find the lowest location from results set
    lowest_result = None
    for data in processed_data:
        print(f"\nresult set : {str(data)}")
        if lowest_result is None or lowest_result > data[1]:
            lowest_result = data[1]

    print("lowest location: ", lowest_result)

    end_time = time.time()
    print("Execution time: ", end_time - start_time)


# def main():
#     main_class_inst = Main()
#     dataset = list(range(100))
#     num_processes = 5

#     chunk_size = len(dataset) // num_processes
#     data_chunks = [
#         dataset[i : i + chunk_size] for i in range(0, len(dataset), chunk_size)
#     ]

#     print(data_chunks)

#     with multiprocessing.Pool(processes=num_processes) as pool:
#         args_list = [(data_chunk, main_class_inst) for data_chunk in data_chunks]
#         processed_data = pool.map(process_data, args_list)

#     result = [item for chunk in processed_data for item in chunk]
#     print(result)


# if __name__ == "__main__":
#     main()

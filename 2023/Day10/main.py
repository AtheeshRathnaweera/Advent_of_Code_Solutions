import time
import pandas as pd
import numpy as np
import sys
from shapely.geometry import Point, Polygon


class Main:
    def __init__(self):
        self.input_file = "inputs/original.txt"
        self.map_df = None
        self.starting_point = None
        self.directions_info = {
            "top": {"change": (-1, 0), "valid_pipes": ["|", "F", "7"]},
            "right": {"change": (0, 1), "valid_pipes": ["-", "J", "7"]},
            "bottom": {"change": (1, 0), "valid_pipes": ["|", "J", "L"]},
            "left": {"change": (0, -1), "valid_pipes": ["-", "L", "F"]},
        }
        self.pipe_next_dirs = {
            "|": ["top", "bottom"],
            "-": ["left", "right"],
            "L": ["top", "right"],
            "J": ["top", "left"],
            "7": ["left", "bottom"],
            "F": ["right", "bottom"],
            ".": [],
            "S": ["top", "right", "bottom", "left"],
        }
        # hold the coorinates of complete paths that were found
        self.success_paths = []

    def get_opposite_of_dir(self, direction):
        direction_mapping = {
            "left": "right",
            "right": "left",
            "top": "bottom",
            "bottom": "top",
        }
        # default value is top
        return direction_mapping.get(direction, "top")

    def get_possible_next_dirs(self, pipe, prev_dir):
        possible_dirs = []
        for next_dir in self.pipe_next_dirs[pipe]:
            if next_dir != prev_dir:
                possible_dirs.append(next_dir)
        return possible_dirs

    def is_valid_pipe(self, direction, pipe_char):
        return pipe_char in self.directions_info[direction]["valid_pipes"]

    def find_next_valid_pipe(
        self, current_coords, current_pipe, prev_dir, pipes_in_current_loop
    ):
        # print(
        #     f"\nstarted the pipe: coord-> {current_coords} current pipe-> {current_pipe} prev dir -> {prev_dir}"
        # )
        current_tile_coords = current_coords
        next_dirs_order = self.get_possible_next_dirs(current_pipe, prev_dir)
        valid_pipe_found = False
        reached_to_start = False

        # print(f"\tfound possible dirs: {next_dirs_order}")

        for next_dir in next_dirs_order:
            # print(f"\tchecking the dir {next_dir} for {current_pipe}")
            next_dir_info = self.directions_info[next_dir]
            next_tile_coords = (
                current_tile_coords[0] + next_dir_info["change"][0],
                current_tile_coords[1] + next_dir_info["change"][1],
            )

            if current_coords != "S" and next_tile_coords == self.starting_point:
                # print("\tstarting point found")
                reached_to_start = True
                break

            if next_tile_coords in pipes_in_current_loop:
                # print(f"\talready considered pipe found: {next_tile_coords}")
                continue

            pipe = self.map_df.iat[next_tile_coords[0], next_tile_coords[1]]
            is_valid_pipe = pipe in next_dir_info["valid_pipes"]

            if is_valid_pipe:
                # print(f"\t\tvalid pipe found: {next_dir} -> {pipe}")
                opposite_of_next_dir = self.get_opposite_of_dir(next_dir)
                pipes_in_current_loop.append(next_tile_coords)
                self.find_next_valid_pipe(
                    next_tile_coords, pipe, opposite_of_next_dir, pipes_in_current_loop
                )
                valid_pipe_found = True

        if reached_to_start:
            self.success_paths.append(pipes_in_current_loop)

        if not valid_pipe_found:
            # reset the current loop
            pipes_in_current_loop = []

    def farthest_point(self, tiles_count):
        if tiles_count % 2 == 0:
            result = tiles_count / 2
        else:
            result = (tiles_count + 1) / 2
        return result

    def print_found_paths(self, loop_coords):
        copy_of_df = self.map_df.copy()
        for index, coord in enumerate(loop_coords):
            copy_of_df.iloc[coord[0], coord[1]] = "#"
        print(copy_of_df)

    def mark_outside_tiles_with_hash(
        self, df, main_loop, rows_count, columns_count, symbol
    ):
        identified_outside_tiles = []

        # update the dataframe by marking open tiles as 0
        for column_index in range(0, columns_count):
            # print(f"column index: {column_index}")
            # top to bottom
            for row_index in range(0, rows_count):
                # print(f"\tcell: {row_index, column_index}")
                if (row_index, column_index) not in main_loop:
                    df.iloc[row_index, column_index] = symbol
                    identified_outside_tiles.append((row_index, column_index))
                else:
                    break

            # bottom to top
            for row_index in range(rows_count - 1, -1, -1):
                # print(f"\tcell: {row_index, column_index}")
                if (row_index, column_index) not in main_loop:
                    df.iloc[row_index, column_index] = symbol
                    identified_outside_tiles.append((row_index, column_index))
                else:
                    break

        return identified_outside_tiles

    def get_enclosed_tiles_using_shapely(self, main_loop):
        # get a new dataframe with main loop marked with #
        copy_of_df = self.map_df.copy()
        rows_count, columns_count = copy_of_df.shape
        identified_outside_tiles = []
        enclosed_tiles = []

        for coord in main_loop:
            copy_of_df.iloc[coord[0], coord[1]] = "#"

        identified_outside_tiles = self.mark_outside_tiles_with_hash(
            copy_of_df, main_loop, rows_count, columns_count, "0"
        )

        print(f"\nIdentified outside cells: {len(identified_outside_tiles)}")

        indices_not_on_loop = (
            copy_of_df.stack()
            .index[(copy_of_df.stack() != "#") & (copy_of_df.stack() != "0")]
            .tolist()
        )
        # print(f"\nfiltered cells: {indices_not_on_loop}")
        print(f"Cells not on the loop: {len(indices_not_on_loop)}\n")

        # Define the polygon coordinates
        # Create a Shapely Polygon object
        polygon = Polygon(main_loop)
        for tile in indices_not_on_loop:
            point = Point(tile)
            if polygon.contains(point):
                copy_of_df.iloc[tile[0], tile[1]] = "I"
                enclosed_tiles.append(tile)

        print(f"\nPart 02 Results: {len(enclosed_tiles)}\n")
        print(copy_of_df)

    def get_enclosed_tiles_count(self, main_loop):
        print(f"\nmain loop tiles count: {len(main_loop)}")
        # get a new dataframe with main loop marked with #
        copy_of_df = self.map_df.copy()
        rows_count, columns_count = copy_of_df.shape
        identified_outside_tiles = []
        enclosed_tiles = []

        for index, coord in enumerate(main_loop):
            copy_of_df.iloc[coord[0], coord[1]] = "#"

        identified_outside_tiles = self.mark_outside_tiles_with_hash(
            copy_of_df, main_loop, rows_count, columns_count, "0"
        )

        print(f"\nIdentified outside cells: {len(identified_outside_tiles)}")
        print(copy_of_df)

        indices_not_in_loop = (
            copy_of_df.stack()
            .index[(copy_of_df.stack() != "#") & (copy_of_df.stack() != "0")]
            .tolist()
        )
        print(f"\nfiltered cells: {indices_not_in_loop}")
        print(f"\nfiltered cells count: {len(indices_not_in_loop)}")

        for item in indices_not_in_loop:
            # valid_main_dirs = False

            main_dir_mappings = {
                "top": {
                    "range": (item[0] - 1, -1, True),
                    "changing_index": "row",
                    "hash_found": False,
                },
                "right": {
                    "range": (item[1] + 1, columns_count, False),
                    "changing_index": "column",
                    "hash_found": False,
                },
                "bottom": {
                    "range": (item[0] + 1, rows_count, False),
                    "changing_index": "row",
                    "hash_found": False,
                },
                "left": {
                    "range": (item[1] - 1, -1, True),
                    "changing_index": "column",
                    "hash_found": False,
                },
            }

            for key, dir_mapping in main_dir_mappings.items():
                for row_or_column_index in range(
                    dir_mapping["range"][0],
                    dir_mapping["range"][1],
                    -1 if dir_mapping["range"][2] else 1,
                ):
                    item_row_index, item_column_index = item

                    coords = (
                        row_or_column_index
                        if dir_mapping["changing_index"] == "row"
                        else item_row_index,
                        row_or_column_index
                        if dir_mapping["changing_index"] == "column"
                        else item_column_index,
                    )

                    print(
                        f"processing column for item -> {item}| dir -> {key}| coords -> {coords}"
                    )

                    if coords in identified_outside_tiles:
                        break

                    if coords in main_loop:
                        dir_mapping["hash_found"] = True
                        break

            print(f"dir mappings results: {main_dir_mappings}\n")
            if all(
                main_dir_mappings[direction]["hash_found"]
                for direction in [
                    "top",
                    "right",
                    "bottom",
                    "left",
                ]
            ):
                enclosed_tiles.append(item)
                copy_of_df.iloc[item[0], item[1]] = "I"
            else:
                copy_of_df.iloc[item[0], item[1]] = "0"

        for tile in enclosed_tiles.copy():
            print(f"processing the tile: {tile} for sides")
            sub_dir_mappings = {
                "top-right": {
                    "coords": (tile[0] - 1, tile[1] + 1),
                    "hash_found": False,
                },
                "bottom-right": {
                    "coords": (tile[0] + 1, tile[1] + 1),
                    "hash_found": False,
                },
                "bottom-left": {
                    "coords": (tile[0] + 1, tile[1] - 1),
                    "hash_found": False,
                },
                "top-left": {
                    "coords": (tile[0] - 1, tile[1] - 1),
                    "hash_found": False,
                },
            }

            for key, sub_dir_mapping in sub_dir_mappings.items():
                # print(f"side: {key} -> {sub_dir_mapping}")
                try:
                    pipe = copy_of_df.iloc[
                        sub_dir_mapping["coords"][0], sub_dir_mapping["coords"][1]
                    ]
                    # print(
                    #     f"sub dir : coords: {sub_dir_mapping['coords']} | pipe:{pipe}"
                    # )

                    if sub_dir_mapping["coords"] in main_loop or pipe == "I":
                        sub_dir_mapping["hash_found"] = True
                        # print("\tfound in main loop or I")
                        # break
                except IndexError:
                    print("Exception occurred")

            print(f"sub dir mappings results: {sub_dir_mappings}\n")

            if all(
                sub_dir_mappings[direction]["hash_found"]
                for direction in [
                    "top-right",
                    "bottom-right",
                    "bottom-left",
                    "top-left",
                ]
            ):
                print(f"sides are valid for : {tile}")
            else:
                copy_of_df.iloc[tile[0], tile[1]] = "0"
                enclosed_tiles.remove(tile)

        print(f"\nEnclosed count: {len(enclosed_tiles)}")
        print(copy_of_df)

    def process(self):
        # considered indexes of the current loop
        pipes_in_current_loop = [self.starting_point]
        self.find_next_valid_pipe(self.starting_point, "S", None, pipes_in_current_loop)

        print("\n\nPart 01\n")
        print(f"found success paths: {len(self.success_paths)}")
        print(f"Part 01 Results: {self.farthest_point(len(self.success_paths[0]))}\n")
        # print(self.success_paths[0])

        # copy_of_df = self.map_df.copy()
        # for index, success_path in enumerate(self.success_paths[0]):
        #     # copy_of_df.iloc[success_path[0], success_path[1]] = index
        #     pipe = copy_of_df.iloc[success_path[0], success_path[1]]
        #     new_symbol = pipe
        #     if pipe == "F":
        #         new_symbol = "┌"
        #     elif pipe == "L":
        #         new_symbol = "└"
        #     elif pipe == "7":
        #         new_symbol = "┐"
        #     elif pipe == "J":
        #         new_symbol = "┘"
        #     copy_of_df.iloc[success_path[0], success_path[1]] = new_symbol

        # print(copy_of_df)

        # get the number of enclosed tiles
        print("\n\nPart 02")
        # self.get_enclosed_tiles_count(self.success_paths[0])
        self.get_enclosed_tiles_using_shapely(self.success_paths[0])

    def get_coorinates_of_starting_point(self):
        # Convert the DataFrame to a NumPy array
        np_array = np.array(self.map_df)
        # Find the coordinates (row and column indices) of the target_char
        indices = np.where(np_array == "S")
        # Return the coordinates
        self.starting_point = indices[0][0], indices[1][0]

    def read_input_files(self):
        with open(self.input_file, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
        self.map_df = pd.DataFrame([list(line) for line in lines])

    def main(self):
        self.read_input_files()
        print(self.map_df)
        self.get_coorinates_of_starting_point()
        print(f"\nStarting point: {self.starting_point}")
        print(f"\nDirections: {self.directions_info}")
        print(f"\nNext directions of pipes: {self.pipe_next_dirs}\n")
        self.process()


if __name__ == "__main__":
    start_time = time.time()

    default_recursion_limit = sys.getrecursionlimit()
    print(f"Default recursion limit: {default_recursion_limit}")
    sys.setrecursionlimit(15000)

    main = Main()
    main.main()
    end_time = time.time()
    print("\nExecution time(s): ", end_time - start_time)

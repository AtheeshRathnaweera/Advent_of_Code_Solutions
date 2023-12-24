import time
import re
import math


class Main:
    def __init__(self):
        self.network_input_file = "inputs/original/network.txt"
        self.navigation_input_file = "inputs/original/navigation.txt"
        self.network = {}
        self.navigation = []

    # Function to calculate the LCM of two numbers
    def lcm(self, x, y):
        return x * y // math.gcd(x, y)

    def lcm_of_list(self, values):
        # Initialize lcm_result with the first value in the list
        lcm_result = values[0]

        # Calculate LCM iteratively for each value in the list
        for value in values[1:]:
            lcm_result = self.lcm(lcm_result, value)

        return lcm_result

    def get_starting_nodes_for_part_02(self):
        return [key for key in self.network if key.endswith("A")]

    def is_matched_to_pattern(self, pattern, vals):
        return all(re.match(pattern, val) for val in vals)

    def navigate(self, starting_nodes, expected_pattern):
        current_nodes = starting_nodes.copy()
        steps_count = 0
        match_found = False

        while not match_found:
            for action in self.navigation:
                # print(f"action: {action} current nodes: {current_nodes}")
                steps_count += 1
                # get the next nodes for the current position
                # current_node = self.network[current_node][action]

                for index, current_node in enumerate(current_nodes):
                    current_nodes[index] = self.network[current_node][action]

                # print(f"next nodes: {current_nodes} updated steps: {steps_count}")
                if self.is_matched_to_pattern(expected_pattern, current_nodes):
                    match_found = True
                    break

        return steps_count

    def read_input_files(self):
        with open(self.network_input_file, "r", encoding="utf-8") as file:
            for line in file:
                formatted_line = re.sub(r"[ \n\(\)']", "", line)
                parts = formatted_line.split("=")
                nodes = tuple(parts[1].split(","))
                self.network[parts[0]] = nodes

        with open(self.navigation_input_file, "r", encoding="utf-8") as file:
            self.navigation.extend(
                0 if char == "L" else 1 for line in file for char in line
            )

    def get_part_02_res(self):
        starting_nodes = self.get_starting_nodes_for_part_02()
        print(f"\nPart 02\nstarting nodes: {starting_nodes}")

        # Calculate steps for each starting node
        steps = [
            self.navigate([starting_node], r"^..Z$") for starting_node in starting_nodes
        ]
        print(f"total steps: {steps}")

        # get the LCM of each node
        lcm = self.lcm_of_list(steps)
        print(f"Result: {lcm}")

    def get_part_01_res(self):
        total_steps = self.navigate(["AAA"], r"^ZZZ$")
        print(f"\nPart 01: {total_steps}")

    def main(self):
        self.read_input_files()
        print(self.network)
        print(self.navigation)
        self.get_part_01_res()
        self.get_part_02_res()


if __name__ == "__main__":
    start_time = time.time()
    main = Main()
    main.main()
    end_time = time.time()
    print("\nExecution time(s): ", end_time - start_time)

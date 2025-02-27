import time


class Main:
    def __init__(self):
        self.input_file = "inputs/original.txt"
        self.history_data = []

    def process_history_entry(self, history):
        current_sequence = []
        next_sequence = list(history)
        # store last value of each sequence
        last_vals = []
        first_vals = [next_sequence[0]]
        final_sequence_found = False
        next_val = 0
        left_most_val = 0

        # print("\n")
        while not final_sequence_found:
            current_sequence = next_sequence.copy()
            next_sequence.clear()
            # print(f"starting the sequence: current: {current_sequence}")
            for key, value in enumerate(current_sequence):
                next_key = key + 1

                if next_key == len(current_sequence):
                    break

                diff = current_sequence[key + 1] - value
                next_sequence.append(diff)

            first_vals.append(next_sequence[0])
            last_vals.append(next_sequence[-1])

            if all(value == 0 for value in next_sequence):
                final_sequence_found = True

            # print(f"ended the sequence: next: {next_sequence}")

        # reverse the last vals and first vals list
        last_vals.reverse()
        first_vals.reverse()

        # print(f"first vals: {first_vals} | last vals: {last_vals}")
        # calculate the next value
        next_val = history[-1] + sum(last_vals)
        # calculate left most history val
        first_vals_len = len(first_vals)
        for key, val in enumerate(first_vals):
            next_key = key + 1
            if next_key < first_vals_len:
                left_most_val = first_vals[next_key] - left_most_val

        # print(
        #     f"process_history_entry ended: next val: {next_val} left most val: {left_most_val}"
        # )
        return (next_val, left_most_val)

    def process_history_data(self):
        part_01_res = 0
        part_02_res = 0
        for history_item in self.history_data:
            res = self.process_history_entry(history_item)
            part_01_res += res[0]
            part_02_res += res[1]

        return (part_01_res, part_02_res)

    def calculate(self):
        sum_of_vals = self.process_history_data()
        print(f"\nPart 01: {sum_of_vals[0]}")
        print(f"\nPart 02: {sum_of_vals[1]}")

    def read_input_files(self):
        with open(self.input_file, "r", encoding="utf-8") as file:
            self.history_data = [
                tuple(int(item) for item in line.split()) for line in file
            ]

    def main(self):
        self.read_input_files()
        self.calculate()


if __name__ == "__main__":
    start_time = time.time()
    main = Main()
    main.main()
    end_time = time.time()
    print("\nExecution time(s): ", end_time - start_time)

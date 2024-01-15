import time
import itertools


def generate_binary_inputs(n):
    """
    Generates all possible binary inputs for n variables (A, B, C in this case).

    Args:
        n: The number of variables.

    Yields:
        A string representing a binary input for all n variables.
    """
    for i in range(2**n):
        binary_digits = [int(bit) for bit in format(i, "0{}b".format(n))]
        yield tuple(binary_digits)


def itertools_way():
    binary_sequences = list(itertools.product([0, 1], repeat=5))

    for binary_sequence in binary_sequences:
        print(binary_sequence)


start_time = time.time()
# for binary_input in generate_binary_inputs(5):
#     print(binary_input)
itertools_way()
end_time = time.time()
print("\nExecution time(s): ", end_time - start_time)

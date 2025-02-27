from itertools import chain, combinations
import re
from typing import Iterable
from functools import cache

file_path = "inputs/original.txt"


@cache
def num_valid_solutions(record: str, groups: tuple[int, ...]) -> int:
    # print(f"\n{record} {groups}")

    if not record:
        # if there are no more spots to check;
        # our only chance at success is if there are no `groups` left
        return len(groups) == 0

    if not groups:
        # if there are no more groups the only possibility of success is that there are no `#` remaining
        # here, `?` are treated as `.`, so no recursion is necessary
        return "#" not in record

    char, rest_of_record = record[0], record[1:]

    # print(f"\n{char} {rest_of_record}")

    if char == ".":
        # print("char is .")
        # dots are ignores, so keep recursing
        return num_valid_solutions(rest_of_record, groups)

    if char == "#":
        group = groups[0]
        # print(f"char is #. group: {group}")
        # print(f"remaining: {record[:group]}")
        # we're at the start of a group! make sure there are enough here to fill the first group
        # to be valid, we have to be:
        if (
            # long enough to match
            len(record) >= group
            # made of only things that can be `#` (no `.`)
            and all(c != "." for c in record[:group])
            # either at the end of the record (allowed)
            # or the next character isn't also a `#` (would be too big)
            and (len(record) == group or record[group] != "#")
        ):
            # print(f"came inside if in #. next: {record[group + 1:]} | {groups[1:]}")
            return num_valid_solutions(record[group + 1 :], groups[1:])

        return 0

    if char == "?":
        # print("char is ?")
        return num_valid_solutions(f"#{rest_of_record}", groups) + num_valid_solutions(
            f".{rest_of_record}", groups
        )

    raise ValueError(f"unknown char: {char}")


def solve_line(line: str, with_multiplier=False) -> int:
    record, raw_shape = line.split()
    shape = tuple(map(int, raw_shape.split(",")))

    if with_multiplier:
        record = "?".join([record] * 5)
        shape *= 5

    print(f"{record} -> {shape}\n")

    return num_valid_solutions(record, shape)


def process() -> int:
    results = []
    part_02_total = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            part_01 = solve_line(line)
            print("part 01 completed\n")
            part_02 = solve_line(line, with_multiplier=True)
            part_02_total += part_02
            results.append((part_01, part_02))

    print()
    # for result in results:
    #     print(f"{result}")

    print(f"part 02: {part_02_total}")


process()


# def powerset(l: list[int]):
#     "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
#     return chain.from_iterable(combinations(l, r) for r in range(len(l) + 1))


# def every_solve_combination(record: str) -> Iterable[list[str]]:
#     """
#     yields every combination of lists of groups of broken springs (`#`)
#     """
#     unknown_indexes = [idx for idx, c in enumerate(record) if c == "?"]
#     for indexes_to_replace in powerset(unknown_indexes):
#         chars = list(record)
#         for i in indexes_to_replace:
#             chars[i] = "#"
#         yield re.findall(r"#+", "".join(chars).replace("?", "."))


# def is_valid(groups: list[str], counts: list[int]) -> bool:
#     """
#     do the listed groups of `#` match the required blueprint?
#     """
#     return len(groups) == len(counts) and all(
#         len(l) == g for l, g in zip(groups, counts)
#     )


# def num_valid_combinations(line: str) -> int:
#     record, raw_shape = line.split()
#     shape = list(map(int, raw_shape.split(",")))

#     return sum(is_valid(l, shape) for l in every_solve_combination(record))


# def solve_line(line: str, with_multiplier=False) -> int:
#     record, raw_shape = line.split()
#     shape = tuple(map(int, raw_shape.split(",")))

#     if with_multiplier:
#         record = "?".join([record] * 5)
#         shape *= 5

#     return num_valid_solutions(record, shape)


# def part_1() -> int:
#     with open("inputs/original.txt", "r", encoding="utf-8") as file:
#         part_01 = sum(num_valid_combinations(line) for line in file)
#         print(part_01)


# def part_2(self) -> int:
#     return sum(solve_line(line, with_multiplier=True) for line in self.input)


# part_1()

# prompt: https://adventofcode.com/2023/day/12

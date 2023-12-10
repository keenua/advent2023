from typing import List
from part1 import Node, read_file


def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def get_cycle_length(node: Node, direction: str) -> int:
    hash_set = set()

    current = (node, 0)

    while current not in hash_set:
        hash_set.add(current)
        step = current[1]
        next = current[0].left if direction[step] == "L" else current[0].right
        current = (next, (step + 1) % len(direction))

    return len(hash_set) - current[1]


def traverse(nodes: List[Node], direction: str) -> int:
    cycle_lengths = [
        get_cycle_length(node, direction) if node.name[-1] == "A" else 1
        for node in nodes
    ]
    result = 1
    for cycle_length in cycle_lengths:
        result = lcm(result, cycle_length)

    return result


def main(file: str):
    task = read_file(file)
    root_nodes = [
        task.allNodes.get(node) for node in task.allNodes.keys() if node.endswith("A")
    ]
    result = traverse(root_nodes, task.direction)
    print(result)


if __name__ == "__main__":
    main("day8/network.txt")

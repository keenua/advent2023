from dataclasses import dataclass
from typing import Mapping, Optional


@dataclass
class Node:
    name: str
    left: Optional["Node"]
    right: Optional["Node"]

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Task:
    direction: str
    rootNode: Node
    allNodes: Mapping[str, Node]


def read_file(file: str) -> Task:
    nodes: Mapping[str, Node] = {}

    with open(file) as f:
        direction = f.readline().strip()

        for line in f:
            if line.strip() == "":
                continue

            [parent, children] = line.split(" = ")
            children = [
                child.replace("(", "").replace(")", "").strip()
                for child in children.split(", ")
            ]

            if parent not in nodes:
                nodes[parent] = Node(parent, None, None)

            if children[0] != "None":
                left = nodes.get(children[0]) or Node(children[0], None, None)
                nodes[parent].left = left
                nodes[children[0]] = left

            if children[1] != "None":
                right = nodes.get(children[1]) or Node(children[1], None, None)
                nodes[parent].right = right
                nodes[children[1]] = right

    return Task(direction, nodes.get("AAA"), nodes)


def traverse(node: Node, direction: str) -> int:
    result = 0
    index = 0

    while node is not None and node.name != "ZZZ":
        if direction[index] == "L":
            node = node.left
        else:
            node = node.right

        index += 1
        if index >= len(direction):
            index = 0

        result += 1

        print(result)

    return result


def main(file: str):
    task = read_file(file)
    result = traverse(task.rootNode, task.direction)
    print(result)


if __name__ == "__main__":
    main("day8/network.txt")

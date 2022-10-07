from typing import Any, List


class Node:
    """
    Class Node that puts together nodes from an acyclic tree-like structure.
    """
    REFERENCES = {}

    def __init__(self, name: str) -> None:
        self.name = name
        self.title = ""
        self.num_of_internal_links = 0
        self.num_of_external_links = 0
        self.num_of_references = 0
        self.children = []
        self.total_num_of_children = 0

    @classmethod
    def get_references(cls, name: str) -> int:
        return cls.REFERENCES.get(name, 0)

    def add_child(self, name: str) -> object:
        self.children.append(Node(name))
        return self

    def depth_first_search(self, array, **kwargs: Any) -> List and int:
        """
        Function has implemented Depth First Search algorithm.
        It traverses the tree (specifically navigating the tree from left to right),
        stores all the nodes' names in the input array, and returns it.

        :param array: arrray takes an empty array that will store all children nodes in the future
        :return: array of start_node's nodes
        """
        to_format = kwargs.get("to_format")
        array.append(self.name)
        for node in self.children:
            _, num_of_sub_children = node.depth_first_search(array, to_format=to_format)
            self.total_num_of_children += num_of_sub_children

        # for crawl command - change format of array to either dict or list
        to_format = kwargs.get("to_format")
        if to_format:
            self.update_references(Node.get_references(self.name))
            self.to_format(array, to_format)

        return array, self.total_num_of_children + 1

    def to_format(self, array: List[list or dict], to_format: str) -> None:
        """
        Depends on selected format, append Node to the given array where all nodes are stored
        :param array: takes an array where are all nodes
        :param to_format: takes either json or csv string
        :return:
        """
        if to_format == 'json':
            array.append(
                {
                    "link": self.name,
                    "title": self.title,
                    "number of internal links": self.num_of_internal_links,
                    "number of external links": self.num_of_external_links,
                    "number of references by other pages": self.num_of_references,
                }
            )
        else:
            array.append(
                [
                    self.name,
                    self.title,
                    self.num_of_internal_links,
                    self.num_of_external_links,
                    self.num_of_references,
                ]
            )

    def update_references(self, references: int) -> None:
        self.num_of_references = references

    def __str__(self, depth=0) -> str:
        if len(self.name) > 100:
            name = f"{self.name[:100]}..."
        else:
            name = self.name

        result = "   " * depth + f"{name} ({self.total_num_of_children})\n"
        for child in self.children:
            result += child.__str__(depth + 1)

        return result

import unittest

from web_scrawler_script.node_class import Node


class TestDepthFirstSearchAlogrithm(unittest.TestCase):
    def test_small_nodes(self):
        graph = Node("A")
        graph.add_child("B")
        graph.add_child("C")
        graph.add_child("D")
        graph.children[0].add_child("E").add_child("F")
        graph.children[2].add_child("G").add_child("H")
        graph.children[0].children[1].add_child("I").add_child("J")
        graph.children[2].children[0].add_child("K")
        self.assertEqual(graph.depth_first_search([]), (["A", "B", "E", "F", "I", "J", "C", "D", "G", "K", "H"], 11))

    def test_many_nodes(self):
        graph = Node("A")
        graph.add_child("B")
        graph.add_child("C")
        graph.add_child("D")
        graph.add_child("E")
        graph.add_child("F")

        # Add to Node("B") children: G, H, I
        graph.children[0].add_child("G").add_child("H").add_child("I")

        # Add to Node("C") children: J
        graph.children[1].add_child("J")

        # Add to Node("D") children: K, L
        graph.children[2].add_child("K").add_child("L")

        # Add to Node("F") children: M, N
        graph.children[4].add_child("M").add_child("N")

        # Add to Node("H")
        graph.children[0].children[1].add_child("O").add_child("P").add_child("Q").add_child("R")

        # Add to Node("K")
        graph.children[2].children[0].add_child("S")

        # Add to Node("P")
        graph.children[0].children[1].children[1].add_child("T").add_child("U")

        # Add to Node("R")
        graph.children[0].children[1].children[3].add_child("V")

        # Add to Node("V")
        graph.children[0].children[1].children[3].children[0].add_child("W").add_child("X").add_child("Y")

        # Add to Node("X")
        graph.children[0].children[1].children[3].children[0].children[1].add_child("Z")

        self.assertEqual(graph.depth_first_search([]),
                         (['A', 'B', 'G', 'H', 'O', 'P', 'T', 'U', 'Q', 'R', 'V', 'W', 'X', 'Z', 'Y', 'I', 'C', 'J',
                          'D', 'K', 'S', 'L', 'E', 'F', 'M', 'N'], 26))

    def test_incorrect_result(self):
        graph = Node("A")
        graph.add_child("B")
        graph.add_child("C")
        graph.add_child("D")
        graph.children[0].add_child("E").add_child("F")
        graph.children[2].add_child("G").add_child("H")
        graph.children[0].children[1].add_child("I").add_child("J")
        graph.children[2].children[0].add_child("K")
        self.assertNotEqual(graph.depth_first_search(["A"]),
                            (["A", "B", "E", "F", "I", "J", "C", "D", "G", "K", "H"], 11))


if __name__ == "__main__":
    unittest.main()

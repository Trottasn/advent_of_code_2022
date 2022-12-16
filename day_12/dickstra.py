
from dijkstar import Graph, find_path


END_VAL = (ord('z') - ord('a')) + 2


class Node:
    def __init__(self, x, y, character, forwards):
        self.id = str(x) + ':' + str(y)
        self.x = x
        self.y = y
        self.parent = None
        self.neighbors = []
        self.character = character
        if forwards:
            self.value = gen_value_forwards(character)
        else:
            self.value = gen_value_backwards(character)
        self.f_score = 0
        self.g_score = 0

    def __repr__(self):
        return f'Node value: {self.value} with F Score: {self.f_score}'

    def __lt__(self, other):
        return self.f_score > other.f_score

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


def gen_value_forwards(character):
    if character == 'S':
        return 0
    elif character == 'E':
        return END_VAL
    return (ord(character) - ord('a')) + 1


def gen_value_backwards(character):
    if character == 'S':
        return END_VAL
    elif character == 'E':
        return 0
    return END_VAL - gen_value_forwards(character)


def process_grid(forwards):
    val_grid = []
    start_node = None
    end_node = None
    a_list = []
    with open("input_day_12.txt", mode='r') as input_file:
        y = 0
        for line in input_file:
            line = line.strip()
            x = 0
            curr_line_nodes = []
            val_grid.append(curr_line_nodes)
            for character in line:
                node = Node(x, y, character, forwards)
                curr_line_nodes.append(node)
                if node.value == END_VAL:
                    end_node = node
                elif node.value == 0:
                    start_node = node
                elif node.value == 1:
                    a_list.append(node)
                x += 1
            y += 1

    graph = Graph()
    for y in range(0, len(val_grid)):
        for x in range(0, len(val_grid[y])):
            current_node = val_grid[y][x]
            if y != 0:
                neighbor = val_grid[y - 1][x]
                if neighbor.value <= (current_node.value + 1):
                    graph.add_edge(current_node.id, neighbor.id, 1)
            if y != (len(val_grid) - 1):
                neighbor = val_grid[y + 1][x]
                if neighbor.value <= (current_node.value + 1):
                    graph.add_edge(current_node.id, neighbor.id, 1)
            if x != 0:
                neighbor = val_grid[y][x - 1]
                if neighbor.value <= (current_node.value + 1):
                    graph.add_edge(current_node.id, neighbor.id, 1)
            if x != (len(val_grid[y]) - 1):
                neighbor = val_grid[y][x + 1]
                if neighbor.value <= (current_node.value + 1):
                    graph.add_edge(current_node.id, neighbor.id, 1)

    for node in a_list:
        try:
            print(find_path(graph, node.id, end_node.id))
        except:
            pass


if __name__ == "__main__":
    process_grid(True)

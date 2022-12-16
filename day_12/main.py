from heapq import heapify, heappush, heappop


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
                x += 1
            y += 1
    return val_grid, start_node, end_node


def a_star(grid, start_node, end_node):
    start_node.f_score = start_node.g_score = end_node.f_score = end_node.g_score = 0
    open_list = [start_node]
    closed_list = []
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f_score <= current_node.f_score:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node.id)
        if current_node == end_node:
            return reconstruct_path(current_node)
        x = current_node.x
        y = current_node.y
        current_node.neighbors.clear()
        if y != 0:
            neighbor = grid[y - 1][x]
            if neighbor.value <= (current_node.value + 1):
                current_node.neighbors.append(neighbor)
        if y != (len(grid) - 1):
            neighbor = grid[y + 1][x]
            if neighbor.value <= (current_node.value + 1):
                current_node.neighbors.append(neighbor)
        if x != 0:
            neighbor = grid[y][x - 1]
            if neighbor.value <= (current_node.value + 1):
                current_node.neighbors.append(neighbor)
        if x != (len(grid[y]) - 1):
            neighbor = grid[y][x + 1]
            if neighbor.value <= (current_node.value + 1):
                current_node.neighbors.append(neighbor)
        for neighbor in current_node.neighbors:
            if neighbor.id in closed_list:
                continue
            neighbor.g_score = current_node.g_score + 1
            neighbor.f_score = neighbor.g_score + crow(current_node, neighbor)
            if (neighbor in open_list) and (neighbor.g_score > current_node.g_score):
                continue
            open_list.append(neighbor)
            neighbor.parent = current_node
    return None


def distance(current_node, next_node):
    if current_node.value < next_node.value:
        return 1
    else:
        return (current_node.value - next_node.value) + 2


def crow(current_node, next_node):
    x1 = current_node.x
    y1 = current_node.y
    x2 = next_node.x
    y2 = next_node.y
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current)
        current = current.parent
    return path[::-1]


if __name__ == "__main__":
    full_grid, start, end = process_grid(True)
    final_results = a_star(full_grid, start, end)
    for result in final_results:
        print(result.x, result.y)
    print(len(final_results))

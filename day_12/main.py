END_VAL = (ord('z') - ord('a')) + 2


class Node:
    def __init__(self, x, y, character, forwards):
        self.id = (x, y)
        self.x = x
        self.y = y
        self.parent = None
        self.neighbors = []
        self.character = character
        self.f_score = 0
        self.g_score = 0
        if forwards:
            self.value = gen_value_forwards(character)
        else:
            self.value = gen_value_backwards(character)
        self.weight = 0

    def __lt__(self, other):
        return self.weight > other.weight


def gen_value_forwards(character):
    if character == 'S':
        return 99999999999
    elif character == 'E':
        return ord('z')
    return ord(character)


def gen_value_backwards(character):
    if character == 'S':
        return END_VAL
    elif character == 'E':
        return 999999999999
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
                if character == 'E':
                    end_node = node
                elif character == 'S':
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
            return reconstruct_path(current_node, start_node)
        set_neighbors(grid, current_node)
        check_neighbors(open_list, closed_list, current_node)
    return None


def set_neighbors(grid, current_node):
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


def check_neighbors(open_list, closed_list, current_node):
    for neighbor in current_node.neighbors:
        if neighbor.id in closed_list:
            continue
        neighbor.g_score = current_node.g_score + 1
        neighbor.f_score = neighbor.g_score + crow(current_node, neighbor)
        if (neighbor in open_list) and (neighbor.g_score > current_node.g_score):
            continue
        open_list.append(neighbor)
        neighbor.parent = current_node


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


def reconstruct_path(current_node, starting_node):
    path = []
    current = current_node
    while True:
        path.append(current)
        current = current.parent
        if current == starting_node:
            break
    return path[::-1]


def find_a_nodes(grid):
    a_list = []
    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            node = grid[y][x]
            if node.character == 'a':
                a_list.append(node)
    return a_list


if __name__ == "__main__":
    full_grid, start, end = process_grid(True)
    final_results = a_star(full_grid, start, end)
    print(len(final_results) - 1)

    list_of_as = find_a_nodes(full_grid)
    a_results = []
    for a_node in list_of_as:
        result = a_star(full_grid, a_node, end)
        if result is None:
            continue
        a_results.append(len(a_star(full_grid, a_node, end)) - 1)
    print(min(a_results))

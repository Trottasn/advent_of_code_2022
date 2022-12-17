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
        self.weight = 0
        if forwards:
            self.value = gen_value_forwards(character)
        else:
            self.value = gen_value_backwards(character)

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
        return ord('z')
    elif character == 'E':
        return 99999999999
    return ord('z') - ord(character)


def process_grid(forwards):
    val_grid = []
    start_node = None
    end_nodes = []
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
                if (forwards and node.character == 'E') or ((not forwards) and node.character == 'a'):
                    end_nodes.append(node)
                elif (forwards and node.character == 'S') or ((not forwards) and node.character == 'E'):
                    start_node = node
                x += 1
            y += 1
    return val_grid, start_node, end_nodes


def a_star(grid, start_node, end_nodes):
    start_node.f_score = start_node.g_score = 0
    for an_end in end_nodes:
        an_end.f_score = an_end.g_score = 0
    open_list = [start_node]
    closed_list = []
    while len(open_list) > 0:
        current_node = open_list[0]
        for index, item in enumerate(open_list):
            if item.f_score <= current_node.f_score:
                current_node = item
        open_list.remove(current_node)
        closed_list.append(current_node.id)
        if current_node in end_nodes:
            return reconstruct_path(current_node, start_node)
        set_neighbors(grid, current_node)
        check_neighbors(open_list, closed_list, current_node, start_node, end_nodes)
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


def check_neighbors(open_list, closed_list, current_node, start_node, end_nodes):
    for neighbor in current_node.neighbors:
        if neighbor.id in closed_list:
            continue
        neighbor.g_score = current_node.g_score + distance(current_node, neighbor, start_node, end_nodes)
        neighbor.f_score = neighbor.g_score + heuristic(current_node, neighbor, start_node, end_nodes)
        if (neighbor in open_list) and (neighbor.g_score > current_node.g_score):
            continue
        open_list.append(neighbor)
        neighbor.parent = current_node


def distance(current_node, next_node, start_node, end_nodes):
    return 1


def heuristic(current_node, next_node, start_node, end_nodes):
    return 0


def reconstruct_path(current_node, starting_node):
    path = []
    current = current_node
    while True:
        path.append(current)
        current = current.parent
        if current == starting_node:
            break
    return path[::-1]


if __name__ == "__main__":
    full_grid, start, end = process_grid(True)
    final_results = a_star(full_grid, start, end)
    print(len(final_results) - 1)

    full_grid, start, end = process_grid(False)
    print(len(a_star(full_grid, start, end)) - 1)

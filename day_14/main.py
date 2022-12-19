class DetectionMovement:
    def __init__(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y
        self.next_movement = None


def process():
    movement_chains = []
    with open("input_day_14.txt", mode='r') as input_file:
        for line in input_file:
            stripped_line = line.strip()
            if len(stripped_line) < 1:
                continue
            split_line = stripped_line.split(" -> ")
            curr_movement = None
            to_add = None
            for split_index in range(0, len(split_line)):
                coordinates = split_line[split_index].split(',')
                new_movement = DetectionMovement(int(coordinates[0]), int(coordinates[1]))
                if curr_movement is not None:
                    curr_movement.next_movement = new_movement
                else:
                    to_add = new_movement
                curr_movement = new_movement
            movement_chains.append(to_add)
    return movement_chains


def create_board(det_move_chains, part_one):
    dimensions = find_dimensions(det_move_chains)
    lowest_coordinates = dimensions[0]
    highest_coordinates = dimensions[1]

    factor = 0
    if not part_one:
        factor = 250
    added_height = 0
    if not part_one:
        added_height = 2
    width = highest_coordinates[0] - lowest_coordinates[0] + factor
    lowest_x = lowest_coordinates[0]
    highest_y = highest_coordinates[1]
    board = []
    for _ in range(0, highest_y + 1 + added_height):
        row = []
        board.append(row)
        for _ in range(0, width + 1 +(factor * 2)):
            row.append('.')

    for det_move_chain in det_move_chains:
        curr_move = det_move_chain
        next_in_chain = det_move_chain.next_movement
        while next_in_chain is not None:
            x1 = (curr_move.start_x - lowest_x) + factor
            x2 = (next_in_chain.start_x - lowest_x) + factor
            y1 = curr_move.start_y
            y2 = next_in_chain.start_y
            for rock_y in range(min(y1, y2), max(y1, y2) + 1):
                for rock_x in range(min(x1, x2), max(x1, x2) + 1):
                    board[rock_y][rock_x] = '#'
            curr_move = next_in_chain
            next_in_chain = curr_move.next_movement

    if not part_one:
        for x in range(0, len(board[-1])):
            board[-1][x] = '#'

    start_x = x = (500 - lowest_x) + factor
    start_y = y = 0
    while True:
        if board[y][x] != '.':
            x = 500 - lowest_x + factor
            y = 0
        in_board = (y < (len(board) - 1))
        if not part_one:
            in_board = (y < (len(board) - 1)) and (0 < x < (len(board[y]) - 1))
        if (not in_board) and part_one:
            break
        if in_board and (board[y + 1][x] == '.'):
            y += 1
        elif in_board and (board[y + 1][x - 1] == '.'):
            x -= 1
            y += 1
        elif in_board and (board[y + 1][x + 1] == '.'):
            x += 1
            y += 1
        else:
            board[y][x] = 's'
        if (x == start_x) and (y == start_y):
            break
    total = 0
    for row in board:
        for character in row:
            if character == 's':
                total += 1
            print(character, end='')
        print('\n', end='')
    print(total)
    return board


def find_dimensions(det_move_chains):
    lowest_y = 999999
    highest_y = 0
    lowest_x = 999999
    highest_x = 0
    for det_move_chain in det_move_chains:
        next_in_chain = det_move_chain
        while next_in_chain is not None:
            if next_in_chain.start_x > highest_x:
                highest_x = next_in_chain.start_x

            if next_in_chain.start_x < lowest_x:
                lowest_x = next_in_chain.start_x

            if next_in_chain.start_y > highest_y:
                highest_y = next_in_chain.start_y

            if next_in_chain.start_y < lowest_y:
                lowest_y = next_in_chain.start_y
            next_in_chain = next_in_chain.next_movement
    return [(lowest_x, lowest_y), (highest_x, highest_y)]


if __name__ == "__main__":
    detection_movement_chains = process()
    print("### PART ONE ###")
    create_board(detection_movement_chains, True)
    print("### PART TWO###")
    create_board(detection_movement_chains, False)

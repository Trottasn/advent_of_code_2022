def process():
    movements = []
    with open("input_day_9.txt", mode='r') as input_file:
        for line in input_file:
            split = line.strip().split()
            vector = split[0]
            magnitude = split[1]
            movements.append((vector, int(magnitude)))
    return movements


def perform_movements_for_rope_size(movements, rope_size):
    rope = []
    for _ in range(0, rope_size):
        rope.append([[0, 0]])

    vector_map = {'U': [0, 1],
                  'D': [0, -1],
                  'L': [-1, 0],
                  'R': [1, 0]}

    for vector, magnitude in movements:
        for _ in range(magnitude):
            last_head_position = rope[0][-1]
            move = vector_map.get(vector)
            head_next = [last_head_position[0] + move[0], last_head_position[1] + move[1]]
            rope[0].append(head_next)
            process_movement(rope, 1)

    unique_positions = set([])
    for position in rope[-1]:
        unique_positions.add((position[0], position[1]))
    print(len(unique_positions))


def process_movement(rope, knot_index):
    if knot_index == len(rope):
        return

    prev_knot = rope[knot_index - 1]
    curr_knot = rope[knot_index]
    latest_prev_knot_position = prev_knot[-1]
    latest_curr_knot_position = curr_knot[-1]
    latest_curr_x = latest_curr_knot_position[0]
    latest_curr_y = latest_curr_knot_position[1]
    x_diff = latest_prev_knot_position[0] - latest_curr_x
    y_diff = latest_prev_knot_position[1] - latest_curr_y

    xs_equal = (latest_prev_knot_position[0] == latest_curr_knot_position[0])
    ys_equal = (latest_prev_knot_position[1] == latest_curr_knot_position[1])
    within_one = (abs(x_diff) > 1) or (abs(y_diff) > 1)
    if not xs_equal and not ys_equal and within_one:
        execute_move_within_one_diagonal(curr_knot, latest_curr_x, latest_curr_y, x_diff, y_diff)
    elif within_one:
        execute_move_within_one(curr_knot, latest_curr_x, latest_curr_y, x_diff, y_diff)

    process_movement(rope, knot_index + 1)


def execute_move_within_one_diagonal(curr_knot, latest_curr_x, latest_curr_y, x_diff, y_diff):
    if x_diff > 0 and y_diff > 0:
        curr_knot.append([latest_curr_x + 1, latest_curr_y + 1])
    elif x_diff > 0 > y_diff:
        curr_knot.append([latest_curr_x + 1, latest_curr_y - 1])
    elif x_diff < 0 < y_diff:
        curr_knot.append([latest_curr_x - 1, latest_curr_y + 1])
    elif x_diff < 0 and y_diff < 0:
        curr_knot.append([latest_curr_x - 1, latest_curr_y - 1])


def execute_move_within_one(curr_knot, latest_curr_x, latest_curr_y, x_diff, y_diff):
    if x_diff > 0:
        curr_knot.append([latest_curr_x + 1, latest_curr_y])
    elif x_diff < 0:
        curr_knot.append([latest_curr_x - 1, latest_curr_y])
    elif y_diff > 0:
        curr_knot.append([latest_curr_x, latest_curr_y + 1])
    elif y_diff < 0:
        curr_knot.append([latest_curr_x, latest_curr_y - 1])


if __name__ == '__main__':
    final_movements = process()
    print("### PART ONE ###")
    perform_movements_for_rope_size(final_movements, 2)

    print("### PART TWO ###")
    perform_movements_for_rope_size(final_movements, 10)

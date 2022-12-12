def process():
    with open("input_day_9.txt", mode='r') as input_file:
        movements = []
        for line in input_file:
            split = line.strip().split()
            vector = split[0]
            magnitude = split[1]
            movements.append((vector, int(magnitude)))

        vector_map = {'U': [0, 1],
                      'D': [0, -1],
                      'L': [-1, 0],
                      'R': [1, 0]}

        rope = []
        for _ in range(0, 10):
            rope.append([[0, 0]])

        for vector, magnitude in movements:
            for _ in range(magnitude):
                rope[0].append(get_summation(get_last(rope[0]), vector_map.get(vector)))
                process_movement(rope, 1)

        unique_positions = set([])
        for position in rope[-1]:
            unique_positions.add((position[0], position[1]))
        print(len(unique_positions))


def get_last(rope):
    return rope[-1]


def process_movement(rope, knot_index):
    if knot_index == len(rope):
        return

    prev_knot = rope[knot_index - 1]
    curr_knot = rope[knot_index]
    latest_prev_knot_position = get_last(prev_knot)
    latest_curr_knot_position = get_last(curr_knot)
    x_diff, y_diff = get_difference(latest_prev_knot_position, latest_curr_knot_position)

    xs_equal = get_last(prev_knot)[0] == get_last(curr_knot)[0]
    ys_equal = get_last(prev_knot)[1] == get_last(curr_knot)[1]
    within_one = (abs(x_diff) > 1) or (abs(y_diff) > 1)
    if not xs_equal and not ys_equal and within_one:
        if x_diff > 0 and y_diff > 0:
            curr_knot.append(get_summation(get_last(curr_knot), [1, 1]))
        elif x_diff > 0 and y_diff < 0:
            curr_knot.append(get_summation(get_last(curr_knot), [1, -1]))
        elif x_diff < 0 and y_diff > 0:
            curr_knot.append(get_summation(get_last(curr_knot), [-1, 1]))
        elif x_diff < 0 and y_diff < 0:
            curr_knot.append(get_summation(get_last(curr_knot), [-1, -1]))
    elif within_one:
        if x_diff > 0:
            curr_knot.append(get_summation(get_last(curr_knot), [1, 0]))
        elif x_diff < 0:
            curr_knot.append(get_summation(get_last(curr_knot), [-1, 0]))
        elif y_diff > 0:
            curr_knot.append(get_summation(get_last(curr_knot), [0, 1]))
        elif y_diff < 0:
            curr_knot.append(get_summation(get_last(curr_knot), [0, -1]))

    process_movement(rope, knot_index + 1)


def get_difference(second_last, last):
    return [second_last[0] - last[0], second_last[1] - last[1]]


def get_summation(second_last, last):
    return [second_last[0] + last[0], second_last[1] + last[1]]


if __name__ == '__main__':
    process()

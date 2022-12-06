def create_layout():
    with open('input_day_5.txt') as input_file:
        box_lines = []
        box_mode = True
        directions = []
        column_box_map = {}
        for line in input_file:
            if box_mode and is_box_line(line):
                box_lines.append(line)
            elif box_mode:
                box_mode = False
                process_end_of_box_mode(box_lines, column_box_map, line)
            else:
                line = line.strip()
                if len(line) < 1:
                    continue
                process_direction_line(directions, line)
        execute_directions(column_box_map, directions)


def execute_directions(column_box_map, directions):
    for key in column_box_map:
        column_string = ""
        for box in column_box_map[key]:
            column_string += box
        print(column_string)
    for direction in directions:
        num_iters = int(direction[0])
        src_index = int(direction[1])
        dst_index = int(direction[2])
        original_dst_len = len(column_box_map[dst_index])
        for _ in range(0, num_iters):
            character = column_box_map[src_index].pop()
            column_box_map[dst_index].insert(original_dst_len, character)
    answer = ""
    for key in column_box_map:
        answer += str(column_box_map[key][-1])
    print(answer)


def process_direction_line(directions, line):
    line = line.replace("move ", "")
    line = line.replace("from ", "")
    line = line.replace("to ", "")
    direction = line.split(' ')
    directions.append(direction)


def process_end_of_box_mode(box_lines, column_box_map, line):
    line = line.strip()
    columns = line.split(' ')
    for x in range(1, int(columns[-1]) + 1):
        column_box_map[x] = []
    for box_line in box_lines:
        process_box_line(column_box_map, box_line)


def process_box_line(column_box_map, line):
    position = 1
    space_count = 0
    ignore_next_space = False
    for character in line:
        if character == '[':
            space_count = 0
        elif character == ']':
            space_count = 0
            ignore_next_space = True
        elif character == ' ':
            if ignore_next_space:
                ignore_next_space = False
                continue
            space_count += 1
            if space_count == 3:
                position += 1
                ignore_next_space = True
                space_count = 0
        elif character != '\n':
            column_box_map[position].insert(0, character)
            position += 1


def is_box_line(line):
    line = line.strip()
    return line.startswith("[")


if __name__ == "__main__":
    create_layout()

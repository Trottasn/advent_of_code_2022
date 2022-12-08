def find_unique_char_substrings(frame_size):
    with open('input_day_6.txt') as input_file:
        for line in input_file:
            find_unique_char_substring(frame_size, line)


def find_unique_char_substring(frame_size, line):
    current_frame = []
    for i in range(0, len(line)):
        character = line[i]
        if len(current_frame) < frame_size:
            current_frame.append(character)
        if len(current_frame) == frame_size:
            result = process_frame(i, current_frame)
            if result is not None:
                return result


def process_frame(current_index, current_frame):
    match_found = False
    for x in range(0, len(current_frame)):
        frame_char = current_frame[x]
        rest_of_frame = current_frame[:x] + current_frame[(x + 1):]
        if frame_char in rest_of_frame:
            match_found = True
            break
    if match_found:
        current_frame.remove(current_frame[0])
        return None
    answer = current_index + 1
    print(answer)
    return answer


if __name__ == "__main__":
    find_unique_char_substrings(4)
    find_unique_char_substrings(14)

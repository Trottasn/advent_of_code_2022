def eval_pairs():
    pairs = []
    with open("input_day_13.txt", mode='r') as input_file:
        curr_pair = [None, None]
        for line in input_file:
            stripped_line = line.strip()
            if len(stripped_line) < 1:
                continue
            if curr_pair[0] is None:
                curr_pair[0] = eval(stripped_line)
            elif curr_pair[1] is None:
                curr_pair[1] = eval(stripped_line)
                pairs.append(curr_pair)
                curr_pair = [None, None]
    return pairs


def compare(top_level_left, top_level_right):
    largest_len = max(len(top_level_left), len(top_level_right))
    for i in range(largest_len):
        if i >= len(top_level_left):
            return 1
        if i >= len(top_level_right):
            return 0
        left = top_level_left[i]
        right = top_level_right[i]
        ordered = inner_compare(left, right)
        if ordered != -1:
            return ordered
    return -1


def inner_compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        elif left > right:
            return 0
    elif isinstance(left, list) and isinstance(right, list):
        return compare(left, right)
    elif isinstance(left, list) and isinstance(right, int):
        right = [right]
        return compare(left, right)
    elif isinstance(left, int) and isinstance(right, list):
        left = [left]
        return compare(left, right)
    return -1


if __name__ == "__main__":
    print("### PART ONE ###")
    all_pairs = eval_pairs()
    result = 0
    pair_index = 1
    merged_pairs = []
    for pair in all_pairs:
        top_left = pair[0]
        top_right = pair[1]
        merged_pairs.append(top_left)
        merged_pairs.append(top_right)
        if compare(pair[0], pair[1]):
            result += pair_index
        pair_index += 1
    print(result)

    print("### PART TWO ###")
    two_divider_count = 1
    six_divider_count = 2
    for pair in merged_pairs:
        if compare(pair, [[2]]) == 1:
            two_divider_count += 1
    for pair in merged_pairs:
        if compare(pair, [[6]]) == 1:
            six_divider_count += 1
    print(two_divider_count * six_divider_count)

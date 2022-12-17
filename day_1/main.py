def find_max_elf_calories():
    """
    Produces (from the input_day_1.txt contents) a list of the top 3 elf calorie collections.

    :return:
    """
    with open('input_day_1.txt') as input_file:
        max_bunching = []
        current_batch = []
        for line in input_file:
            line = line.strip()
            if not line:
                curr_calories = sum(iter(current_batch))
                max_bunching = process_batch(max_bunching, curr_calories)
                current_batch.clear()
            try:
                current_batch.append(int(line))
            except (ValueError, TypeError):
                continue
    return max_bunching


def process_batch(max_bunching, curr_calories):
    """
    Takes the current top x list of elf calories and makes a new list that also considers the current calorie count.

    :param max_bunching:
    :param curr_calories:
    :return:
    """
    if len(max_bunching) < 3:
        max_bunching.append(curr_calories)
        return max_bunching
    temp_bunching = max_bunching + [curr_calories]
    min_calories = min(temp_bunching)
    temp_bunching.remove(min_calories)
    return temp_bunching


# Execution of Day 1 of Advent of Code
if __name__ == '__main__':
    max_bunching = find_max_elf_calories()
    print("### PART ONE ###")
    print("Max For Any Given Elf: {}".format(max(max_bunching)))
    print("### PART TWO ###")
    print("Total For Top Three Elves: {}".format(sum(max_bunching)))

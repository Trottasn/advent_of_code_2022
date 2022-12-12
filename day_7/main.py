TAB_STRING = "  "


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name):
        self.name = name
        self.parent_dir = None
        self.sub_dirs = []
        self.files = []
        self.total_size = -1


def process_file():
    top_level_dir = None
    curr_dir = None
    with open('input_day_7.txt') as input_file:
        for line in input_file:
            line = line.strip()
            if line.startswith('$'):
                [top_level_dir, curr_dir] = process_command_line(top_level_dir, curr_dir, line)
            else:
                process_list_line(curr_dir, line)
    return top_level_dir


def process_list_line(curr_dir, line):
    if not line.startswith("dir"):
        size_name_split = line.split(' ')
        size = int(size_name_split[0])
        name = size_name_split[1]
        curr_dir.files.append(File(name, size))


def process_command_line(top_level_dir, curr_dir, line):
    line = line[1:]
    line = line.strip()
    if line.startswith("cd"):
        curr_dir = process_cd_line(curr_dir, line)
        if curr_dir.parent_dir is None:
            top_level_dir = curr_dir
    return [top_level_dir, curr_dir]


def process_cd_line(curr_dir, line):
    dir_name = line[2:]
    dir_name = dir_name.strip()
    if (dir_name == "..") and (curr_dir.parent_dir is not None):
        curr_dir = curr_dir.parent_dir
    else:
        parent_dir = curr_dir
        curr_dir = Directory(dir_name)
        if parent_dir is not None:
            curr_dir.parent_dir = parent_dir
            parent_dir.sub_dirs.append(curr_dir)
    return curr_dir


def display_filesystem(all_dirs, curr_dir, indent_count):
    tab_string = "  "
    # Create space-prefix string
    space_string = create_space_string(indent_count)
    # Print current directory name
    print("{}{}".format(space_string, curr_dir.name))
    # Add a tab
    space_string += tab_string
    # Print the current directory and total the size
    curr_dir_size = find_current_dir_size(space_string, curr_dir)
    # Recurse and gather results
    accumulator, curr_dir.total_size = find_accumulator_and_total_size(indent_count, all_dirs, curr_dir_size, curr_dir)
    all_dirs.append(curr_dir)
    # If the curr dir is under the designated total size, add it to both the accumulation AND the overall total
    if curr_dir.total_size <= 100000:
        return (accumulator + curr_dir.total_size), curr_dir.total_size
    else:
        return accumulator, curr_dir.total_size


def find_accumulator_and_total_size(indent_count, all_dirs, total_size, curr_dir):
    accumulator = 0
    for sub_dir in curr_dir.sub_dirs:
        sub_accumulator, sub_dir_size = display_filesystem(all_dirs, sub_dir, indent_count + 1)
        total_size += sub_dir_size
        accumulator += sub_accumulator
    return [accumulator, total_size]


def find_current_dir_size(space_prefix, curr_dir):
    curr_dir_size = 0
    for file in curr_dir.files:
        curr_dir_size += file.size
        print("{}file: {} size: {}".format(space_prefix, file.name, file.size))
    print("{}dir size: {}".format(space_prefix, curr_dir_size))
    return curr_dir_size


def create_space_string(indent_count):
    space_string = ""
    for _ in range(0, indent_count):
        space_string += TAB_STRING
    return space_string


if __name__ == "__main__":
    master_dir = process_file()
    dir_list = []
    sub_summation, total = display_filesystem(dir_list, master_dir, 1)
    print("total size: {}".format(total))
    print("total size of dirs UNDER 100000: {}".format(sub_summation))
    MAX_SYSTEM_SIZE = 70000000
    space_needed = abs(MAX_SYSTEM_SIZE - total - 30000000)
    print("space needed: {}".format(space_needed))
    smallest_dir_size_above_needed = MAX_SYSTEM_SIZE
    for potential_smallest_dir in dir_list:
        if (potential_smallest_dir.total_size >= space_needed) and \
                (potential_smallest_dir.total_size < smallest_dir_size_above_needed):
            smallest_dir_size_above_needed = potential_smallest_dir.total_size
    print(smallest_dir_size_above_needed)

def process_file():
    top_level_dir = None
    curr_dir = None
    with open('input_day_7.txt') as input_file:
        for line in input_file:
            line = line.strip()
            if line_is_command(line):
                line = line[1:]
                line = line.strip()
                if is_cd_command(line):
                    curr_dir = process_cd_line(curr_dir, line)
                    if curr_dir.parent_dir is None:
                        top_level_dir = curr_dir
            else:
                if not is_dir_list_entry(line):
                    size_name_split = line.split(' ')
                    size = int(size_name_split[0])
                    name = size_name_split[1]
                    curr_dir.files.append(File(name, size))
    return top_level_dir


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


def is_dir_list_entry(line):
    return line.startswith("dir")


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


def is_cd_command(line):
    return line.startswith("cd")


def line_is_command(line):
    return line.startswith('$')


def display_filesystem(all_dirs, curr_dir, indent_count):
    tab_string = "  "
    space_string = ""
    for _ in range(0, indent_count):
        space_string += tab_string
    print("{}{}".format(space_string, curr_dir.name))
    space_string += tab_string
    curr_dir_size = 0
    for file in curr_dir.files:
        curr_dir_size += file.size
        print("{}file: {} size: {}".format(space_string, file.name, file.size))
    print("{}dir size: {}".format(space_string, curr_dir_size))
    total_size = curr_dir_size
    accumulator = 0
    for sub_dir in curr_dir.sub_dirs:
        sub_accumulator, sub_dir_size = display_filesystem(all_dirs, sub_dir, indent_count + 1)
        total_size += sub_dir_size
        accumulator += sub_accumulator
    curr_dir.total_size = total_size
    all_dirs.append(curr_dir)
    if total_size <= 100000:
        return (accumulator + total_size), total_size
    else:
        return accumulator, total_size


if __name__ == "__main__":
    master_dir = process_file()
    dir_list = []
    sumz, total = display_filesystem(dir_list, master_dir, 1)
    print("total size: {}".format(total))
    print("total size of dirs UNDER 100000: {}".format(sumz))
    MAX_SYSTEM_SIZE = 70000000
    space_needed = abs(MAX_SYSTEM_SIZE - total - 30000000)
    print("space needed: {}".format(space_needed))
    smallest_dir_size_above_needed = MAX_SYSTEM_SIZE
    for potential_smallest_dir in dir_list:
        if (potential_smallest_dir.total_size >= space_needed) and \
                (potential_smallest_dir.total_size < smallest_dir_size_above_needed):
            smallest_dir_size_above_needed = potential_smallest_dir.total_size
    print(smallest_dir_size_above_needed)

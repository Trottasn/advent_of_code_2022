class Bag:
    def __init__(self, contents):
        self.contents = contents
        compartment_size = len(contents) // 2
        compartment1 = Compartment(contents[0:compartment_size])
        compartment2 = Compartment(contents[compartment_size:])
        self.compartment1 = compartment1
        self.compartment2 = compartment2

    def get_compartment_match(self):
        return self.compartment1.find_match(self.compartment2)

    def find_bag_match(self, bag2, bag3):
        all_common = []
        for character in bag3.contents:
            if (character in bag2.contents) and (character not in all_common):
                all_common.append(character)
        for character in bag3.contents:
            if (character not in self.contents) and (character in all_common):
                all_common.remove(character)
        return all_common


class Compartment:
    def __init__(self, contents):
        self.contents = contents
        self.all_common = []

    def find_match(self, other_compartment):
        for character in other_compartment.contents:
            if character in self.contents:
                return character


def calculate_priority(match):
    a_ord = ord('a')
    a_ord_upper = ord('A')
    if match.isupper():
        return (ord(match) - a_ord_upper) + 27
    else:
        return (ord(match) - a_ord) + 1


def calculate_bag_sum():
    total = 0
    group_total = 0
    grouping = []
    with open('input_day_3.txt') as input_file:
        for line in input_file:
            line = line.strip()
            bag = Bag(line)
            grouping.append(bag)
            compartment_match = bag.compartment1.find_match(bag.compartment2)
            priority = calculate_priority(compartment_match)
            total += priority
            if len(grouping) == 3:
                grouping.sort(key=lambda curr_bag: len(curr_bag.contents))
                group_match = grouping[0].find_bag_match(grouping[1], grouping[2])
                priority = calculate_priority(group_match[0])
                group_total += priority
                grouping.clear()
    return total, group_total


# Execution of Day 3 of Advent of Code
if __name__ == '__main__':
    final_total, final_group_total = calculate_bag_sum()
    print("### PART ONE ###")
    print(final_total)
    print("### PART TWO ###")
    print(final_group_total)

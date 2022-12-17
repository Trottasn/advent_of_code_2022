from math import gcd
from functools import reduce


MONKEY = "Monkey"
STARTING_ITEMS = "Starting items:"
OPERATION = "Operation:"
TEST_DIVISIBLE_BY = "Test: divisible by "
IF_TRUE_THROW = "If true: throw to monkey "
IF_FALSE_THROW = "If false: throw to monkey "


class Monkey:
    def __init__(self, number):
        self.number = number
        self.items = []
        self.divisor_number = 1
        self.true_monkey_number = 0
        self.false_monkey_number = 0
        self.items_inspected = 0
        self.add = False
        self.mult = False
        self.adjustor = None


def handle_throw(curr_monkey, old, monkey_map, least_common, worry_division):
    if curr_monkey.mult:
        old.handle_mult(curr_monkey.adjustor)
    elif curr_monkey.add:
        old.handle_add(curr_monkey.adjustor)
    if worry_division:
        old.value = old.value // 3
    curr_monkey.items_inspected += 1
    old.value = old.value % least_common
    if old.handle_divisor_check(curr_monkey.divisor_number):
        print("Monkey {} throws item {} to Monkey {}".format(curr_monkey.number, old.value,
                                                             curr_monkey.true_monkey_number))
        monkey_map[curr_monkey.true_monkey_number].items.append(old)
    else:
        print("Monkey {} throws item {} to Monkey {}".format(curr_monkey.number, old.value,
                                                             curr_monkey.false_monkey_number))
        monkey_map[curr_monkey.false_monkey_number].items.append(old)


class Item:
    def __init__(self, initial_value):
        self.value = initial_value

    def handle_mult(self, adjustor):
        if adjustor is None:
            self.value = self.value * self.value
        else:
            self.value = self.value * adjustor

    def handle_add(self, adjustor):
        self.value += adjustor

    def handle_divisor_check(self, divisor):
        return self.value % divisor == 0


def process():
    processed_monkey_map = {}
    current_monkey = None
    with open("input_day_11.txt", mode='r') as input_file:
        for line in input_file:
            stripped_line = line.strip()
            if stripped_line.startswith(MONKEY):
                current_monkey = handle_monkey_line(stripped_line, processed_monkey_map)
            elif stripped_line.startswith(STARTING_ITEMS):
                process_starting_items(stripped_line, current_monkey)
            elif stripped_line.startswith(OPERATION):
                process_operation(stripped_line, current_monkey)
            elif stripped_line.startswith(TEST_DIVISIBLE_BY):
                divisor_number = stripped_line.replace(TEST_DIVISIBLE_BY, '')
                current_monkey.divisor_number = int(divisor_number)
            elif stripped_line.startswith(IF_TRUE_THROW):
                true_monkey_number = stripped_line.replace(IF_TRUE_THROW, '')
                current_monkey.true_monkey_number = int(true_monkey_number)
            elif stripped_line.startswith(IF_FALSE_THROW):
                false_monkey_number = stripped_line.replace(IF_FALSE_THROW, '')
                current_monkey.false_monkey_number = int(false_monkey_number)
    return processed_monkey_map


def handle_monkey_line(modified_line, processed_monkey_map):
    monkey_split = modified_line.replace(':', '').split(" ")
    number = monkey_split[1]
    current_monkey = Monkey(int(number))
    processed_monkey_map[int(number)] = current_monkey
    return current_monkey


def process_starting_items(modified_line, current_monkey):
    modified_line = modified_line.replace(": ", ", ")
    item_numbers = modified_line.split(", ")
    actual_items = []
    for item_number in item_numbers[1:]:
        actual_items.append(Item(int(item_number)))
    current_monkey.items = actual_items


def process_operation(modified_line, current_monkey):
    modified_line = modified_line.replace(OPERATION, '').replace("new = ", '').strip()
    equation_split = modified_line.split(' ')
    operation = equation_split[1]
    if operation == '+':
        current_monkey.add = True
    else:
        current_monkey.mult = True
    if equation_split[2] != "old":
        current_monkey.adjustor = int(equation_split[2])


def perform_rounds(l_c_m, monkey_map, num_rounds, worry_division):
    for _ in range(0, num_rounds):
        for key in monkey_map:
            curr_monkey = monkey_map[key]
            if len(curr_monkey.items) > 0:
                for curr_item in curr_monkey.items:
                    handle_throw(curr_monkey, curr_item, monkey_map, l_c_m, worry_division)
                curr_monkey.items.clear()
    inspected_list = []
    for key in monkey_map:
        inspected_list.append(monkey_map[key].items_inspected)
    most = max(inspected_list)
    inspected_list.remove(most)
    second_most = max(inspected_list)
    print("Most: {}\nSecond Most: {}".format(most, second_most))
    print(most * second_most)


def lcm(all_divisors):
    return reduce(lambda x, y: (x * y) // gcd(x, y), all_divisors)


if __name__ == "__main__":
    final_monkey_map = process()
    divisors = []
    for mon_key in final_monkey_map:
        divisors.append(final_monkey_map[mon_key].divisor_number)
    least_common_multiple = lcm(divisors)

    perform_rounds(least_common_multiple, final_monkey_map, 10000, False)

import math

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

    def handle_throw(self, old, monkey_map, least_common):
        if self.mult:
            old.handle_mult(self.adjustor)
        elif self.add:
            old.handle_add(self.adjustor)
        self.items_inspected += 1
        old.value = old.value % least_common
        if old.handle_divisor_check(self.divisor_number):
            print("Monkey {} throws item {} to Monkey {}".format(key, old.value, curr_monkey.true_monkey_number))
            monkey_map[curr_monkey.true_monkey_number].items.append(old)
        else:
            print("Monkey {} throws item {} to Monkey {}".format(key, old.value, curr_monkey.false_monkey_number))
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
    monkey_map = {}
    current_monkey_number = 0
    with open("input_day_11.txt", mode='r') as input_file:
        for line in input_file:
            stripped_line = line.strip()
            if stripped_line.startswith("Monkey"):
                monkey_split = stripped_line.replace(':', '').split(" ")
                number = monkey_split[1]
                monkey_map[int(number)] = Monkey(int(number))
                current_monkey_number = int(number)
            elif stripped_line.startswith("Starting items:"):
                modified_line = stripped_line.replace(": ", ", ")
                item_numbers = modified_line.split(", ")
                actual_items = []
                for item_number in item_numbers[1:]:
                    actual_items.append(Item(int(item_number)))
                monkey_map[current_monkey_number].items = actual_items
            elif stripped_line.startswith("Operation:"):
                curr_monk = monkey_map[current_monkey_number]
                modified_line = stripped_line.replace("Operation:", '').replace("new = ", '').strip()
                equation_split = modified_line.split(' ')
                operation = equation_split[1]
                if operation == '+':
                    curr_monk.add = True
                else:
                    curr_monk.mult = True
                if equation_split[2] != "old":
                    curr_monk.adjustor = int(equation_split[2])
            elif stripped_line.startswith("Test: divisible by "):
                divisor_number = stripped_line.replace("Test: divisible by ", '')
                monkey_map[current_monkey_number].divisor_number = int(divisor_number)
            elif stripped_line.startswith("If true: throw to monkey "):
                true_monkey_number = stripped_line.replace("If true: throw to monkey ", '')
                monkey_map[current_monkey_number].true_monkey_number = int(true_monkey_number)
            elif stripped_line.startswith("If false: throw to monkey "):
                false_monkey_number = stripped_line.replace("If false: throw to monkey ", '')
                monkey_map[current_monkey_number].false_monkey_number = int(false_monkey_number)
    return monkey_map


if __name__ == "__main__":
    monkey_map = process()
    all_divisors = []
    for key in monkey_map:
        all_divisors.append(monkey_map[key].divisor_number)
    least_common_multiple = math.lcm(*all_divisors)
    for _ in range(0, 10000):
        for key in monkey_map:
            curr_monkey = monkey_map[key]
            if len(curr_monkey.items) > 0:
                for curr_item in curr_monkey.items:
                    curr_monkey.handle_throw(curr_item, monkey_map, least_common_multiple)
                curr_monkey.items.clear()
    inspected_list = []
    for key in monkey_map:
        inspected_list.append(monkey_map[key].items_inspected)
    most = max(inspected_list)
    inspected_list.remove(most)
    second_most = max(inspected_list)
    print("Most: {}\nSecond Most: {}".format(most, second_most))
    print(most * second_most)

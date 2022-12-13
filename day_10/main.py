class System:
    def __init__(self):
        self.current_cycle = -1
        self.commands_in_progress = []
        self.completed_commands = []
        self.signal_strength = 1
        self.x_register = 1

    def calculate_signal_strength(self):
        self.signal_strength = self.current_cycle * self.x_register
        return self.signal_strength


class Command:
    name = None

    def execute(self, system):
        pass


class NoopCommand(Command):
    def __init__(self):
        self.name = "noop"
        self.cycles_left = 1


class AddXCommand(Command):
    def __init__(self, amount):
        self.name = "addx"
        self.cycles_left = 2
        self.amount = amount

    def execute(self, system):
        system.x_register += self.amount


def process():
    system = System()
    start_cycle = 20
    cycle_cadence = 40
    signal_strength_total = 0
    display_array = []
    for x in range(0, 6):
        display_array.append([])
        for _ in range(0, 40):
            display_array[x].append('.')
    with open("input_day_10.txt", mode='r') as input_file:
        for line in input_file:
            command = line.strip()
            if command == "noop":
                noop_command = NoopCommand()
                system.commands_in_progress.append(noop_command)
                most_recent_command = noop_command
            else:
                command_sections = command.split(' ')
                name = command_sections[0]
                if name == "addx":
                    amount = command_sections[1]
                    add_x_command = AddXCommand(int(amount))
                    system.commands_in_progress.append(add_x_command)
                    most_recent_command = add_x_command

            if most_recent_command is not None:
                for _ in range(0, most_recent_command.cycles_left):
                    system.current_cycle += 1
                    result = check_signal_strength(start_cycle, cycle_cadence, signal_strength_total, system)
                    if result is not None:
                        signal_strength_total = result
                    row = system.current_cycle // 40
                    possible_columns = [system.x_register - 1, system.x_register, system.x_register + 1]
                    cycle_column = system.current_cycle - (row * 40)
                    if cycle_column in possible_columns:
                        display_array[row][cycle_column] = '#'
                most_recent_command.execute(system)

    return signal_strength_total, display_array


# If the system had been in parallel - I would have liked part II to have been about that...
# system.current_cycle += 1

# recently_completed_commands = []
# for in_progress in system.commands_in_progress:
#     in_progress.cycles_left -= 1
#     if in_progress.cycles_left == 0:
#         in_progress.execute(system)
#         system.completed_commands = in_progress
#         recently_completed_commands.append(in_progress)

# for recently_completed_command in recently_completed_commands:
#     system.commands_in_progress.remove(recently_completed_command)


def check_signal_strength(start_cycle, cycle_cadence, signal_strength_total, system):
    cadence_mod = ((system.current_cycle - start_cycle) % cycle_cadence)
    if (start_cycle == system.current_cycle) or (cadence_mod == 0):
        current_signal_strength = system.calculate_signal_strength()
        print(current_signal_strength)
        return signal_strength_total + current_signal_strength
    return None


if __name__ == "__main__":
    strength, display = process()
    print(strength)
    for x in range(0, len(display)):
        current_row_string = ""
        for y in range(0, len(display[x])):
            current_row_string += display[x][y]
        print(current_row_string)

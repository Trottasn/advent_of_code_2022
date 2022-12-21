class HasPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def manhattan_distance(self, other_pos):
        return abs(self.x - other_pos.x) + abs(self.y - other_pos.y)

    def __str__(self):
        return f"Location: {self.x}, {self.y}"

    def __repr__(self):
        return f"Location: {self.x}, {self.y}"

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)


class Beacon(HasPosition):
    def __init__(self, x, y):
        super().__init__(x, y)


class Sensor(HasPosition):
    def __init__(self, x, y):
        super().__init__(x, y)


def process():
    sensors = []
    beacons = []
    with open("input_day_15.txt", mode='r') as input_file:
        for line in input_file:
            stripped_line = line.strip()
            sensor, beacon = process_sensor_and_beacon(stripped_line)
            sensors.append(sensor)
            beacons.append(beacon)
    return sensors, beacons


def process_sensor_and_beacon(line):
    first_equal = line.find('=')
    line = line[(first_equal + 1):]
    first_comma = line.find(',')
    sensor_x = int(line[:first_comma])
    line = line[(first_comma + 4):]
    first_colon = line.find(':')
    sensor_y = int(line[:first_colon])
    line = line[(first_colon + 1):].replace(" closest beacon is at x=", '')
    second_comma = line.find(',')
    beacon_x = int(line[:second_comma])
    beacon_y = int(line[(second_comma + 4):].strip())
    return Sensor(sensor_x, sensor_y), Beacon(beacon_x, beacon_y)


def get_all_dead_node_xs_at_y(sensor, beacon, y):
    manhattan = sensor.manhattan_distance(beacon)
    if ((sensor.y + manhattan) < y) or ((sensor.y - manhattan) > y):
        number_of_dead_nodes_at_y = 0
        return None, None
    else:
        number_of_dead_nodes_at_y = ((2 * manhattan) + 1) - (abs(sensor.y - y) * 2)
    return (sensor.x - (number_of_dead_nodes_at_y // 2)), (sensor.x + (number_of_dead_nodes_at_y // 2))


def squash_ranges(sub_ranges):
    composite_ranges = []
    for x_range in sub_ranges:
        start_x = x_range[0]
        end_x = x_range[1]
        if len(composite_ranges) == 0:
            composite_ranges.append(x_range)
        else:
            compare_against_composites(start_x, end_x, composite_ranges)
    return composite_ranges


def compare_against_composites(range_start, range_end, composite_ranges):
    new_composite_range = None
    remove_range = False
    composite_range = None
    for composite_range in composite_ranges:
        composite_range_start = composite_range[0]
        composite_range_end = composite_range[1]
        if (range_start > composite_range_start) or (range_end < composite_range_end):
            new_composite_range = (min(range_start, composite_range_start), max(range_end, composite_range_end))
            remove_range = True
            break
    if remove_range:
        composite_ranges.remove(composite_range)
        composite_ranges.append(new_composite_range)


def find_hidden_beacon(sensors, beacons):
    for i in range(0, len(sensors)):
        sensor = sensors[i]
        beacon = beacons[i]
        manhattan = sensor.manhattan_distance(beacon)
        for x_distance in range(manhattan + 2):
            y_distance = (manhattan + 1) - x_distance
            for vector_x, vector_y in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                x = sensor.x + (x_distance * vector_x)
                y = sensor.y + (y_distance * vector_y)
                if not(0 <= x <= 4000000 and 0 <= y <= 4000000):
                    continue
                if not within_other_sensors_ranges(x, y, sensors, beacons):
                    return x, y
    return None, None


def within_other_sensors_ranges(x, y, sensors, beacons):
    for j in range(0, len(sensors)):
        some_sensor = sensors[j]
        some_closest_beacon = beacons[j]
        theoretical_beacon = Beacon(x, y)
        if some_sensor.manhattan_distance(theoretical_beacon) <= some_sensor.manhattan_distance(some_closest_beacon):
            return True
    return False


if __name__ == "__main__":
    all_sensors, all_beacons = process()
    print("### PART ONE ###")
    ranges = []
    for index in range(0, len(all_sensors)):
        curr_sensor = all_sensors[index]
        curr_beacon = all_beacons[index]
        min_x, max_x = get_all_dead_node_xs_at_y(curr_sensor, curr_beacon, 2000000)
        if (min_x is not None) and (max_x is not None):
            ranges.append((min_x, max_x))
    ranges = squash_ranges(ranges)
    total = 0
    for final_range in ranges:
        total += (final_range[1] - final_range[0])
    print(total)

    print("### PART TWO ###")
    final_x, final_y = find_hidden_beacon(all_sensors, all_beacons)
    print((final_x * 4000000) + final_y)

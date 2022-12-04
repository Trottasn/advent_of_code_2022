class Assignment:
    def __init__(self, assignment_str):
        start, end = assignment_str.split('-')
        self.start = int(start)
        self.end = int(end)

    def contains(self, other_ass):
        beginning_contained = other_ass.start >= self.start
        end_contained = other_ass.end <= self.end
        return beginning_contained and end_contained

    def overlaps(self, other_ass):
        other_ass_start_contained = self.start <= other_ass.start <= self.end
        other_ass_end_contained = self.start <= other_ass.end <= self.end
        return other_ass_start_contained or other_ass_end_contained


def count_overlap():
    contain_total = 0
    overlap_total = 0
    with open('input_day_4.txt') as input_file:
        for line in input_file:
            line = line.strip()
            assignment_str1, assignment_str2 = line.split(',')
            ass1 = Assignment(assignment_str1)
            ass2 = Assignment(assignment_str2)
            if ass1.contains(ass2) or ass2.contains(ass1):
                contain_total += 1
            if ass1.overlaps(ass2) or ass2.overlaps(ass1):
                overlap_total += 1
    return contain_total, overlap_total


# Execution of Day 4 of Advent of Code
if __name__ == '__main__':
    # Execute
    print(count_overlap())

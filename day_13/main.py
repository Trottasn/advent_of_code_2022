class Pair:
    def __init__(self):
        self.one = None
        self.two = None


def eval_pairs():
    pairs = []
    with open("input_day_13.txt", mode='r') as input_file:
        pair = Pair()
        for line in input_file:
            stripped_line = line.strip()
            if len(stripped_line) < 1:
                continue
            if pair.one is None:
                pair.one = eval(stripped_line)
            if pair.two is None:
                pair.two = eval(stripped_line)
                pairs.append(pair)
                pair = Pair()


if __name__ == "__main__":
    eval_pairs()

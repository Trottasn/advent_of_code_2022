class Weapon:
    def is_rock(self):
        return isinstance(self, Rock)

    def is_paper(self):
        return isinstance(self, Paper)

    def is_scissors(self):
        return isinstance(self, Scissors)

    def get_winning_opponent(self):
        raise Exception("subtype-less weapon cannot determine winning opponent")

    def get_losing_opponent(self):
        raise Exception("subtype-less weapon cannot determine losing opponent")

    def get_equal_opponent(self):
        raise Exception("subtype-less weapon cannot determine equal opponent")

    def intrinsic_score(self):
        raise Exception("not a valid weapon, no intrinsic score")

    def win_score(self, enemy_weapon):
        if isinstance(enemy_weapon, self.get_winning_opponent()):
            return 0
        if isinstance(enemy_weapon, self.get_equal_opponent()):
            return 3
        if isinstance(enemy_weapon, self.get_losing_opponent()):
            return 6
        raise Exception("could not match opponent type with win/lose/tie conditions")


class Rock(Weapon):
    def get_winning_opponent(self):
        return Paper

    def get_losing_opponent(self):
        return Scissors

    def get_equal_opponent(self):
        return Rock

    def intrinsic_score(self):
        return 1


class Paper(Weapon):
    def get_winning_opponent(self):
        return Scissors

    def get_losing_opponent(self):
        return Rock

    def get_equal_opponent(self):
        return Paper

    def intrinsic_score(self):
        return 2


class Scissors(Weapon):
    def get_winning_opponent(self):
        return Rock

    def get_losing_opponent(self):
        return Paper

    def get_equal_opponent(self):
        return Scissors

    def intrinsic_score(self):
        return 3


def calculate_total_points(second_rules):
    with open('input_day_2.txt') as input_file:
        total_score = 0
        for line in input_file:
            processed_line = line.strip()
            weapons = processed_line.split()
            if len(weapons) < 1:
                raise Exception("too little weapons for this round")
            enemy_weapon = generate_based_on_code(weapons[0])
            if second_rules:
                weapon = generate_based_on_win_condition(weapons[1], enemy_weapon)
            else:
                weapon = generate_based_on_code(weapons[1])
            total_score += calculate_round_points(weapon, enemy_weapon)
    return total_score


def generate_based_on_code(code):
    if code in ["A", "X"]:
        return Rock()
    if code in ["B", "Y"]:
        return Paper()
    if code in ["C", "Z"]:
        return Scissors()


def generate_based_on_win_condition(code, enemy_weapon):
    if code == "X":
        return enemy_weapon.get_losing_opponent()()
    if code == "Y":
        return enemy_weapon.get_equal_opponent()()
    if code == "Z":
        return enemy_weapon.get_winning_opponent()()


def calculate_round_points(weapon, enemy_weapon):
    return weapon.win_score(enemy_weapon) + weapon.intrinsic_score()


# Execution of Day 2 of Advent of Code
if __name__ == '__main__':
    '''
    Your total score is the sum of your scores for each round.
    The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) 
    plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).
    '''
    # Execute
    print(calculate_total_points(False))
    print(calculate_total_points(True))

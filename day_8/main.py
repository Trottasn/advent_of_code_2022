class Tree:
    def __init__(self, line_number, column_number, size):
        self.line_number = line_number
        self.column_number = column_number
        self.size = size
        self.left_trees = None
        self.right_trees = None
        self.top_trees = None
        self.bottom_trees = None


def make_grid():
    with open('input_day_8.txt') as input_file:
        grid = []
        all_trees = []
        line_number = 0
        for line in input_file:
            line = line.strip()
            grid.append([])
            column_number = 0
            for character in line:
                tree = Tree(line_number, column_number, int(character))
                grid[line_number].append(tree)
                all_trees.append(tree)
                column_number += 1
            line_number += 1
    return [all_trees, grid]


def connect_grid_components(all_trees, grid):
    for tree in all_trees:
        top_tree = (tree.line_number == 0)
        bottom_tree = (tree.line_number == (len(grid) - 1))
        left_tree = (tree.column_number == 0)
        right_tree = (tree.column_number == (len(grid[tree.line_number]) - 1))
        if not left_tree:
            tree.left = grid[tree.line_number][tree.column_number - 1]
            if not top_tree:
                tree.top_left = grid[tree.line_number - 1][tree.column_number - 1]
            if not bottom_tree:
                tree.bottom_left = grid[tree.line_number + 1][tree.column_number - 1]
            tree.left_trees = get_all_trees_left_of_column(grid, tree.line_number, tree.column_number)
        if not right_tree:
            tree.right = grid[tree.line_number][tree.column_number + 1]
            if not top_tree:
                tree.top_right = grid[tree.line_number - 1][tree.column_number + 1]
            if not bottom_tree:
                tree.bottom_right = grid[tree.line_number + 1][tree.column_number + 1]
            tree.right_trees = get_all_trees_right_of_column(grid, tree.line_number, tree.column_number)
        if not top_tree:
            tree.top = grid[tree.line_number - 1][tree.column_number]
            tree.top_trees = get_all_trees_above_row(grid, tree.line_number, tree.column_number)
        if not bottom_tree:
            tree.bottom = grid[tree.line_number - 1][tree.column_number]
            tree.bottom_trees = get_all_trees_below_row(grid, tree.line_number, tree.column_number)


def get_all_trees_left_of_column_full(grid, column_number):
    all_left_trees = []
    for x in range(0, len(grid)):
        for y in range(0, column_number):
            all_left_trees.append(grid[x][y])
    return all_left_trees


def get_all_trees_left_of_column(grid, line_number, column_number):
    all_left_trees = []
    for y in range(column_number - 1, -1, -1):
        all_left_trees.append(grid[line_number][y])
    return all_left_trees


def get_all_trees_right_of_column_full(grid, column_number):
    all_right_trees = []
    for x in range(0, len(grid)):
        for y in range(column_number + 1, len(grid[x])):
            all_right_trees.append(grid[x][y])
    return all_right_trees


def get_all_trees_right_of_column(grid, line_number, column_number):
    all_right_trees = []
    for y in range(column_number + 1, len(grid[line_number])):
        all_right_trees.append(grid[line_number][y])
    return all_right_trees


def get_all_trees_above_row_full(grid, line_number):
    all_top_trees = []
    for x in range(0, line_number):
        for y in range(0, len(grid[x])):
            all_top_trees.append(grid[x][y])
    return all_top_trees


def get_all_trees_above_row(grid, line_number, column_number):
    all_top_trees = []
    for x in range(line_number - 1, -1, -1):
        all_top_trees.append(grid[x][column_number])
    return all_top_trees


def get_all_trees_below_row_full(grid, line_number):
    all_bottom_trees = []
    for x in range(line_number + 1, len(grid)):
        for y in range(0, len(grid[x])):
            all_bottom_trees.append(grid[x][y])
    return all_bottom_trees


def get_all_trees_below_row(grid, line_number, column_number):
    all_bottom_trees = []
    for x in range(line_number + 1, len(grid)):
        all_bottom_trees.append(grid[x][column_number])
    return all_bottom_trees


def get_total_visible(all_trees):
    visible_trees = 0
    max_view_score = 0
    for tree in all_trees:
        counted = False
        view_score = 1
        visible, score_left = check_visibility(tree, tree.left_trees)
        if visible:
            counted = True
            visible_trees += 1
        view_score = view_score * score_left
        visible, score_right = check_visibility(tree, tree.right_trees)
        if visible and not counted:
            counted = True
            visible_trees += 1
        view_score = view_score * score_right
        visible, score_top = check_visibility(tree, tree.top_trees)
        if visible and not counted:
            counted = True
            visible_trees += 1
        view_score = view_score * score_top
        visible, score_bottom = check_visibility(tree, tree.bottom_trees)
        if visible and not counted:
            visible_trees += 1
        view_score = view_score * score_bottom
        if view_score > max_view_score:
            max_view_score = view_score
    return visible_trees, max_view_score


def check_visibility(tree, tree_list):
    if tree_list is None:
        return True, 0
    score = 0
    visible = True
    for sub_tree in tree_list:
        score += 1
        if sub_tree.size >= tree.size:
            visible = False
            break
    return visible, score


# Execute Day 8 Solution
if __name__ == "__main__":
    final_trees, final_grid = make_grid()
    connect_grid_components(final_trees, final_grid)
    total_visible_trees, best_view_score = get_total_visible(final_trees)
    print(total_visible_trees)
    print(best_view_score)

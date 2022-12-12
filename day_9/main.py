class RopePiece:
    def __init__(self, number):
        self.number = number
        self.x = 0
        self.y = 0
        self.positions = [(0, 0)]
        self.next = None
        self.is_head = False


def process():
    with open('input_day_9.txt') as input_file:
        first_rope = None
        last_rope = None
        for x in range(0, 10):
            new_rope = RopePiece(x)
            if last_rope is not None:
                last_rope.next = new_rope
            else:
                first_rope = new_rope
                first_rope.is_head = True
            last_rope = new_rope
        for line in input_file:
            action_array = line.strip().split(" ")
            vector = action_array[0]
            magnitude = action_array[1]
            process_action(first_rope, vector, int(magnitude))
    return first_rope, last_rope


def process_action(first_piece, vector, magnitude):
    for _ in range(0, magnitude):
        if vector == 'R':
            first_piece.x = piece.x + 1
        elif vector == 'L':
            process_left(first_piece)
        elif vector == 'U':
            process_up(first_piece)
        else:
            process_down(first_piece)


def process_right(piece):
    if piece.next is None:
        return
    next_piece = piece.next
    if piece.is_head:
        piece.x = piece.x + 1
        piece.positions.append((piece.x, piece.y))
    if not is_touching(piece, next_piece):
        next_piece.x = piece.x - 1
        next_piece.y = piece.y

    # TODO: compare previous and current positions to find actual direction of child to use in recursion / chain
    process_right(next_piece)
    next_piece.positions.append((next_piece.x, next_piece.y))


def process_left(piece):
    if piece.next is None:
        return
    next_piece = piece.next
    if piece.is_head:
        piece.x = piece.x - 1
    piece.positions.append((piece.x, piece.y))
    if not is_touching(piece, next_piece):
        next_piece.x = piece.x + 1
        next_piece.y = piece.y
    process_left(next_piece)
    next_piece.positions.append((next_piece.x, next_piece.y))


def process_up(piece):
    if piece.next is None:
        return
    next_piece = piece.next
    if piece.is_head:
        piece.y = piece.y + 1
    piece.positions.append((piece.x, piece.y))
    if not is_touching(piece, next_piece):
        next_piece.x = piece.x
        next_piece.y = piece.y - 1
    process_up(next_piece)
    next_piece.positions.append((next_piece.x, next_piece.y))


def process_down(piece):
    if piece.next is None:
        return
    next_piece = piece.next
    if piece.is_head:
        piece.y = piece.y - 1
    piece.positions.append((piece.x, piece.y))
    if not is_touching(piece, next_piece):
        next_piece.x = piece.x
        next_piece.y = piece.y + 1
    process_down(next_piece)
    next_piece.positions.append((next_piece.x, next_piece.y))


def is_touching(piece, next_piece):
    next_piece_tuple = (next_piece.x, next_piece.y)
    
    (piece.x, piece.y), (piece.x - 1, piece.y - 1), (piece.x, piece.y - 1), (piece.x + 1, piece.y - 1),
                          (piece.x - 1, piece.y), (piece.x + 1, piece.y), (piece.x - 1, piece.y + 1), (piece.x, piece.y + 1),
                          (piece.x + 1, piece.y + 1)]
    return (next_piece.x, next_piece.y) in touching_positions


if __name__ == "__main__":
    head, tail = process()
    for position in tail.positions:
        print(position)
    unique_tail_tuples = []
    for tail_tuple in tail.positions:
        if tail_tuple not in unique_tail_tuples:
            unique_tail_tuples.append(tail_tuple)
    print(len(unique_tail_tuples))

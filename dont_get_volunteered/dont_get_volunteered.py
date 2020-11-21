from collections import deque


def solution(src, dest):
    """Uses breadth first search algorithm to find least amount of moves."""
    chessboard = Chessboard()

    queue = deque()
    queue.append(Node(src, 0))

    while(len(queue) > 0):
        this_elem = queue.popleft()

        if this_elem.index == dest:
            return this_elem.distance

        valid_moves = chessboard.get_valid_moves(this_elem.index)
        for move in valid_moves:
            move_node = Node(move, this_elem.distance + 1)
            if move_node not in queue:
                queue.append(move_node)


class Chessboard:
    """Chessboard class to help get points on the chessboard and valid moves.

    Probably slightely inefficient but I use a dictionary and a 2D array to
    easily convert between coordinates and the board index.
    """

    def __init__(self):
        self._chessboard = []
        self._chessboard_map = {}

        self._init_board()

    def _init_board(self):
        """Initializes the board and the board map."""
        index = 0
        for _row in range(0, 8):
            row = []
            for _col in range(0, 8):
                row.append(index)
                self._chessboard_map[index] = (_row, _col)
                index += 1
            self._chessboard.append(row)

    def get_coords(self, index):
        """Get coordinates of chessboard square for given index."""
        return self._chessboard_map[index]

    def get_index(self, x, y):
        return self._chessboard[x][y]

    def get_valid_moves(self, index):
        """Gets a list of valid indices from this index for all knight moves."""
        valid_moves = []
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]
        this_x, this_y = self.get_coords(index)
        for move in knight_moves:
            move_x = this_x + move[0]
            move_y = this_y + move[1]
            if move_x < 0 or move_x > 7 or move_y < 0 or move_y > 7:
                continue
            valid_moves.append(self.get_index(move_x, move_y))

        return valid_moves


class Node:
    """Node class to put into the BFS algorithm queue."""

    def __init__(self, index, distance):
        self.index = index
        self.distance = distance

    def __eq__(self, other):
        return self.index == other.index


if __name__ == '__main__':
    print(solution(0, 1)) # Should be 3
    print(solution(19, 36)) # Should be 1
    chessboard = Chessboard()
    src = chessboard.get_index(7, 0)
    dest = chessboard.get_index(0, 7)
    print(solution(src, dest)) # Should be 6

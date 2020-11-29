from fractions import Fraction
from fractions import gcd

def solution(matrix):
    mat = AbsorbingMarkhovChain(matrix)
    abs_probs = mat.get_result()

    if sum(matrix[0]) == 0:
        # Check for case where s0 is absorbing - we don't need to do lcm.
        return abs_probs

    l = 1
    for item in abs_probs:  # Find least common multiple for all fractions
        l = lcm(l, item.denominator)

    # Convert fractions into integers with least common demoninator
    result = [x.numerator * l // x.denominator for x in abs_probs]
    result.append(l)  # Append lease common denominator to result list
    return result


def lcm(x, y):
    """Calculate lowest common mulitple of x and y."""
    return abs(x * y) // gcd(x, y)


class AbsorbingMarkhovChain:

    def __init__(self, matrix):
        self.n_transient = 0
        self.n_absorbing = 0
        self.n_states = len(matrix)
        self.result_probabilities = None

        self.P = []  # The transition matrix (albeit without the Identity part)
        self.Q = []  # Describes transitions between transient states
        self.R = []  # Describes transitions from transient to absorbative states
        self.N = []  # The fundamental matrix

        if sum(matrix[0]) != 0: # Check that s0 isn't an absorbing state
            self._init_P_matrix(matrix)
            self._init_Q_R()
            self._calc_N()
            self._calc_absorption_probabilities()
        else:
            # If s0 is absorbing return [1, 1] since it never leaves s0
            self.result_probabilities = [1, 1]


    def get_result(self):
        return self.result_probabilities

    def _init_P_matrix(self, matrix):
        """Converts the input matrix into a transition matrix, P.

        We also need to sort the matrix appropriately in the cases where the
        absorbing states aren't given at the bottom rows of the matrix.
        """
        transients = []
        absorbatives = []
        trans_indices = []
        abs_indices = []

        for n, row in enumerate(matrix):
            if sum(row) == 0:
                absorbatives.append([Fraction(0, 1) for x in row])
                abs_indices.append(n)
            else:
                transients.append([Fraction(x, sum(row)) for x in row])
                trans_indices.append(n)

        self.n_transient = len(transients)
        self.n_absorbing = len(absorbatives)

        # Place absorbaitve states on the bottom most rows of the matrix
        new_matrix = transients + absorbatives
        new_col_order = trans_indices + abs_indices

        for row in new_matrix:
            self.P.append([row[j] for j in new_col_order]) # Swap columns


    def _init_Q_R(self):
        """Extracts the Q and R matrix from the transition matrix, P."""

        self.Q = [row[:self.n_transient] for row in self.P[:self.n_transient]]
        self.R = [row[self.n_transient:] for row in self.P[:self.n_transient]]

    def _calc_N(self):
        """Calculates the fundamental matrix N = inverse(I - Q)."""
        I_minus_Q = []
        for i in range(0, self.n_transient):  # rows
            row = []
            for j in range(0, self.n_transient):  # columns
                x = 1 if i == j else 0
                row.append(x - self.Q[i][j])
            I_minus_Q.append(row)

        self.N = self.invert_matrix(I_minus_Q)

    def _calc_absorption_probabilities(self):
        """Calculates the probabilities of ending up in each absorption state.

        Note that I am only calculating the top row of this matrix since the
        problem states that the ore always starts in state s0.
        """
        result_probabilities = []
        N_top_row = self.N[0]
        for i in range(0, len(self.R[0])):
            _sum = 0
            for j in range(0, len(N_top_row)):
                _sum += N_top_row[j] * self.R[j][i]
            result_probabilities.append(_sum)

        self.result_probabilities = result_probabilities

    @staticmethod
    def get_identity(dim):
        """Returns a dim by dim identity matrix."""
        I = []
        for i in range(0, dim):
            row = []
            for j in range(0, dim):
                x = Fraction(1, 1) if i == j else Fraction(0, 1)
                row.append(x)
            I.append(row)
        return I

    def invert_matrix(self, matrix):
        """Inverts the matrix if possible using Gauss-Jordan algorithm."""
        N = len(matrix)
        Im = self.get_identity(N)

        indices = list(range(N))
        for focus in range(0, N):  # Focus -- the diagonal terms
            scale = 1 / matrix[focus][focus]
            for j in range(N):  # Scale this row by diagonal term
                matrix[focus][j] *= scale
                Im[focus][j] *= scale
            for i in indices[0:focus] + indices[focus + 1:]:  # Non diagonals
                row_scale = matrix[i][focus]
                for j in range(N):
                    matrix[i][j] = matrix[i][j] - row_scale * matrix[focus][j]
                    Im[i][j] = Im[i][j] - row_scale * Im[focus][j]

        return Im


if __name__ == '__main__':
    print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4],
                    [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]))
    print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))

    # Found additional test cases online for the pesky scenarios when the
    # absorbing states aren't at the bottom rows of the matrix -> See df_test.py

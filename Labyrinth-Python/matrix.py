from tile import Tile
from collections import deque

DIMENSION = 7


class Matrix(object):
    """Class representing a matrix of NB_ROWS * NB_ROWS with default value in each cell"""

    def __init__(self, default_value=0):
        matrix = {}
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                matrix[(i, j)] = default_value
        self.matrix = matrix

    def get_value(self, row, col) -> Tile:
        """Return the value in the matrix at the line and column passed as parameters"""
        assert row >= 0 and row < DIMENSION, "Row out of bounds"
        assert col >= 0 and col < DIMENSION, "Column out of bounds"
        return self.matrix[row, col]

    def set_value(self, row, col, value) -> None:
        """Set the value in the matrix at the line and column passed as parameters"""
        assert row >= 0 and row < DIMENSION, "Row out of bounds"
        assert col >= 0 and col < DIMENSION, "Column out of bounds"
        self.matrix[row, col] = value

    def shift_row_left(self, row_index, updated_value=0) -> int:
        """Shifts the row at the index passed as parameter to the left by one cell
        and inserts the updated value in the cell that was ejected by the shift
        Returns the value of the cell that was ejected by the shift"""

        assert row_index >= 0 and row_index < DIMENSION, "Row index out of bounds"
        assert updated_value != None, "Updated value cannot be None"
        assert row_index % 1 == 0, "Row index must be odd"

        ejected_value = self.get_value(row_index, 0)
        for j in range(DIMENSION - 1):
            self.set_value(row_index, j, self.get_value(row_index, j + 1))
        self.set_value(row_index, DIMENSION - 1, updated_value)
        return ejected_value

    def shift_row_right(self, row_index, updated_value=0) -> int:
        """Shifts the row at the index passed as parameter to the right by one cell
        and inserts the updated value in the cell that was ejected by the shift
        Returns the value of the cell that was ejected by the shift"""

        assert row_index >= 0 and row_index < DIMENSION, "Row index out of bounds"
        assert updated_value != None, "Updated value cannot be None"
        assert row_index % 1 == 0, "Row index must be odd"

        ejected_value = self.get_value(row_index, DIMENSION - 1)
        for j in range(DIMENSION - 1, 0, -1):
            self.set_value(row_index, j, self.get_value(row_index, j - 1))
        self.set_value(row_index, 0, updated_value)
        return ejected_value

    def shift_column_up(self, col_index, updated_value=0) -> int:
        """Shifts the column at the index passed as parameter up by one cell
        and inserts the updated value in the cell that was ejected by the shift
        Returns the value of the cell that was ejected by the shift"""

        assert col_index >= 0 and col_index < DIMENSION, "Column index out of bounds"
        assert updated_value != None, "Updated value cannot be None"
        assert col_index % 1 == 0, "Column index must be odd"

        ejected_value = self.get_value(0, col_index)
        for i in range(DIMENSION - 1):
            self.set_value(i, col_index, self.get_value(i + 1, col_index))
        self.set_value(DIMENSION - 1, col_index, updated_value)
        return ejected_value

    def shift_column_down(self, col_index, updated_value=0):
        """Shifts the column at the index passed as parameter down by one cell
        and inserts the updated value in the cell that was ejected by the shift
        Returns the value of the cell that was ejected by the shift"""

        assert col_index >= 0 and col_index < DIMENSION, "Column index out of bounds"
        assert updated_value != None, "Updated value cannot be None"
        assert col_index % 1 == 0, "Column index must be odd"

        ejected_value = self.get_value(DIMENSION - 1, col_index)
        for i in range(DIMENSION - 1, 0, -1):
            self.set_value(i, col_index, self.get_value(i - 1, col_index))
        self.set_value(0, col_index, updated_value)
        return ejected_value

    def get_matrice_accessibilite(self, start_x, start_y):
        """Génère une matrice 7x7 avec des 1 pour les tuiles accessibles depuis la position d'origine (start_x, start_y).
        
        Args:
            start_x (int): Coordonnée x de départ.
            start_y (int): Coordonnée y de départ.

        Returns:
            List[List[int]]: Matrice 7x7 représentant les tuiles accessibles (1 = accessible, 0 = inaccessible).
        """
        accessible_matrix = [[0 for _ in range(DIMENSION)] for _ in range(DIMENSION)]

        # file pour suivre tuiles visiter
        visited = set()
        queue = deque([(start_x, start_y)])

        # marque la tuile de départ 
        accessible_matrix[start_x][start_y] = 1
        visited.add((start_x, start_y))

        while queue:
            x, y = queue.popleft()

            if x > 0 and self.get_value(x, y).can_go_north(self.get_value(x - 1, y)) and (x - 1, y) not in visited:
                visited.add((x - 1, y))
                accessible_matrix[x - 1][y] = 1
                queue.append((x - 1, y))

            if x < DIMENSION - 1 and self.get_value(x, y).can_go_south(self.get_value(x + 1, y)) and (x + 1, y) not in visited:
                visited.add((x + 1, y))
                accessible_matrix[x + 1][y] = 1
                queue.append((x + 1, y))

            if y > 0 and self.get_value(x, y).can_go_west(self.get_value(x, y - 1)) and (x, y - 1) not in visited:
                visited.add((x, y - 1))
                accessible_matrix[x][y - 1] = 1
                queue.append((x, y - 1))

            if y < DIMENSION - 1 and self.get_value(x, y).can_go_east(self.get_value(x, y + 1)) and (x, y + 1) not in visited:
                visited.add((x, y + 1))
                accessible_matrix[x][y + 1] = 1
                queue.append((x, y + 1))

        return accessible_matrix
    
    def get_matrice_tuiles(self):
        """Génère une matrice 7x7 avec les valeurs des tuiles du plateau.
        
        Returns:
            List[List[Tile]]: Matrice 7x7 représentant les tuiles du plateau.
        """
        tuiles_matrix = [[self.get_value(i, j).to_char() for j in range(DIMENSION)] for i in range(DIMENSION)]
        return tuiles_matrix
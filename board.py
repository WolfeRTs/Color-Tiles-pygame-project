from collections import Counter
from random import choices
import pygame


class Board:

    MAX_AMOUNT_COLOR = 20
    MAX_AMOUNT_EMPTY = 145
    COLORS = ['green', 'gray', 'red', 'light_blue', 'dark_blue', 'yellow', 'orange', 'brown', 'pink', 'purple', 'empty']
    DIRECTIONS = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    def __init__(self, block_size: float, num_rows: int, num_cols: int):
        self._block_size = block_size
        self._rows = num_rows
        self._cols = num_cols
        self.matrix = []
        self.randomize_matrix()

    def draw_board(self, screen):
        """Draws the randomly generated matrix on the screen"""
        for row in range(self._rows):
            for col in range(self._cols):
                if self.matrix[row][col] == 'empty':
                    continue
                tile = pygame.image.load(f'images/{self.matrix[row][col]}.png')
                screen.blit(tile, (self._block_size * (col + 1), self._block_size * (row + 1)))

    def randomize_matrix(self):
        """Creates a randomly generated 2D matrix"""
        matrix = []
        colors_amount = {color: 0 for color in self.COLORS}
        weights = [self.MAX_AMOUNT_COLOR - y if x != 'empty'
                   else self.MAX_AMOUNT_EMPTY - y for x, y in colors_amount.items()]
        for row in range(self._rows):
            current_row = []
            for col in range(self._cols):
                block = choices(self.COLORS, weights=tuple(weights), k=1)[0]
                while True:
                    if self.__valid_matrix_block(block, colors_amount):
                        break
                    block = choices(self.COLORS, weights=tuple(weights), k=1)[0]
                current_row.append(block)
                colors_amount[block] += 1
                weights[self.COLORS.index(block)] -= 1
            matrix.append(current_row)
        self.matrix = matrix

    def calculate_points(self, click_position: tuple) -> int:
        """Calculate points based on a valid move or any matches.
        Returns 2 values - the changed matrix (if there were any matches) and points depending on the case:
        --> -1 if the player clicked out of the board or on a block
        --> 0 if there aren't any matches
        --> positive value between 2 and 4 if there are any matches"""
        current_row, current_col = click_position
        if not self.__valid_click(current_row, current_col, self._rows, self._cols) or self.matrix[current_row][current_col] != 'empty':
            return -1
        direction_blocks = {'up': {'color': None, 'coordinates': tuple()},
                            'down': {'color': None, 'coordinates': tuple()},
                            'left': {'color': None, 'coordinates': tuple()},
                            'right': {'color': None, 'coordinates': tuple()}}

        for direction in self.DIRECTIONS:
            next_row, next_col = current_row + self.DIRECTIONS[direction][0], current_col + self.DIRECTIONS[direction][1]
            while self.__valid_click(next_row, next_col, self._rows, self._cols):
                if self.matrix[next_row][next_col] != 'empty':
                    direction_blocks[direction]['color'] = self.matrix[next_row][next_col]
                    direction_blocks[direction]['coordinates'] = (next_row, next_col)
                    break
                next_row, next_col = next_row + self.DIRECTIONS[direction][0], next_col + self.DIRECTIONS[direction][1]

        blocks_for_removal = self.__valid_matches(direction_blocks)
        points = self.__remove_blocks(blocks_for_removal, direction_blocks)
        return points

    @staticmethod
    def __valid_click(row: int, col: int, rows_size: int, cols_size: int) -> bool:
        """Checks if the clicked position is a valid game move"""
        if row in range(rows_size) and col in range(cols_size):
            return True
        return False

    @staticmethod
    def __valid_matches(found_blocks: dict[str: dict]) -> list[str]:
        """Checks for any valid block matches in four directions (up, down, left, right)"""
        found_colors = [found_blocks[direction]['color'] for direction in found_blocks if
                        found_blocks[direction]['color']]
        blocks_to_be_removed = []
        colors_amount = Counter(found_colors)
        for color, amount in colors_amount.items():
            if amount > 1:
                blocks_to_be_removed.append(color)
        return blocks_to_be_removed

    def __valid_matrix_block(self, block_variation: str, amounts: dict[str: int]) -> bool:
        """Checks if the randomly chosen color variation is valid for adding to the matrix"""
        if block_variation == 'empty' and amounts['empty'] < self.MAX_AMOUNT_EMPTY:
            return True
        if amounts[block_variation] == self.MAX_AMOUNT_COLOR or amounts[block_variation] == self.MAX_AMOUNT_EMPTY:
            return False
        return True

    def __remove_blocks(self, blocks_to_be_removed: list[str], found_blocks: dict[str: dict]) -> int:
        """Removes matched blocks (if there are any) and returns their count"""
        if not blocks_to_be_removed:
            return 0
        count_removed_blocks = 0
        for direction in found_blocks:
            if found_blocks[direction]['color'] in blocks_to_be_removed:
                row, col = found_blocks[direction]['coordinates']
                self.matrix[row][col] = 'empty'
                count_removed_blocks += 1
        return count_removed_blocks

from operator import le
import time

class Game:
    def __init__(self):
        self.is_game_over = False
        self.initialize_game()

    def initialize_game(self):
        self.board_cell_n = int(input('Board is n*n. Please enter n: '))
        self.current_state = []
        for i in range(0, self.board_cell_n):
            newRow = []
            for j in range(0, self.board_cell_n):
                newRow.append('.')
            self.current_state.append(newRow)

        # نوبت اولین بازیکن
        self.player_turn = 'X'

    def draw_board(self):
        for i in range(0, self.board_cell_n):
            for j in range(0, self.board_cell_n):
                print('{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    def is_valid(self, px, py):
        if px < 0 or px > self.board_cell_n - 1 or py < 0 or py > self.board_cell_n - 1:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):
        # Vertical win
        for i in range(0, self.board_cell_n):
            column = []
            for j in range(0, self.board_cell_n):
                column.append(self.current_state[j][i])
            column = list(dict.fromkeys(column))
            if len(column) == 1 and column[0] != '.': return column[0]

        # Horizontal win
        for i in range(0, self.board_cell_n):
            row_x = []
            row_o = []
            for j in range(0, self.board_cell_n): row_x.append('X')
            for j in range(0, self.board_cell_n): row_o.append('O')
            if (self.current_state[i] == row_x):
                return 'X'
            elif (self.current_state[i] == row_o):
                return 'O'

        # Main diagonal win
        diagonal_left_to_right = []
        for i in range(0, self.board_cell_n):
            diagonal_left_to_right.append(self.current_state[i][i])
        diagonal_left_to_right = list(dict.fromkeys(diagonal_left_to_right))
        if len(diagonal_left_to_right) == 1 and diagonal_left_to_right[0] != '.': return diagonal_left_to_right[0]

        # Second diagonal win
        diagonal_right_to_left = []
        for i in range(0, self.board_cell_n):
            diagonal_right_to_left.append(self.current_state[i][self.board_cell_n - (i + 1)])
        diagonal_right_to_left = list(dict.fromkeys(diagonal_right_to_left))
        if len(diagonal_right_to_left) == 1 and diagonal_right_to_left[0] != '.': return diagonal_right_to_left[0]


        # چک میکنه جای خالی هست رو برد یا ن
        for i in range(0, self.board_cell_n):
            for j in range(0, self.board_cell_n):
                if (self.current_state[i][j] == '.'):
                    return None

        # It's a tie!
        return '.'

    def max_alpha_beta(self, alpha, beta):
        maxv = -3
        px = None
        py = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, self.board_cell_n):
            for j in range(0, self.board_cell_n):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'

                    # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                    if maxv >= beta:
                        return (maxv, px, py)

                    if maxv > alpha:
                        alpha = maxv

        return (maxv, px, py)

    def min_alpha_beta(self, alpha, beta):
        minv = 3

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, self.board_cell_n):
            for j in range(0, self.board_cell_n):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'

                    if minv <= alpha:
                        return (minv, qx, qy)

                    if minv < beta:
                        beta = minv

        return (minv, qx, qy)

    def play(self):
        # برای اینکه فقط هوش مصنوعی دربرابر هوش مصنوعی بازی کند این بولین رو تغییر دهید
        is_both_ai = True

        while True:
            self.draw_board()
            self.result = self.is_end()

            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("It's a tie!")


                # self.initialize_game()
                self.draw_board()
                return

            if self.player_turn == 'X':

                while True:
                    start = time.time()
                    (m, qx, qy) = self.min_alpha_beta(-3, 3)
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 7)))

                    if is_both_ai == False:
                        print('Recommended move: X = {}, Y = {}'.format(qx, qy))
                        px = int(input('Insert the X coordinate: '))
                        py = int(input('Insert the Y coordinate: '))

                        qx = px
                        qy = py

                    px = qx
                    py = qy

                    if self.is_valid(px, py):
                        self.current_state[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('The move is not valid! Try again.')

            else:
                (m, px, py) = self.max_alpha_beta(-3, 3)
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'

def main():
    g = Game()
    g.play()

if __name__ == "__main__":
    main()
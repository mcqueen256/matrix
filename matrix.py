# import libraries for whole file to use 
import curses
import time
import random

FREQ = 0.01

# TODO: handle resize
# TODO: grow columns
# TODO: mutate symbol
# TODO: shift group of symbols
# TODO: implement do_nothing
# TODO: add japanese characters
# TODO: Add bold chars

MUTATION_DURATION = 10

class SymbolState:
    MUTATING = 0
    FIXED = 1

class Symbol(object):
    symbols = []

    def __init__(self, matrix, column, y):
        super()
        self._matrix = matrix
        self._column = column
        self._char_list = [
            str(x) for x in range(10)
        ]
        self._char_list.extend([
            chr(x) for x in range(ord('a'), ord('z') + 1)
        ])
        self._char_list.extend([
            chr(x) for x in range(ord('A'), ord('Z') + 1)
        ])
        self._char = random.choice(self._char_list)
        # if self._mutating == None then this symbols is not in a mutating
        # state, otherwise it is a positive int of remaining mutations to
        # undergo. On creation, symbols mutate.
        self.state = {
            'mutating': MUTATION_DURATION,
            'x': self._column.x,
            'y': y,
        }

        Symbol.symbols.append(self)
    
    def update(self):
        if self.mutating is not None:
            self.mutate()
            self.draw()
    
    def mutate(self):
        pass
    
    def start_mutation(self):
        self._mutating = MUTATION_DURATION
    
    def draw(self):
        self.matrix.scr.move(self.y, self.x)
        self.matrix.scr.addstr(self._char)
    
    @property
    def matrix(self):
        return self._matrix
    @property
    def mutating(self):
        return self.state['mutating']
    @property
    def x(self):
        return self.state['x']
    @property
    def y(self):
        return self.state['y']


class Column(object):
    def __init__(self, matrix, x):
        super()
        self._matrix = matrix
        self._symbols = []
        self._x = x
    
    def grow(self):
        # if the column is full, do not grow it.
        if self._matrix.height <= len(self) + 1: return
        self._symbols.append(Symbol(self._matrix, self, len(self)))
    
    def update(self):
        for symbol in self._symbols:
            symbol.update()
    
    def __len__(self):
        return len(self._symbols)

    @property
    def x(self):
        return self._x


class Matrix(object):
    def __init__(self, stdscr):
        super()
        stdscr.clear()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        stdscr.nodelay(True)
        self._stdscr = stdscr
        self._iterations = 0
        self._height = curses.LINES - 1
        self._width = curses.COLS - 1
        self._columns = [Column(self, i) for i, _ in enumerate(range(self._width))]

    def loop(self):
        ops = [
            'grow',
            'mutate',
            'shift',
            'do nothing',
        ]
        user_input = self._stdscr.getch()
        # TODO: fix the exit condition
        while user_input != ord('q'):
            self._op_grow()
            self.scr.clear()
            self._iterations += 1
            for column in self._columns:
                column.update()
            self.scr.refresh()
            time.sleep(FREQ)

    @property
    def scr(self):
        return self._stdscr
    @property
    def height(self):
        return self._height
    @property
    def width(self):
        return self._width

    def _op_grow(self):
        """Select a random column to add a single symbol to."""
        column = random.choice(self._columns)
        column.grow()
        

def main():
    # starts the library
    try:
        stdscr = curses.initscr()
        matrix = Matrix(stdscr)
        matrix.loop()

        # def choose_col():
        #     col_n = random.randint(0, width-1)
        #     return col_n
        # def choose_symbol():
        #     pass

        # def grow():
        #     col_n = choose_col()
        #     col = columns[col_n]
        #     col.append('x')
        #     stdscr.move(len(col) - 1, col_n)
        #     stdscr.addstr("x")
        #     pass
        # def mutate():
        #     # stdscr.addstr("mutate ")
        #     pass
        # def shift():
        #     pass
        # def do_nothing():
        #     # stdscr.addstr("do_nothing ")
        #     pass
        # operations = [grow, mutate, shift, do_nothing]

        # # update the matrix interface
        # user_input = stdscr.getch()
        # while user_input != ord('q'):
        #     op_count = random.randint(0, MAX_OP_COUNT)
        #     f = operations[random.randint(0,len(operations)-1)]
        #     f()
        #     iterations += 1
        #     time.sleep(0.01)
        #     stdscr.refresh()
    finally:
        curses.endwin()


if __name__ == "__main__":
    main()

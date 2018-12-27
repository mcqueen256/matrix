'''
        The Matrix Script
        =================
        > Run with python 3
'''
import curses
import time
import random

# Constants
FREQ = 0.001
MUTATION_DURATION = 50


class Symbol:
    '''Single character on the terminal'''

    def __init__(self, matrix, column, y):
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
        self._char_list.extend(self._char_list)
        self._char_list.extend(self._char_list)
        self._char_list.extend(self._char_list)
        # japanese numbers
        self._char_list.extend([
            chr(x) for x in range(12321, 12330)
        ])
        # japanese chars
        self._char_list.extend([
            chr(x) for x in range(12337, 12347)
        ])
        # more japanese chars
        self._char_list.extend([
            chr(x) for x in range(12353, 12439)
        ])
        # more japanese chars
        self._char_list.extend([
            chr(x) for x in range(12443, 12543)
        ])
        # more japanese chars
        self._char_list.extend([
            chr(x) for x in range(12549, 12590)
        ])
        # if self._mutating == None then this symbols is not in a mutating
        # state, otherwise it is a positive int of remaining mutations to
        # undergo. On creation, symbols mutate.

        # made state a named collection incase I want to transfure object properties
        self.state = {
            'mutating': MUTATION_DURATION,
            'x': self._column.x,
            'y': y,
            'char': random.choice(self._char_list),
        }
    
    def update(self):
        '''Change state of symbol if required'''
        if self.mutating is not None:
            self.mutate()
            self.draw()
    
    def mutate(self):
        if self.mutating is None: return
        if self.mutating == 0:
            self.state['mutating'] = None
        else:
            self.state['mutating'] -= 1
        self.state['char'] = random.choice(self._char_list)

    
    def start_mutation(self):
        self.state['mutating'] = MUTATION_DURATION
    
    def draw(self):
        self.matrix.scr.move(self.y, self.x)
        self.matrix.scr.addstr(self.char)
    
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
    @property
    def char(self):
        return self.state['char']


class Column:
    '''Stores a column of symbols for every column on the terminal'''

    def __init__(self, matrix, x):
        self._matrix = matrix
        self._symbols = []
        self._x = x
    
    def grow(self):
        # if the column is full, do not grow it.
        if self._matrix.height <= len(self) + 1: return
        self._symbols.append(Symbol(self._matrix, self, len(self)))

    def shift_random(self):
        if len(self._symbols) <= 1: return
        if self._matrix.height <= len(self) + 1:
            self._symbols.remove(self._symbols[-1])
        pos = random.randint(0, len(self._symbols) - 1)
        for s in self._symbols[pos:]:
            s.state['y'] += 1
        self._symbols.insert(pos, Symbol(self._matrix, self, pos))
        for s in self._symbols:
            s.draw()
    
    def update(self):
        for symbol in self._symbols:
            symbol.update()
        
    def __len__(self):
        return len(self._symbols)

    @property
    def x(self):
        return self._x


class Matrix:
    '''This object stores the columns and manipulates them'''

    def __init__(self, stdscr):
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
        user_input = self._stdscr.getch()
        # TODO: fix the exit condition
        while user_input != ord('q'):
            column = random.choice(self._columns)
            # TODO: clean up 'column._symbols'
            symbol = random.choice(column._symbols) if len(column._symbols) != 0 else None
            ops = [
                lambda: column.grow(),
                lambda: symbol.start_mutation() if symbol is not None else 0,
                lambda: column.shift_random(),
                # lambda: column.split_n_drop(),
                lambda: 0
            ]
            op = random.choice(ops)
            op()
            # self.scr.clear()
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

def main():
    try:
        stdscr = curses.initscr()
        matrix = Matrix(stdscr)
        matrix.loop()
    finally:
        curses.endwin()

if __name__ == "__main__":
    main()

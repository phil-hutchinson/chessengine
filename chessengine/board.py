class Board:
    def __init__(self):
        self.squares = {}
        self.next_to_play = 'W'
        self.white_kingside_castle = True
        self.white_queenside_castle = True
        self.black_kingside_castle = True
        self.black_queenside_castle = True
        self.en_passant_file = None
        
    def starting_pos(self):
        self.squares = {}
        self.squares[(1,1)] = 'WR'
        self.squares[(2,1)] = 'WN'
        self.squares[(3,1)] = 'WB'
        self.squares[(4,1)] = 'WQ'
        self.squares[(5,1)] = 'WK'
        self.squares[(6,1)] = 'WB'
        self.squares[(7,1)] = 'WN'
        self.squares[(8,1)] = 'WR'
        self.squares[(1,8)] = 'BR'
        self.squares[(2,8)] = 'BN'
        self.squares[(3,8)] = 'BB'
        self.squares[(4,8)] = 'BQ'
        self.squares[(5,8)] = 'BK'
        self.squares[(6,8)] = 'BB'
        self.squares[(7,8)] = 'BN'
        self.squares[(8,8)] = 'BR'
        for file in range(1, 9):
            self.squares[(file, 2)] = 'WP'
            self.squares[(file, 7)] = 'BP'
        self.next_to_play = 'W'
        self.white_kingside_castle = True
        self.white_queenside_castle = True
        self.black_kingside_castle = True
        self.black_queenside_castle = True
        self.en_passant_file = None
        
    def copy_from(self, other: 'Board') -> None:
        self.squares = other.squares.copy()
        self.next_to_play = other.next_to_play
        self.en_passant_file = other.en_passant_file
        self.white_kingside_castle = other.white_kingside_castle
        self.white_queenside_castle = other.white_queenside_castle
        self.black_kingside_castle = other.black_kingside_castle
        self.black_queenside_castle = other.black_queenside_castle
        
    def print(self):
        print('-----------------------------------------')
        for rank in range(8, 0, -1):
            line = '|';
            for file in range(1, 9):
                key = (file, rank)
                if key in self.squares:
                    square = self.squares[key]
                    line += ' ' + square + ' |'
                else:
                    line += '    |'
            print(line)
            print('-----------------------------------------')
                    
        

        












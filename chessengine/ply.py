from typing import Union
from board import Board
from notation import Notation

class KingUnderAttack(Exception):
    def __init__(self, message='King under attack'):
        self.message = message
        super().__init__(self.message)

class Ply:
    def __init__(self, old_board: Board, new_board: Board, ply_notation: str):
        self.old_board = old_board
        self.new_board = new_board
        self.ply_notation = ply_notation
        
    @staticmethod
    def find_all_valid_plies(starting_board: Board) -> list['Ply']:
        all_plies = Ply.find_all_plies(False, starting_board)
        valid_plies = filter(lambda m: not Ply.king_left_under_attack(m.new_board), all_plies)
        return list(valid_plies)

    @staticmethod
    def find_all_plies(for_check_under_attack: bool, starting_board: Board) -> list['Ply']:
        # note that this includes illegal plies that leave the player in check
        # use find_all_valid_plies to exclude these plies.
        return_value: list[Ply] = []
        for file in range(1, 9):
            for rank in range(1, 9):
                key = (file, rank)
                if key in starting_board.squares:
                    ply_result = Ply.find_all_plies_from_square(for_check_under_attack, starting_board, file, rank)
                    return_value += ply_result
                    
        return return_value
    
    @staticmethod
    def find_all_plies_from_square(for_check_under_attack: bool, starting_board: Board, file: int, rank: int) -> list['Ply']:
        return_value: list[Ply] = []
        key = (file, rank)
        if key in starting_board.squares:
            square = starting_board.squares[key]
            piece_colour = square[0]
            if piece_colour == starting_board.next_to_play:
                piece_type = square[1]
                if piece_type == 'K':
                    return_value += Ply.find_all_king_plies_from_square(for_check_under_attack, starting_board, piece_colour, file, rank)
                elif piece_type == 'Q':
                    return_value += Ply.find_all_queen_plies_from_square(starting_board, piece_colour, file, rank)
                elif piece_type == 'R':
                    return_value += Ply.find_all_rook_plies_from_square(starting_board, piece_colour, file, rank)
                elif piece_type == 'B':
                    return_value += Ply.find_all_bishop_plies_from_square(starting_board, piece_colour, file, rank)
                elif piece_type == 'N':
                    return_value += Ply.find_all_knight_plies_from_square(starting_board, piece_colour, file, rank)
                elif piece_type == 'P':
                    return_value += Ply.find_all_pawn_plies_from_square(starting_board, piece_colour, file, rank)
                    
        return return_value

    @staticmethod
    def find_all_king_plies_from_square(for_check_under_attack: bool, starting_board: Board, piece_colour: str, file: int, rank: int) -> list['Ply']:
        return_value: list['Ply'] = []

        if piece_colour == 'W':
            piece = 'WK'
            opposite_colour = 'B'
        else:
            piece = 'BK'
            opposite_colour = 'W'

        starting_pos = (file, rank)
        
        possible_end_pos = [
                (file - 1, rank - 1),
                (file - 1, rank),
                (file - 1, rank + 1),
                (file, rank - 1),
                (file, rank + 1),
                (file + 1, rank - 1),
                (file + 1, rank),
                (file + 1, rank + 1),
            ]
        
        for end_pos in possible_end_pos:
            new_board, _ =  Ply.try_ply_piece(starting_board, piece, starting_pos, end_pos)
            if isinstance(new_board, Board):
                return_value.append(Ply(starting_board, new_board, Notation.build_notation(starting_pos, end_pos)))

        if not for_check_under_attack:                
            return_value += Ply.find_all_castling_plies(starting_board)
                
        return return_value
                    
    @staticmethod
    def find_all_queen_plies_from_square(starting_board: Board, piece_colour: str, file: int, rank: int) -> list['Ply']:
        return_value: list['Ply'] = []

        return_value += Ply.find_all_orthogonal_plies_from_square(starting_board, piece_colour, 'Q', file, rank)
        return_value += Ply.find_all_diagonal_plies_from_square(starting_board, piece_colour, 'Q', file, rank)
    
        return return_value
    
    @staticmethod
    def find_all_rook_plies_from_square(starting_board: Board, piece_colour: str, file: int, rank: int) -> list['Ply']:
        return Ply.find_all_orthogonal_plies_from_square(starting_board, piece_colour, 'R', file, rank)
                    
    @staticmethod
    def find_all_bishop_plies_from_square(starting_board: Board, piece_colour: str, file: int, rank: int) -> list['Ply']:
        return Ply.find_all_diagonal_plies_from_square(starting_board, piece_colour, 'B', file, rank)
                    
    @staticmethod
    def find_all_knight_plies_from_square(starting_board: Board, piece_colour: str, file: int, rank: int) -> list['Ply']:
        return_value: list['Ply'] = []

        if piece_colour == 'W':
            piece = 'WN'
            opposite_colour = 'B'
        else:
            piece = 'BN'
            opposite_colour = 'W'

        starting_pos = (file, rank)
        
        possible_end_pos = [
                (file - 2, rank - 1),
                (file - 2, rank + 1),
                (file - 1, rank - 2),
                (file - 1, rank + 2),
                (file + 1, rank - 2),
                (file + 1, rank + 2),
                (file + 2, rank - 1),
                (file + 2, rank + 1),
            ]
        
        for end_pos in possible_end_pos:
            new_board, _ =  Ply.try_ply_piece(starting_board, piece, starting_pos, end_pos)
            if isinstance(new_board, Board):
                return_value.append(Ply(starting_board, new_board, Notation.build_notation(starting_pos, end_pos)))
                
        return return_value
                    
    @staticmethod
    def find_all_pawn_plies_from_square(starting_board: Board, piece_colour: str, file: int, rank: int) -> list['Ply']:
        return_value: list['Ply'] = []
        
        if piece_colour == 'W':
            home_rank = 1
            starting_rank = 2
            direction = 1
            promotion_rank = 8
            piece = 'WP'
            opposite_colour = 'B'
        else:
            home_rank = 8
            starting_rank = 7
            direction = -1
            promotion_rank = 1
            piece = 'BP'
            opposite_colour = 'W'
            
        if rank == promotion_rank:
            raise ValueError('Unpromoted pawn in promotion rank')
        
        if rank == home_rank:
            raise ValueError('Pawn in home rank')
        
        orig_key = (file, rank)

        # try one square ahead
        key_one_square = (file, rank + direction)
        if not key_one_square in starting_board.squares:
            new_board = Ply.ply_piece_or_pawn(starting_board, piece, orig_key, key_one_square)
            return_value += Ply.process_pawn_ply(starting_board, new_board, orig_key, key_one_square, promotion_rank, piece_colour)
            
            # first square was open - try two squares
            if rank == starting_rank:
                key_two_squares = (file, rank + direction * 2)
                if not key_two_squares in starting_board.squares:
                    new_board = Ply.ply_piece_or_pawn(starting_board, piece, orig_key, key_two_squares, new_en_passant_file=file)
                    return_value.append(Ply(starting_board, new_board, Notation.build_notation(orig_key, key_two_squares)))
        
        # try capture
        key_capture_left = (file - 1, rank + direction)
        if key_capture_left in starting_board.squares:
            piece_capture_left = starting_board.squares[key_capture_left]
            if piece_capture_left[0] == opposite_colour:
                if piece_capture_left[1] == 'K':
                    raise KingUnderAttack()
                new_board = Ply.ply_piece_or_pawn(starting_board, piece, orig_key, key_capture_left)
                return_value += Ply.process_pawn_ply(starting_board, new_board, orig_key, key_capture_left, promotion_rank, piece_colour)

        key_capture_right = (file + 1, rank + direction)
        if key_capture_right in starting_board.squares:
            piece_capture_right = starting_board.squares[key_capture_right]
            if piece_capture_right[0] == opposite_colour:
                if piece_capture_right[1] == 'K':
                    raise KingUnderAttack()
                new_board = Ply.ply_piece_or_pawn(starting_board, piece, orig_key, key_capture_right)
                return_value += Ply.process_pawn_ply(starting_board, new_board, orig_key, key_capture_right, promotion_rank, piece_colour)

        # try en passant
        if isinstance(starting_board.en_passant_file, int):
            if (rank == starting_rank + 3 * direction) and (starting_board.en_passant_file == file + 1 or starting_board.en_passant_file == file - 1):
                en_passant_key = (starting_board.en_passant_file, rank + direction)
                new_board = Ply.ply_piece_or_pawn(starting_board, piece, orig_key, en_passant_key)
                rePlyd_piece_key = (starting_board.en_passant_file, rank)
                del new_board.squares[rePlyd_piece_key]
                return_value.append(Ply(starting_board, new_board, Notation.build_notation(orig_key, en_passant_key)))
                    
        return return_value

    @staticmethod
    def find_all_orthogonal_plies_from_square(starting_board: Board, piece_colour: str, piece_type: str, file: int, rank: int) -> list['Ply']:
        return_value: list['Ply'] = []

        piece = piece_colour + piece_type
        starting_pos = (file, rank)
        directions: list[tuple[int,int]] = [
                (-1,0),
                (0,-1),
                (0,1),
                (1,0)
            ]

        for direction in directions:
            return_value += Ply.find_all_directional_plies_from_square(starting_board, piece, file, rank, direction)
                
        return return_value

    @staticmethod
    def find_all_diagonal_plies_from_square(starting_board: Board, piece_colour: str, piece_type: str, file: int, rank: int) -> list['Ply']:
        return_value: list['Ply'] = []

        piece = piece_colour + piece_type
        starting_pos = (file, rank)
        directions: list[tuple[int,int]] = [
                (-1,-1),
                (-1,1),
                (1,-1),
                (1,1)
            ]

        for direction in directions:
            return_value += Ply.find_all_directional_plies_from_square(starting_board, piece, file, rank, direction)
                
        return return_value

    @staticmethod
    def find_all_directional_plies_from_square(starting_board: Board, piece: str, file: int, rank: int, direction: tuple[int,int]) -> list['Ply']:
        return_value: list['Ply'] = []

        piece_colour = piece[0]
        starting_pos = (file, rank)
        can_continue = True
        end_pos = (file, rank)
        
        while can_continue:
            end_pos = (end_pos[0] + direction[0], end_pos[1] + direction[1])
            new_board, occupied =  Ply.try_ply_piece(starting_board, piece, starting_pos, end_pos)
            if isinstance(new_board, Board):
                return_value.append(Ply(starting_board, new_board, Notation.build_notation(starting_pos, end_pos)))
                can_continue = not occupied
            else:
                can_continue = False
                
        return return_value
    
    @staticmethod
    def try_ply_piece(
            starting_board: Board, 
            piece: str,
            starting_pos: tuple[int, int], 
            end_pos: tuple[int, int], 
        ) -> tuple[Union[Board, None], bool]:
        piece_colour = piece[0]
        end_file = end_pos[0]
        end_rank = end_pos[1]
        if end_file < 1 or end_file > 8 or end_rank < 1 or end_rank > 8:
            return None, True
        is_capture = False
        if end_pos in starting_board.squares:
            existing_piece = starting_board.squares[end_pos]
            if existing_piece[0] == piece_colour:
                return None, True
            elif existing_piece[1] == 'K':
                raise KingUnderAttack();
            else:
                is_capture = True
        new_board = Ply.ply_piece_or_pawn(starting_board, piece, starting_pos, end_pos)
        if piece == 'WK':
            new_board.white_kingside_castle = False
            new_board.white_queenside_castle = False
        elif piece == 'BK':
            new_board.black_kingside_castle = False
            new_board.black_queenside_castle = False
        elif starting_pos == (1, 1):
            new_board.white_queenside_castle = False
        elif starting_pos == (8, 1):
            new_board.white_kingside_castle = False
        elif starting_pos == (1, 8):
            new_board.black_queenside_castle = False
        elif starting_pos == (8, 8):
            new_board.black_kingside_castle = False
        return new_board, is_capture

    @staticmethod
    def ply_piece_or_pawn(
            starting_board: Board, 
            piece: str,
            starting_pos: tuple[int, int], 
            end_pos: tuple[int, int], 
            new_en_passant_file: Union[int, None] = None
        ) -> Board:
        new_board = Board()
        new_board.copy_from(starting_board)
        del new_board.squares[starting_pos]
        new_board.squares[end_pos] = piece
        new_board.en_passant_file = new_en_passant_file
        new_board.next_to_play = 'W' if starting_board.next_to_play == 'B' else 'B'
        return new_board
        
    @staticmethod
    def process_pawn_ply(
            starting_board,
            new_board: Board,
            start_pos: tuple[int, int],
            end_pos: tuple[int, int],
            promotion_rank: int,
            piece_colour: str
        ) -> list['Ply']:
        return_value: list[Ply] = []
        if end_pos[1] != promotion_rank:
            return_value.append(Ply(starting_board, new_board, Notation.build_notation(start_pos, end_pos)))
        else:
            queen_board = Board()
            queen_board.copy_from(new_board)
            queen_board.squares[end_pos] = piece_colour + 'Q'
            return_value.append(Ply(starting_board, queen_board, Notation.build_notation(start_pos, end_pos, 'Q')))
            
            rook_board = Board()
            rook_board.copy_from(new_board)
            rook_board.squares[end_pos] = piece_colour + 'R'
            return_value.append(Ply(starting_board, rook_board, Notation.build_notation(start_pos, end_pos, 'R')))

            bishop_board = Board()
            bishop_board.copy_from(new_board)
            bishop_board.squares[end_pos] = piece_colour + 'B'
            return_value.append(Ply(starting_board, bishop_board, Notation.build_notation(start_pos, end_pos, 'B')))

            knight_board = Board()
            knight_board.copy_from(new_board)
            knight_board.squares[end_pos] = piece_colour + 'N'
            return_value.append(Ply(starting_board, knight_board, Notation.build_notation(start_pos, end_pos, 'N')))
            
        return return_value

    @staticmethod
    def find_all_castling_plies(starting_board: Board) -> list['Ply']:
        return_value: list[Ply] = []

        if starting_board.next_to_play == 'W':
            check_kingside = starting_board.white_kingside_castle
            check_queenside = starting_board.white_queenside_castle
            castling_rank = 1
            piece_colour = 'W'
            opposite_colour = 'B'
            king_starting_pos = (5, 1)
        else:
            check_kingside = starting_board.black_kingside_castle
            check_queenside = starting_board.black_queenside_castle
            castling_rank = 8
            piece_colour = 'B'
            opposite_colour = 'W'
            king_starting_pos = (5, 8)

        if not check_kingside and not check_queenside:
            return []
        
        opposite_board = Board()
        opposite_board.copy_from(starting_board)
        opposite_board.next_to_play = opposite_colour
        if Ply.king_left_under_attack(opposite_board):
            return []
        
        #kingside
        if check_kingside:
            rook_end_pos = (6, castling_rank)
            king_end_pos = (7, castling_rank)
            if rook_end_pos not in starting_board.squares and king_end_pos not in starting_board.squares:
                kingside_test_board = Board()
                kingside_test_board.copy_from(opposite_board)
                del kingside_test_board.squares[king_starting_pos]
                kingside_test_board.squares[rook_end_pos] = piece_colour + 'K'
                if not Ply.king_left_under_attack(kingside_test_board):
                    kingside_board, _ = Ply.try_ply_piece(starting_board, piece_colour + 'K', king_starting_pos, king_end_pos)
                    rook_start_pos = (8, castling_rank)
                    del kingside_board.squares[rook_start_pos]
                    kingside_board.squares[rook_end_pos] = piece_colour + 'R'
                    return_value.append(Ply(starting_board, kingside_board, Notation.build_notation(king_starting_pos, king_end_pos)))

        if check_queenside:
            rook_end_pos = (4, castling_rank)
            king_end_pos = (3, castling_rank)
            b_file_pos = (2,castling_rank)
            if rook_end_pos not in starting_board.squares and king_end_pos not in starting_board.squares and b_file_pos not in starting_board.squares:
                queenside_test_board = Board()
                queenside_test_board.copy_from(opposite_board)
                del queenside_test_board.squares[king_starting_pos]
                queenside_test_board.squares[rook_end_pos] = piece_colour + 'K'
                if not Ply.king_left_under_attack(queenside_test_board):
                    queenside_board, _ = Ply.try_ply_piece(starting_board, piece_colour + 'K', king_starting_pos, king_end_pos)
                    rook_start_pos = (1, castling_rank)
                    del queenside_board.squares[rook_start_pos]
                    queenside_board.squares[rook_end_pos] = piece_colour + 'R'
                    return_value.append(Ply(starting_board, queenside_board, Notation.build_notation(king_starting_pos, king_end_pos)))

        return return_value

    
    @staticmethod
    def king_left_under_attack(board: Board) -> bool:
        try:
            Ply.find_all_plies(True, board)
        except KingUnderAttack as _:
            return True
        return False
            
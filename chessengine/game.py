from typing import Union
from board import Board
from enum import Enum
from ply import Ply


class GameStatus(Enum):
    ACTIVE = 1
    DRAW = 2
    WHITE_VICTORY = 3
    BLACK_VICTORY = 4
    
class VictoryCondition(Enum):
    CHECKMATE = 1
    TOTAL_CAPTURE = 2
    PAWN_PROMOTION = 3
    
class Game:
    def __init__(self, victory_condition: VictoryCondition = VictoryCondition.CHECKMATE, board: Board = None):
        if (board == None):
            self.board = Board()
            self.board.starting_pos()
            self.status = GameStatus.ACTIVE
        else:
            self.board = board
            self.status = GameStatus.ACTIVE
            # TODO - look at board to determine GameStatus
        
        self.allow_forced_skip = (victory_condition == VictoryCondition.CHECKMATE)
        
    #make "move"
    def perform_ply(self, notation: str) -> bool:
        if (notation == 'SKIP'):
            return self.choose_skip()
        all_plies = Ply.find_all_valid_plies(self.board)
        matching_plies = filter(lambda p: p.ply_notation == notation, all_plies)
        user_ply: Ply = next(matching_plies, None)
        if isinstance(user_ply, Ply):
            self.board = user_ply.new_board
            # TODO check for victory conditions
            return True
        else:
            return False
        
    def choose_skip(self) -> bool:
        if not self.allow_forced_skip:
            return False
        
        all_plies = Ply.find_all_valid_plies(self.board)
        if all_plies:
            return False
        
        # skip allowed
        self.board.next_to_play = 'W' if self.board.next_to_play == 'B' else 'B'
        
        # todo check victory conditions?

        next_move_all_plies = Ply.find_all_valid_plies(self.board)
        
        if not next_move_all_plies:
            self.status = GameStatus.DRAW
            
        return True
        
        

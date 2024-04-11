from typing import Optional, Union
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
        
        self.victory_condition = victory_condition
        self.allow_forced_skip = (victory_condition == VictoryCondition.CHECKMATE)
        
    #make "move"
    def perform_ply(self, notation: str) -> bool:
        if (notation == 'PASS'):
            return self.perform_pass()
        all_plies = Ply.find_all_valid_plies(self.board)
        matching_plies = filter(lambda p: p.ply_notation == notation, all_plies)
        user_ply: Ply = next(matching_plies, None)
        if isinstance(user_ply, Ply):
            self.board = user_ply.new_board
            self.check_for_victory(notation)
            return True
        else:
            return False
        
    def perform_pass(self) -> bool:
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
    
    def check_for_victory(self, notation: str) -> Optional[None]:
        if self.victory_condition == VictoryCondition.CHECKMATE:
            next_plies = Ply.find_all_valid_plies(self.board)
            if not next_plies:
                test_board = Board()
                test_board.copy_from(self.board)
                test_board.next_to_play = 'W' if test_board.next_to_play == 'B' else 'B'
                is_in_check = Ply.king_left_under_attack(test_board)
                if is_in_check:
                    self.status = GameStatus.WHITE_VICTORY if self.board.next_to_play == 'B' else GameStatus.BLACK_VICTORY
                else:
                    self.status = GameStatus.DRAW
        elif self.victory_condition == VictoryCondition.TOTAL_CAPTURE:
            pass
            #TODO
        elif self.victory_condition == VictoryCondition.PAWN_PROMOTION:
            pass
            #TODO

        
        

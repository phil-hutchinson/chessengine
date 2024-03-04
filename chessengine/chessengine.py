from math import e
from board import Board
from move import KingUnderAttack, Move

def check_king_under_attack(board: Board) -> bool:
    try:
        Move.find_all_moves(True, board)
    except KingUnderAttack as exception:
        return True
    return False


print("Would you like to play chess?")

board = Board()

board.starting_pos()

#board.print()
#all_moves = Move.find_all_moves(board)
#print(len(all_moves))
#board = all_moves[5].new_board
#board.print()

playing = True

while(playing):
    board.print()
    user_move_entry = input('Enter your move using coordinates, or QUIT to quit\n')
    if user_move_entry == 'QUIT':
        playing = False
    else:
        all_moves = Move.find_all_valid_moves(board)
        matching_moves = filter(lambda m: m.move_notation == user_move_entry, all_moves)
        user_move: Move = next(matching_moves, None)
        if isinstance(user_move, Move):
            board = user_move.new_board
        else:
            print('MOVE NOT FOUND')
            

    
        
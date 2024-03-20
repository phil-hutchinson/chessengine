from math import e
from board import Board
from ply import KingUnderAttack, Ply

def check_king_under_attack(board: Board) -> bool:
    try:
        Ply.find_all_moves(True, board)
    except KingUnderAttack as exception:
        return True
    return False


print("Would you like to play chess?")

board = Board()

board.starting_pos()

playing = True

while(playing):
    board.print()
    user_ply_entry = input('Enter your move using coordinates, or QUIT to quit\n')
    if user_ply_entry == 'QUIT':
        playing = False
    else:
        all_plies = Ply.find_all_valid_plies(board)
        matching_plies = filter(lambda p: p.move_notation == user_ply_entry, all_plies)
        user_ply: Ply = next(matching_plies, None)
        if isinstance(user_ply, Ply):
            board = user_ply.new_board
        else:
            print('MOVE NOT FOUND')
            

    
        
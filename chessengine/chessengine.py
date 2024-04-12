from game import Game, GameStatus, VictoryCondition


print("Would you like to play chess?")

game = Game(victory_condition=VictoryCondition.CHECKMATE)
# game = Game(victory_condition=VictoryCondition.TOTAL_CAPTURE)
# game = Game(victory_condition=VictoryCondition.PAWN_PROMOTION)

while game.status == GameStatus.ACTIVE:
    game.board.print()
    user_ply_entry = input('Enter your move using coordinates, or QUIT to quit\n')
    if user_ply_entry == 'QUIT':
        break
    else:
        is_valid = game.perform_ply(user_ply_entry)
        if not is_valid:
            print('MOVE NOT FOUND')
            
if game.status != GameStatus.ACTIVE:
    #game concluded, not aboarted
    game.board.print()

if game.status == GameStatus.WHITE_VICTORY:
    print("White Wins!")
elif game.status == GameStatus.BLACK_VICTORY:
    print("Black Wins!")
elif game.status == GameStatus.DRAW:
    print("it's a tie")
    
        
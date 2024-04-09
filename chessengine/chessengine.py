from game import Game, GameStatus


print("Would you like to play chess?")

game = Game()

while(game.status == GameStatus.ACTIVE):
    game.board.print()
    user_ply_entry = input('Enter your move using coordinates, or QUIT to quit\n')
    if user_ply_entry == 'QUIT':
        break
    else:
        is_valid = game.perform_ply(user_ply_entry)
        if not is_valid:
            print('MOVE NOT FOUND')
            

    
        
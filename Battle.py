import Ships
import DataAnalysis as da

if __name__ == "__main__":
    computer1 = Ships.Computer('Computer1','easy')
    computer2 = Ships.Computer('Computer2','master')
    computer1.place_ships()
    computer2.place_ships()
    computer1.copy_guess(computer2)
    computer2.copy_guess(computer1)
    turn_counter = 1
    while True:
        computer1.play(computer2)
        print("computer 1")
        computer1.print_board(computer1.guessing_map)
        print(computer1.guesses)
        computer2.play(computer1)
        print("computer 2")
        computer2.print_board(computer2.guessing_map)
        print(computer2.guesses)
        turn_counter += 1
        a = Ships.end_game(computer1, computer2)
        if a:
            break
    print("FINISHED GAME")
import random

def start_game():
    print("Welcome to the dice roller!")
    print("---------------------------")
    
    while True:
        choice = input("Press Enter to roll, or type 'q' to quit: ")
        
        if choice.lower() == "q":
            print("Thank you for playing!")
            break
        
        roll = random.randint(1, 6)
        print("You got:", roll)
        print()

start_game()
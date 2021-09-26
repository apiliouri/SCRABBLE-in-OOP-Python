import classes
from classes import *
'''
    Η main που περιλαμβάνει την δημιουργία του παιχνιδιού στο οποίο συμπεριλαμβάνονται 
    ολες οι υπόλοιπες κλασεις καθώς και ένα αρχικό μενού που παραπέμπει σε υπο-μενου
    των κλάσσεων με στοιχεία και διάφορες ρυθμίσεις.
    Το σενάριο που υλοποιήθηκε είνοι το Smart-Fail.
'''


def main():

    def start_menu():
        print("*" * 30)
        print("Αρχικό Μενού")
        print("1. Ιστορικό Παιχνιδιού - Σκόρ")
        print("2. Ρυθμίσεις - Παιχνιδιού")
        print("3. Ρυθμίσεις - Θέματα Λέξιλογίου")
        print("4. Νέο Παιχνίδι")
        print("5. Εμφάνιση docstring")
        print("q. Έξοδος")
        print("*" * 30)

    def guidelines():
        help(classes)

    print("Εκτέλεση Προγράμματος...")
    my_game = Game()

    # Το UI του παχνιδιού
    print("\n"*5)
    print("*" * 30 + "\n" + "*" * 10 + " Scrabble " + "*" * 10 + "\n" + "*" * 30 + "\n")
    print(f"Καλώς ήρθες, {my_game.player.name}\n")
    while True:
        start_menu()
        users_input = input("Εισάγετε επιλογή: ")
        while users_input not in ("1", "2", "3", "4", "5", "q"):
            users_input = input("Εισάγετε επιλογή: ")
        if users_input == "1":
            my_game.history.Game_stats_submenu()
        elif users_input == "2":
            my_game.setup()
        elif users_input == "3":
            my_game.words.Words_handle_sumbmenu()
        elif users_input == "4":
            my_game.run()
        elif users_input == "5":
            help(guidelines())
        else:
            print("\n*** Οριστικός Τερματισμός του παιχνιδιού ***")
            exit()


if __name__ == '__main__':
    main()

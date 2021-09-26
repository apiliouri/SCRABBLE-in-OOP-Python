# Τυχαιότητα
import random
# Διαχείριση αρχείου JSON
import json
# Πιθανοί συνδισμοί
import itertools as it
# Ημερομηνία και ώρα που πάιζεται το παιχνίδι
from datetime import datetime

"""
    Το σύνολο των κλάσσεων του παιχνιδιού:
    Game 
    SackClass 
    Player 
        Human 
        Computer 
    Words 
    GameStats    
"""


class Game:
    """
    Κλάση Game: Είναι η κλάση στην οποία λαμβάνει χώρα το παιχνίδι
    """

    def __init__(self):
        self.main_sak = SakClass().available_letters
        self.sak_players = SakClass()
        self.sak_players.randomize_sak()
        self.sak_pcs = SakClass()
        self.sak_pcs.randomize_sak()
        self.words = Words()
        self.words.add_words_from_txt("greek7.txt")
        self.words.create_the_game_words()
        self.history = GameStats()
        self.history.load_data("data.json")
        self.player = Human(input("Δώσε το όνομά σου: ").strip(), self.words.game_words)
        self.computer_player = Computer("Η/Υ", self.words.game_words)
        self.datetime = datetime.now()
        self.datetime = self.datetime.strftime("%d/%m/%Y %H:%M:%S")
        self.Round = 0

    def __repr__(self):
        return f"Datetime: {self.datetime}, Player: {self.player}, Computer as player: {self.computer_player}," \
               f"class history: {self.history}"

    @staticmethod
    def setup():
        """
        Απαραίτητες ενέργειες πριν το ξεκίνημα του παιχνιδιού - οπως είναι η ρύθμιση της
        δυσκολίας, στην προκειμένη περίπτωση εκτέλείται ένα και μόνο σεναριο το Smart - Fail
        """

        def game_setup_submenu():
            print("*" * 30)
            print("Ρυθμίσεις - Παιχνιδιού")
            print("1. Επιλογή Δυσκολίας")
            print("q. Πίσω στο Αρχικό Μενού")
            print("*" * 30)

        while True:
            game_setup_submenu()
            users_input = input("Εισάγετε επιλογή: ").strip()
            while users_input not in ("1", "q"):
                users_input = input("Εισάγετε επιλογή: ").strip()
            if users_input == "1":
                print("\nΗ Δυσκολία του παιχνίδιού ορίζεται στο σενάριο Smart-Fail")
                print("Η παρούσα επιλογή αφορά δομή προς μελλοντική επέκταση του παιχνιδιού\n")
            else:
                break

    def end(self):
        """
        Κάνει τις απαραίτητες ενέργειες για να κλείσει το παιχνίδι - δημιουργεί ένα αρχείο με τα στοιχεία
        του παιχνιδιού, κάνει εισαγωγή στην κλάσση GameStats και τα γράφει σε json αρχείο προκριμένου να
        είναι διάθέσιμα
        """
        if self.player.points > self.computer_player.points:
            print("\n" * 3)
            print("=" * 20 + "ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ")
            print("=" * 20 + f"Έχετε Νικήσει {self.player.points} vs {self.computer_player.points} τον Η/Υ!!")
            print("=" * 20 + f"Παίξατε συνολικά {self.Round} γύρους")
            print("=" * 20 + f"Ελπίζουμε να σας ξαναδούμε!!!")
            print("\n" * 2)
        elif self.player.points < self.computer_player.points:
            print("\n" * 3)
            print("=" * 20 + "ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ")
            print("=" * 20 + f"Δυστυχώς χάσατε {self.player.points} vs {self.computer_player.points} από τον Η/Υ")
            print("=" * 20 + f"Παίξατε συνολικά {self.Round} γύρους")
            print("=" * 20 + f"Ελπίζουμε να σας ξαναδούμε με μία καλύτερη προσπάθεια!!!")
            print("\n" * 2)
        else:
            print("\n" * 3)
            print("=" * 20 + "ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ")
            print("=" * 20 + f"Ισοπαλία!! {self.player.points} vs {self.computer_player.points} με τον Η/Υ")
            print("=" * 20 + f"Παίξατε συνολικά {self.Round} γύρους")
            print("=" * 20 + f"Ελπίζουμε να σας ξαναδούμε!!!")
            print("\n" * 2)

        self.history.insert_new_data_as_match_history(str(self.datetime), self.player.points,
                                                      self.computer_player.points, self.Round, self.Round,
                                                      self.player.points - self.computer_player.points)

        self.history.write_data_to_json_file("data.json")

        print("Έξοδος από το παιχνίδι...")
        exit()

    def run(self):
        """
        Η εξέλιξη του παιχνιδιού - Εδω τρέχει το παιχνίδι - μέθοδος που θα κληθεί από την Main
        Εισάγονται οι playes (Human - Computer) που ένουν κατασκευαστεί στην __init__()
        Εισάγονται στην μέθοδο play() αυτών ορίσματα όπως sak (σακουλάκι) και επιστρέφουν αποτέλεσμα
        την λέξη που βρέθηκε, "p" για πάσο και "q" για έξοδο.
        Εφόσον βρεθεί λέξη υπολογίζεται το σκορ ή σε άλλη περίπτωση κατά περίπωση συμβάινουν οι ανάλογες
        ενέργειες.
        Επίσης υπάρχει έλεγχος για το αν έχουν τελειώσει τα γράμματα στο κενρικό σακουλάκι προκειμένα να
        τερματίσει το παιχνίδι
        """

        print("\n\n\nTo παιχνίδι ξεκινά!!!!\n\n")
        self.Round = 1
        print("=" * 30)
        while True:
            print(f"Σειρά σου, είναι ο {self.Round}ος γύρος..")
            result = self.player.play(self.sak_players.sak)

            if result == "p":
                self.sak_players.update_sak()
            elif result == "q":
                # σοσ να δώσω λειτουργία
                self.end()
            else:
                self.sak_players.randomize_sak()

            if SakClass().if_letters_left() < 7:
                self.end()

            print("=" * 30)
            print(f"Σειρά του Η/Υ, στον {self.Round}ος γύρος..")
            result = self.computer_player.play(self.sak_pcs.sak)
            if result == "p":
                self.sak_pcs.update_sak()
            elif result == "q":
                self.end()
                break
            else:
                self.sak_pcs.randomize_sak()

            if SakClass().if_letters_left() < 7:
                self.end()

            self.Round += 1
            print("\n" * 2 + "=" * 40)
            print(
                f"Γύρος Νο.{self.Round} || {self.player.name}: {self.player.points} vs {self.computer_player.points} :"
                f"{self.computer_player.name}")
            print("=" * 40 + "\n" * 2)

        self.end()


class SakClass:
    """
        Η συγκεκριμένη κλάση περιλαμβάνει τα διαθέσιμα γράμματα με την αντίστοιχή τους βαθμολογία
        Το κεντρικό σακουλάκι με όλα τα γράμματα είναι χαρακτηριστικό της κλάσσης προκειμένου να έχουμε πρόσβαση
        σε αυτό πριν την κατασκευή αντικειμένου τύπου SakClass()
        Περιλαμβάνει επίσης μεθόδους χειρισμού τόσο του κύριου λεξικού με το συνολικό αριθμό γραμμάτων όσο
        των λεξικών στα χέρια των παικτών (υπολογισμός αξίας - ανανέωση - κτλ)
    """

    # Χαρακτηριστικό κλάσης - τα συνολικά γράμματα με πλήθος και την αξία - Hardcoded
    available_letters = {"Α": [12, 1], "Β": [1, 8], "Γ": [2, 4], "Δ": [2, 4], "Ε": [8, 1],
                         "Ζ": [1, 10], "Η": [7, 1], "Θ": [1, 10], "Ι": [8, 1], "Κ": [4, 2],
                         "Λ": [3, 3], "Μ": [3, 3], "Ν": [6, 1], "Ξ": [1, 10], "Ο": [9, 1],
                         "Π": [4, 2], "Ρ": [5, 2], "Σ": [7, 1], "Τ": [8, 1], "Υ": [4, 2],
                         "Φ": [1, 8], "Χ": [1, 8], "Ψ": [1, 10], "Ω": [3, 3]
                         }

    def __init__(self):
        self.sak = {}

    @staticmethod
    def if_letters_left():
        """
        :return: Τον αριθμό των γραμμάτων που έχουν μείνει μέσα στο σακουλάκι με το σύνολο τψν γραμμάτων
        """
        cnt = 0
        for element in SakClass.available_letters:
            if SakClass.available_letters[element][0] != 0:
                cnt += SakClass.available_letters[element][0]
        if cnt == 0:
            return 0
        else:
            return cnt

    def letters_in_hand_left(self):
        """
        :return: Αριθμό γραμμάτων στο χέρι του παίκτη
        """
        cnt = 0
        for letter in self.sak:
            if self.sak[letter][0] != 0:
                cnt += self.sak[letter][0]
        if cnt == 0:
            return 0
        else:
            return cnt

    def fill_sak_randomly(self, number_of_letters, a_sak):
        """
        :param number_of_letters: Αριθμό με το πόσα γράμματα θέλω να κάνω εισαγωγή
        :param a_sak: το λεξικό που θέλω να κάνω εισαγωγή τον αροθμό γραμμάτων
        :return: γεμισμα με τυχαιότητα το πάνω λεξικό και έλεγχος για το αν όντως είναι διαθέσιμα
        από το κεντρικό σακουλάκι προκειμένου να τα αφαιρέσω εκεί και να τα εισάγω στο "χέρι"
        """
        for _ in range(number_of_letters):
            a_random_letter = random.choice(list(SakClass.available_letters))
            while SakClass.available_letters[a_random_letter][0] == 0 and self.if_letters_left() is not None:
                a_random_letter = random.choice(list(SakClass.available_letters))
            if a_random_letter in a_sak:
                a_sak[a_random_letter][0] += 1
            else:
                a_sak[a_random_letter] = [1, SakClass.available_letters[a_random_letter][1]]
            SakClass.available_letters[a_random_letter][0] -= 1

    def randomize_sak(self):
        """
        :return: γεμίζει το λεξικό ("χέρι παίκτη") με όσα γράμματα λείπουν ώστε να έχει 7 - χρήση της
        παραπάνω μεθόδου fill_sak_randomly()
        """
        if len(self.sak) == 0:
            self.fill_sak_randomly(7, self.sak)
        else:
            self.fill_sak_randomly(7 - len(self.sak), self.sak)

    def put_back_letter(self, letter):
        """
        :param letter: γράμμα που επιθυμώ να επιστρέψω στο κενρτρικό σακουλάκι
        :return: πρόσθεση στο κεντρικό σακουλάκι (+= 1) το γράμμα που αφαιρώ από το χέρι μου και αντίστοιχη
        μείωση κατά ένα την ποσότητα απότο χέρι μου. Επειδή πρόκειται για λεξικό και το γράμμα αποτελει κλειδί
        δεν διαγράφεται - απαιτείται επιπλέον ενέργεια διαγαφής
        """
        if letter in self.sak and self.sak[letter][0] > 0:
            self.sak[letter][0] -= 1
            SakClass.available_letters[letter][0] += 1
        else:
            print(f"Το γράμμα {letter} δεν υπάρχει στο χέρι σου!")

    def get_letters(self):
        """
        :return: Επιστρέφει πλήθος γραμμάτων και συγκεκριμένα γράμματα (επιλογή πάικτη) από το χέρι του
        στο κεντρικό λεξικό με τα γράμματα και εισάγεται στο χέρι του ο ίδιος αριθμός με τυχαίο όμως τρόπο
        """
        if self.if_letters_left == 0:
            print("Δεν είναι διαθέσιμη αυτή η ενέργεια, διότι δεν υπάρχουν άλλα γράμματα στο σακουλάκι!")
            return None
        else:
            users_input = int(input("Πληκτρολόγησε τον αριθμό των γραμμάτων που θέλεις να πάρεις: "))
            while users_input > 7 - len(self.sak):
                users_input = int(input("Δεν μπορείς να έχεις στο χέρι πάνω από 7 γράμματα, δοκίμασε ξανά: "))
            for _ in range(users_input):
                a_random_letter = random.choice(list(SakClass.available_letters))
                while SakClass.available_letters[a_random_letter][0] == 0:
                    a_random_letter = random.choice(list(SakClass.available_letters))
                if a_random_letter in self.sak:
                    self.sak[a_random_letter][1] += 1
                else:
                    self.sak[a_random_letter] = [SakClass.available_letters[a_random_letter][0], 1]
                print(f"Πήρες: {a_random_letter}!")
                SakClass.available_letters[a_random_letter][0] -= 1

    def update_sak(self):
        """
        :return: Ανανεώνει το σακουλάκι του παίκτη - επιστροφή όλων των γραμμάτων στο κεντρικό και
        εισαγωγή άλλων επτά
        """
        new_sak = {}
        self.fill_sak_randomly(7, new_sak)
        letters_to_remove = []
        for letter in self.sak:
            for _ in range(self.sak[letter][0]):
                letters_to_remove.append(letter)
        for letter in letters_to_remove:
            SakClass.available_letters[letter][0] += 1
        self.sak.clear()
        self.sak = new_sak.copy()
        del new_sak, letters_to_remove


class Player:
    """
    Κλάση Player - μια γενική κλάση με τα χαρακτηριστικά και τις μεθόδους που χρειάζονται και περιέχουν τις
    ενέργειες με τον τροπο του παιχνιδιού.
    Κληρονομέι τις δύο παραγόμενες Human την οποία χειρίζεται ο παίκτης και την Computer στην οποία
    ενσωματώνεται ο αλγόριθμος Smart - Fail που προσομοιάζει την λογική και τον τρόπο παιχνιδιού ενός κανονικού
    ανθρώπου.
    """

    def __init__(self, name, words_dict):
        self.name = name
        self.words = Words()
        self.words_dict = words_dict
        self.points = 0

    def __repr__(self):
        return repr(f"Όνομα Παίκτη:{self.name}, Συλονικό Score:{self.points}, Μήκος Λεξικού: {len(self.words_dict)} "
                    f"και Θέση στην Μνήμη: {id(self.words_dict)}")

    def play(self, his_letters):
        """
        :param his_letters: Λεξικό, Το Σακουλάκι με τα επτά διαθέσιμα γράμματα από τα οποιά πρέπει να βρεί λέξη
        :return: "p" για πάσο, ως ανανέωση των γραμμάτων για να παίξει στον επόμενο γύρο, "q" για έξοδο και
        τερματισμό από το πρόγραμμα και τέλευταια η λέξη την οποία έχει εντοπίσει - ως αποδεικτικού ελέγχου
        """
        print(f"Τα διαθέσιμα γράμματα στο χέρι σας είναι: ")
        for letter in his_letters:
            if his_letters[letter][0] > 1:
                for _ in range(his_letters[letter][0]):
                    print(f"{letter}:{his_letters[letter][1]}", end=", ")
            else:
                print(f"{letter}:{his_letters[letter][1]}", end=", ")
        print("")
        print(f"Τα υπόλοιπα γράμματα στο σακουλακι είναι: {SakClass().if_letters_left()}")

        users_input = input("Εισάγετε μία λέξη που να σχηματίζεται από τα γράμματα του χεριού σας ή "
                            "'p' για πάσο και 'q' για έξοδο: ").strip()
        if users_input == "p":
            return "p"
        if users_input == "q":
            return "q"
        while True:
            if users_input not in Words().permutations_of_hand_letters(his_letters):
                print("Η εισαγόμενη λέξη δεν αποτελείται από τα γράμματα του χεριού σας,")
                users_input = input("Δοκιμάστε ξανά με άλλη λέξη ή 'p' για πάσο και 'q' για έξοδο: ").strip()
                if users_input == "p":
                    return users_input
                if users_input == "q":
                    return "q"
            elif users_input not in self.words_dict:
                print("Η εισαγόμενη λέξη είναι μη αποδεκτή,")
                users_input = input("Δοκιμάστε ξανά με άλλη λέξη ή 'p' για πάσο και 'q' για έξοδο: ").strip()
                if users_input == "p":
                    return users_input
                if users_input == "q":
                    return "q"
            else:
                self.points += self.words_dict[users_input]
                print(f"H λέξη του εισήγαγες είναι η {users_input}, Κέρδισες {self.words_dict[users_input]} πόντους!")
                print(f"H συνολική σου βαθμολογία είναι: {self.points} πόντοι!")
                for letter in users_input:
                    if his_letters[letter][0] > 1:
                        his_letters[letter][0] -= 1
                    else:
                        his_letters.pop(letter)
                return users_input


class Human(Player):
    """
    Η κλάση κληρονομεί τα πάντα από την πάνω και δεν χρειάζεται καμία τροποποίηση καθώς η λειτουργικότητα
    της Player την καλύπτει πλήρως
    """

    def __init__(self, name, words_dict):
        super().__init__(name, words_dict)


class Computer(Player):
    """
        Παραγόμενη κλάσση του player - η διαδικάσια και η λογική που παίζει ο υπολογιστής
    """

    def __init__(self, name, words_dict):
        super().__init__(name, words_dict)

    def smart_fail_algorithm(self, comp_letters, dif=4):
        """
        :param comp_letters: λεξικό με το "χέρι" του Η/Υ - διαθέσιμα γράμματα
        :param dif: Βαθμός δυσκολίας, πργαματικός αριθμός, όσο μειώνεται αυξάνεται η δυσκολία με βαθμό 1
         το μέγιστο της δυσκολίας- Η μεθοδος προσομοιώνει την σκέψη του ανθρώπου που μπορεί να βρει ή την
         καλύτερη λέξη σε πόντους ή κάποια λίγο χειρότερη. Οι κορυφαίες επιλογές κατατάσονται σε μία λίστα
         μήκους όσο και ο βαθμός δυσκολίας και επιλέται μία τυχαία λέξη από αυτές. Συνεπώς όσο μεγαλύτερη η
         λίστα τόσο ποιο πιθανή η επιλογή λέξης με λιγότερους πόντους
        :return: None εάν δεν έχει βρεί από τα διαθέσιμά γράμματα κάποιον πιθανό συνδιασμό ή την λέξη.
        """
        possible_words = Words().permutations_of_hand_letters(comp_letters)

        valid_words = []
        for word in possible_words:
            if word in self.words_dict:
                valid_words.append(word)
        del possible_words

        valid_words_including_score = {}

        for word in valid_words:
            valid_words_including_score[word] = self.words_dict[word]

        # only scores
        scores = [valid_words_including_score[x] for x in valid_words_including_score]
        scores.sort()

        choose_depend_difficulty = []

        for score in scores:
            if score in choose_depend_difficulty:
                continue
            else:
                choose_depend_difficulty.append(score)

        del scores

        top_scores = choose_depend_difficulty[0:dif]

        if len(top_scores) > 0:
            comp_choice = random.choice(top_scores)
        else:
            return None

        del top_scores

        for word in valid_words_including_score:
            if valid_words_including_score[word] == comp_choice:
                print(f"Η λέξη που παίζει ο υπολογιστής είναι {word} και έχει {comp_choice} πόντους!")
                return word
        return None

    # method override της κλάσσης Player
    def play(self, comp_letters):
        """
        :param comp_letters: Λεξικό, Το Σακουλάκι με τα επτά διαθέσιμα γράμματα από τα οποιά πρέπει να βρεί λέξη
        :return: "p" για πάσο, ως ανανέωση των γραμμάτων εφόσον δεν βρει λέξη ώστε να παίξει στον επόμενο γύρο
        και η λέξη την οποία έχει εντοπίσει - ως αποδεικτικό ελέγχου
        """
        print(f"Τα διαθέσιμα γράμματα του υπολογιστή είναι: ")
        for letter in comp_letters:
            if comp_letters[letter][0] > 1:
                for _ in range(comp_letters[letter][0]):
                    print(f"{letter}:{comp_letters[letter][1]}", end=", ")
            else:
                print(f"{letter}:{comp_letters[letter][1]}", end=", ")
        print("")
        print(f"Τα υπόλοιπα γράμματα στο σακουλακι είναι: {SakClass().if_letters_left()}")
        comp_input = self.smart_fail_algorithm(comp_letters)
        if comp_input is None:
            print("Ο Η/Υ πάει πάσο γιατί δεν εντόπισε κάποια λέξη!")
            return "p"

        else:
            self.points += self.words_dict[comp_input]
            print(f"H συνολική σου βαθμολογία του Η/Υ είναι: {self.points} πόντοι!")
            for letter in comp_input:
                if comp_letters[letter][0] > 1:
                    comp_letters[letter][0] -= 1
                else:
                    comp_letters.pop(letter)
            return comp_input


class Words:
    """
        Κλάση Words - δημιουργία λεξικού με το λεξιλόγιο του παιχνιδιού - μέθοδοι για εισαγωγή λέξεων
        από αρχείο, υπολογισμός αξίας της λέξης, εισαγωγή καινούριας λέξης και επανεγγραφή σε αρχέιο
        για μελλοντική χρήση
    """

    def __init__(self):
        self.word_list_from_file = []
        self.game_words = {}

    def add_words_from_txt(self, name_of_txt_file):
        """
        :param name_of_txt_file: το όνομα του .txt αρχείο που θέλουμε να ανοίξουμε για εισαγωγή λέξεων
        :return:Γέμισμα λίστας με τις λέξεις που είναι μεγαλύτερες από δύο λέξεις και μικρότερες ή ίσες από
        επτά γράμματα εναλακτικά τις διαγράφει
        """
        try:
            with open(name_of_txt_file, "r", encoding="utf-8") as f:
                for element_in_line in f:
                    self.word_list_from_file.append(element_in_line.strip("\n"))
        except FileNotFoundError:
            print(f"Το αρχείο με όνομα {name_of_txt_file} δεν βρέθηκε!")
        except:
            print(f"Κάτι δεν πήγε καλά με την εισαγωγή των δεδομένων από το αρχείο...")
        else:
            print(f"Επιτυχής εισαγωγή των λεξεων από το αρχείο {name_of_txt_file}...")

        # Έλεγχος και διαγραφή των λέξεων που έχουν λιγότερα από  2 και περισσότερα από 7 γράμματα
        element_to_delete = []
        print("Αφαίρεση λέξεων παυ είναι μικρότερες από 2 ή μεγαλύτερες από 7 γράμματα εφόσον υπάρχουν...")

        for element in self.word_list_from_file:
            if len(element) > 7 or len(element) <= 2:
                element_to_delete.append(element)

        for element in element_to_delete:
            print(f"Διαγραφή λέξης: {element}")
            self.word_list_from_file.remove(element)

        del element_to_delete

    def check_if_word_exists_in_list(self, new_word):
        """
        :param new_word: Λέξη που αναζητούμε στην Λίστα
        :return: True αν την υπάρχει και None εάν δεν υπάρχει
        """
        if new_word in self.word_list_from_file:
            return True
        else:
            return None

    def new_word_insert_in_game_words(self, new_word):
        """
        :param new_word:Λέξη που επιθυμούμε να εισάγουμε στην λίστα
        :return: True εάν δεν υπάρχει στην λίστα και έχει καταχωριθεί και None εάν υπαρχει ή δεν
        πληρεί τις προυποθέσεις
        """
        if self.check_if_word_exists_in_list(new_word) is True:
            print("\nΗ λέξη υπάρχει ήδη!\n")
            return None
        else:
            if 2 < len(new_word) <= 7:
                print(f"\nΗ λέξη {new_word} δεν υπάρχει στην λίστα και έχει καταχωριθεί!\n")
                self.word_list_from_file.append(new_word)
            else:
                print("\nΗ λέξη δεν καταχωρήθηκε επειδή έχει μη επιτρεπτό μέγεθος!\n")
            return True

    @staticmethod
    def permutations_of_hand_letters(sak):
        """
        :param sak: Τα γράμματα που διαθέτει ο παίκτης
        :return: Λίστα με πιθανούς συνδιασμούς - Πιθανές λέξεις
        """
        my_letters = []
        for letter in sak:
            if sak[letter][0] == 0:
                my_letters.append(letter)
            else:
                for _ in range(sak[letter][0]):
                    my_letters.append(letter)
        words = []
        for number_of_letters_per_word in range(3, 7 + 1):
            for i in it.permutations(my_letters, number_of_letters_per_word):
                word = ""
                for letter in i:
                    word += letter
                words.append(word)
        return words

    def words_that_are_in_game_words(self, permutations):
        """
        :param permutations: Λίστα με τους πιθανούς συνδιασμούς
        :return: Λεξικό στην μορφή {Λέξη:πόντοι λέξης}
        Λέξη: Συνδιασμοί που είναι λέξεις - υπαρχουν στην λίστα από το αρχείο που τους έχουμε εισάγει
        """
        words_in_hand = {}
        for word in permutations:
            if word in self.game_words:
                if word in words_in_hand:
                    continue
                else:
                    words_in_hand[word] = self.game_words[word]
        return words_in_hand

    @staticmethod
    def calculate_the_value_of_word(word):
        """
        :param word: Λέξη που θέλουμε να υπολογίσουμε την αξία της
        :return: Αξία της λέξης
        """
        value = 0
        for letter in word:
            value += SakClass.available_letters[letter][1]
        return value

    def create_the_game_words(self):
        """
        :return: Λεξικό της μορφής {Λέξη : Αξία Λέξης} από την λίστα των λέξεων.
        Με αυτόν τον τρόπο παρακάμπτουμε τη σειριακή αναζητηση της λίστας με αποτέλεσμα να μειώνεται
        ο χρόνος αναζήτησης και επιστρέφεται άμεσα η διαθέσιμη βαθμολογία για την επιλογή
        """
        for word in self.word_list_from_file:
            self.game_words[word] = self.calculate_the_value_of_word(word)

    def write_txt_to_file(self, name_of_file_to_write):
        """
        :param name_of_file_to_write: όνομα αρχείου που θέλω να γράψω το λεξιλόγιο των λέξεων εφόσον έχω
        εισάγει μία καινούρια λέξη με σκοπό να το τρέξω στο επόμενο άνοιγμα και να μην χαθεί η εισαγόμενη
        ή εισαγόμενες λέξεις
        :return: Γραμμένο - Ανανεωμένο αρχείο με τις ήδη υπάρχουσες αλλά και τις καινούριες λέξεις
        """
        with open(name_of_file_to_write, "w", encoding="utf-8") as f:
            for i in range(len(self.word_list_from_file)):
                f.write(self.word_list_from_file[i] + "\n")

    def Words_handle_sumbmenu(self):
        """
        :return: Εμφάνηση υπο-μενού και παραπομπή σε μεθόδους - λειτουργίες της κλάσσης
        """

        def words_handle_submenu():
            print("*" * 30)
            print("Ρυθμίσεις - Θέματα Λέξιλογίου")
            print("1. Αναζήτηση μιας λέξης εάν υπάρχει")
            print("2. Υπολογισμός πόντων μια λέξης")
            print("3. Εισαγωγή μιας καινούριας λέξης")
            print("4. Εμφάνιση Όλων των Λέξεων")
            print("q. Πίσω στο Αρχικό Μενού")
            print("*" * 30)

        while True:
            words_handle_submenu()
            users_input = input("Εισάγετε επιλογή: ").strip()
            while users_input not in ("1", "2", "3", "4", "q"):
                users_input = input("Εισάγετε επιλογή: ").strip()
            if users_input == "1":
                users_input = input(
                    "Παρακαλώ εισάγετε μία λέξη στα Ελληνικά χωρίς τόνους και κατά προτίμιση με κεφαλαίους "
                    "χαρακτήρες: ").strip().upper()
                if self.check_if_word_exists_in_list(users_input) is True:
                    print(f'\nΗ λέξη {users_input} υπάρχει ήδη στο σύστημα!\n')
                else:
                    print(f"\nΗ λέξη {users_input} δεν ήταν δυνατόν να εντοπιστεί\n")
            elif users_input == "2":
                print("Υπολογισμός πόντων μίας λέξης, ανεξάρτητα αν υπάρχει στο σύστημα ή όχι!")
                users_input = input(
                    "Εισάγετε μια λέξη στα Ελληνικά χωρίς τόνους και κατά προτίμηση με κεφαλαίους χαρακτήρες: ")\
                    .strip().upper()
                print(
                    f"\nΗ αξία της λέξης {users_input} είναι {self.calculate_the_value_of_word(users_input)} πόντοι!\n")
            elif users_input == "3":
                users_input = input(
                    "Εισάγετε μία καινούρια λέξη στο σύστημα με κεφαλαία, στα Ελληνικά , χωρίς τόνους: ").\
                    strip().upper()
                if self.new_word_insert_in_game_words(users_input) is True:
                    value = self.calculate_the_value_of_word(users_input)
                    self.game_words[users_input] = value
                    # εγραφή στο αρχείο greek7.txt ώστε να αποθηκεύονται για μελλοντική χρήση
                    self.write_txt_to_file("greek7.txt")
            elif users_input == "4":
                cnt = 1
                print("\n")
                for word in self.game_words:
                    print(f"{cnt}. Λέξη: {word} - Αξία: {self.game_words[word]} πόντοι")
                    cnt += 1
            else:
                break


class GameStats:
    """
    Κλάση που έχει ως δεδομένα στατιστικά στοιχέια προηγούμςνων παιχνιδιών - μέθοδοι διαχείρησης
    αρχείου json και επεξεργασίας δεδομένων
    """

    def __init__(self):
        self.data = {}

    def load_data(self, name_of_json_file):
        """
        :param name_of_json_file: Όνομα αρχείου JSON από όπου θέλουμς να εισάγουμε τα δεδομένα μας
        :return: Λέξικό - Δημιουργια τοης ιδιότητας με τα στατιστικά στοιχέια
        """
        try:
            with open(name_of_json_file, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print("Το αρχείο που πληλρολογίσατε δεν υπάρχει")
        except:
            print("Κάτι πήγε λάθος με το όνομα ή άνοιγμα ή την εγγραφή των δεδομένων από το αρχείο")
        else:
            print(f"Επιτυχής φόρτωση δεδομένων παλαιότερων παιχνιδιών από το αρχείο {name_of_json_file}...")

    def write_data_to_json_file(self, name_of_json_file):
        """
        :param name_of_json_file: Όνομα αρχείου JSON που θέλουμε να γράψουμε ωστε να διατηρήσουμε τα δεδομένα
        :return: Ανανεωμενο αρχείο JSON με τα ήδη υπάρχοντα και τα καινούρια δεδομένα
        """
        with open(name_of_json_file, "w") as file:
            json.dump(self.data, file)

    def insert_new_data_as_match_history(self, date, human_score, pc_score, human_round_played,
                                         pc_round_played, human_score_dif_pc_score):
        """
        :param date: datetime - ημερομηνία και ώρα παιχνιδιού σε μορφή str ως κλειδί λεξικού
        :param human_score: σκόρ παίκτη
        :param pc_score: σκόρ Η/Υ
        :param human_round_played: γύροι που παίχτηκαν από τον παίκτη
        :param pc_round_played: γύροι που παίχτηκαν από τον Η/Υ
        :param human_score_dif_pc_score: Διαφορά μεταξύ των δύο σκορ
        :return: Εισαγωγή λεξικού στην λίστα δεδομέων της μορφής
        {date: [human_score, pc_score, human_round_played, pc_round_played, human_score - pc score]}
        """
        self.data[date] = [human_score, pc_score, human_round_played, pc_round_played, human_score_dif_pc_score]

    def show_all_games(self):
        """
        :return: Εμφάνιση στην οθόνη το σύνολο των παιχνιδιών που έχουν παιχτεί
        """
        print(f"\nΙστορικό παιχνιδιών κατά ημερομηνία: ")
        cnt = 1
        for match in self.data:
            print(f"{cnt}. Date: {match}, Player: {self.data[match][0]} vs {self.data[match][1]} :Computer, "
                  f"Player's rounds: {self.data[match][2]} vs {self.data[match][3]} :Computer's rounds")
            cnt += 1
        print("\n")

    def a_number_of_best_games(self, number_of_games):
        """
        :param number_of_games: ακεραιο αριθμό με τα καλύτερα παιχνίδια που θέλουμε να αναζητήσουμε
        :return: εκτύπωση των καλύτερων του αριθμού εισαγωγής, παιχνιδιών ταξινομιμένων κατά το σκορ
        του πάικτη
        """
        top_players_score = []
        for elem in self.data:
            top_players_score.append(self.data[elem][0])
        top_players_score.sort()

        top_of_the_top_information = []
        for score in top_players_score:
            for key, value in self.data.items():
                if score == value[0]:
                    top_of_the_top_information.append(f"Date: {key}, Player: {self.data[key][0]} vs {self.data[key][1]}"
                                                      f":Computer, Player's rounds: {self.data[key][2]} vs "
                                                      f"{self.data[key][3]} :Computer's rounds")
        print(f"\nΤα {number_of_games} Καλύτερα παιχνίδια: ")
        if number_of_games >= len(top_of_the_top_information):
            for i in range(len(top_of_the_top_information)):
                print(f"{i + 1}. {top_of_the_top_information[i]}")
        else:
            for i in range(number_of_games):
                print(f"{i + 1}. {top_of_the_top_information[i]}")
        print("\n")

    def Game_stats_submenu(self):
        """
        :return: Υπομενού με κλήση των ανάλογων μεθόδων προς διαχέιριση - αναζήτησης δεδομένων
        """

        def game_stats_submenu():
            print("*" * 30)
            print("Ιστορικό Παιχνιδιού - Σκορ")
            print("1. Ιστορικό Παιχνιδίών κατά Ημερομηνία")
            print("2. Τα καλύτερα παιχνίδια")
            print("q. Πίσω στο Αρχικό Μενού")
            print("*" * 30)

        while True:
            game_stats_submenu()
            users_input = input("Εισάγετε επιλογή: ").strip()
            while users_input not in ("1", "2", "q"):
                users_input = input("Εισάγετε επιλογή: ").strip()
            if users_input == "1":
                self.show_all_games()
            elif users_input == "2":
                while True:
                    try:
                        users_input = int(input("Εισάγετε έναν αριθμό (π.χ. 10 ως τα 10 "
                                                "καλύετρα παιχνίδια που έχουν καταγραφεί): "))
                        break
                    except ValueError:
                        print("Παρακαλώ εισάγετε ακαίρεο αριθμό κορυφαίων παιχνιδιών!")
                self.a_number_of_best_games(users_input)
            else:
                break

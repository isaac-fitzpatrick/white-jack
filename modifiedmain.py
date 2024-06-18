import random
import time
import itertools
from random import randint

def read_value(filename):
    try:
        with open(filename, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
# sets function to read text files in designated file


def write_value(filename, guess_num):
    with open(filename, 'w') as file:
        file.write(str(guess_num))
# sets function to write back values to file


class Deck:
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def fill_deck(self):
        for i in range(0, 6):
            for suit, value in itertools.product(self.suits, self.values):
                self.cards.append(Card(suit, value))

    def clear_deck(self):
        self.cards = []

    def shuffle(self):
        random.shuffle(self.cards)


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

    @property
    def cardscore(self):
        if self.value in ["Jack", "Queen", "King"]:
            return 10
        if self.value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            return int(self.value)
        if self.value == "Ace":
            return 1


class Player:
    def __init__(self):
        self.hand = []

    def show_hand(self):
        print("\nPlayer's Hand:")
        for n, card in enumerate(self.hand):
            print(str(self.hand[n]))
        print()

    def reset(self):
        self.hand = []

    @property
    def ace_count(self):
        return len([c for c in self.hand if c.value == "Ace"])

    @property
    def handscore(self):
        return sum([c.cardscore for c in self.hand])

    @property
    def handscore_ace_adjusted(self):
        score = self.handscore
        for ace in range(self.ace_count):
            if score < 12:
                score += 10
        return score

    @property
    def isbusted(self):
        return self.handscore_ace_adjusted > 21

    @handscore.setter
    def handscore(self, value):
        self._handscore = value


class Human(Player):
    def __init__(self, chips):
        super().__init__()
        self.chips = chips
        self.split_hands = []  # To store split hands

    def place_bet(self, initial_bet=True):
        chance = random.randint(1, 10)
        if chance == 1:
            print("*you notice a sparkle in Genghis' eyes*")
            # rare pop-up to compel continuous plays (reference to actual slots machine)
        bet = input(f"\nYou have {self.chips} chips. \nHow much would you like to bet?: ")
        try:
            if int(bet) > self.chips:
                print("You don't have enough to bet that much!")
                return self.place_bet(initial_bet)
            else:
                self.chips -= int(bet)
                return int(bet)
        except ValueError:
            print("That is not a valid bet entry.")
            return self.place_bet(initial_bet)


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.hand = []

    def show_hand(self, showall=False):
        # Prints dealer's hand
        print("\nDealer's Hand:")
        if showall:
            for n, card in enumerate(self.hand):
                print(str(self.hand[n]))
        else:
            print(str(self.hand[0]))
            print("???")


class Game:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.playerbet = 0
        self.players_turn = True

    def deal(self, player, cards=2):
        for _ in range(cards):
            card = self.deck.cards.pop()
            player.hand.append(card)

    def hit(self, player):
        card = self.deck.cards.pop()
        player.hand.append(card)
        if isinstance(player, Dealer):
            player.show_hand(True)
        else:
            player.show_hand()
        self.checkbust(player)
        print(f"Handscore is {player.handscore_ace_adjusted}")

    def playerchoice(self, player):
        answer = input("Hit or Stick? H/S: ")
        if answer.lower() == "h":
            self.hit(player)
        elif answer.lower() == "s":
            print(f"Player Sticks with hand of {str(player.handscore_ace_adjusted)}\n")
            self.players_turn = False

    def checkbust(self, player):
        if player.isbusted:
            if isinstance(player, Human):
                print("Player Busts!")
                self.players_turn = False
                self.playerlose()
            if isinstance(player, Dealer):
                print("\nDealer Busts!")

    def playerwin(self, player):
        print(f"You win! \n{str(2 * self.playerbet)} chips added to your total.")
        player.chips += 2 * self.playerbet
        self.playerbet = 0

    def playerlose(self):
        print(f"You lose!")

    def draw(self, player):
        print(f"It's a draw, you get your bet of {self.playerbet} back.")
        player.chips += self.playerbet

    def comparescores(self, player, dealer):
        if player.handscore_ace_adjusted > dealer.handscore_ace_adjusted:
            self.playerwin(player)
        elif player.handscore_ace_adjusted == dealer.handscore_ace_adjusted:
            self.draw(player)
        else:
            self.playerlose()

    def resetplayers(self):
        for player in self.players:
            player.reset()
        self.playerbet = 0

    def playagain(self, player):
        again = None
        while again != "y" and again != "n":
            again = input("\nWould you like to play again? Y/N: ")
            chipvalues = player.chips
            if again.lower() == "y":
                return True
            elif again.lower() == "n":
                if player.chips <= 0:
                    write_value('chips.txt', 100)
                    print("\nYour chips have been reset to 100!")
                elif player.chips > 0:
                    print(f"\nYou walk away, you are left with {player.chips} chips.")
                    write_value('chips.txt', chipvalues)
                    input("Press any key to exit: ")
                    return False
                else:
                    print("That was not a valid input")

    def split_hand(self, player):
        split_card = player.hand.pop(1)
        deck1 = []
        deck2 = []
        deck1.append([split_card, self.deck.cards.pop()])
        deck2.append([split_card, self.deck.cards.pop()])
        player.split_hands.append([split_card, self.deck.cards.pop()])
        player.split_hands.append([split_card, self.deck.cards.pop()])

    def split_hand_deck1(self, player):
        split_card = player.hand.pop(1)
        deck1 = []
        player.deck1.append([split_card, self.deck.cards.pop()])
        return deck1

    def split_hand_deck2(self, player):
        split_card = player.hand.pop(1)
        deck2 = []
        player.deck2.append([split_card, self.deck.cards.pop()])
        return deck2


    def handle_splits(self, player):
        self.split_hand(player)
        split_bets = [self.playerbet] * 2
        hand_scores = []

        for idx, split_hand in enumerate(player.split_hands):
            print(f"\nPlaying hand {idx + 1}:")
            player.hand = split_hand
            player.show_hand()
            hit_count = 0  # Counter to track the number of hits for the current hand

            while not player.isbusted and self.players_turn:
                self.playerchoice(player)
                hit_count += 1
            if player.isbusted:
                print(f"Hand {idx + 1} busts!")
            player.handscore(split_hand)
            hand_score = player.handscore_ace_adjusted()
            hand_scores.append((hand_score, split_hand.copy(), hit_count))
            self.players_turn = True

        # Ensure we have two hand scores
        if len(hand_scores) < 2:
            print("Error: Not enough hand scores.")
            return

        # Compare scores of split hands
        scores = [hs[0] for hs in hand_scores]
        if scores[0] > scores[1]:
            winning_hand = hand_scores[0][1]
            losing_hand = hand_scores[1][1]
            winning_hand_hits = hand_scores[0][2]
            losing_hand_hits = hand_scores[1][2]
        elif scores[0] < scores[1]:
            winning_hand = hand_scores[1][1]
            losing_hand = hand_scores[0][1]
            winning_hand_hits = hand_scores[1][2]
            losing_hand_hits = hand_scores[0][2]
        else:
            winning_hand = hand_scores[0][1]
            losing_hand = None
            winning_hand_hits = hand_scores[0][2]
            losing_hand_hits = None

        # Only add the larger hand back to the main hand unless it's over 21
        player.hand = []
        if player.handscore_ace_adjusted(winning_hand) <= 21:
            player.hand = winning_hand
        elif losing_hand and player.handscore_ace_adjusted(losing_hand) <= 21:
            player.hand = losing_hand
        else:
            print("Both hands busted!")
        player.split_hands = []
        # Clear the split hands

    def play(self):
        print("\n---------- Welcome to Blackjack ----------\n")
        self.deck.fill_deck()
        self.deck.shuffle()
        chipvalue = read_value('chips.txt')
        player = Human(chipvalue)
        dealer = Dealer()
        self.players = [player, dealer]
        running = True

        while running:
            if self.players[0].chips == 0:
                print("You are flat broke! It's time to leave the table.")
                write_value('chips.txt', 100)
                input("Press any key to walk away in shame (Your chips have been reset to 100).")
                break
            self.playerbet = player.place_bet()
            self.deal(player)
            self.deal(dealer, 2)
            dealer.show_hand()
            player.show_hand()
            deez = False
            if player.hand[0].value == player.hand[1].value or (player.hand[0].value in ["Jack", "Queen", "King"] and player.hand[1].value in ["Jack", "Queen", "King"]):
                split_choice = input("You have two cards of the same value. Would you like to split? Y/N: ")
                while deez == False:
                    if split_choice.lower() == "y":
                        print("\nYou chose to split!")
                        self.handle_splits(player)
                        deez = True
                    elif split_choice.lower() == "n":
                        print("\nYou chose to keep your hand")
                        deez = True
                        self.playerchoice(player)
                    else:
                        print("Invalid entry. Please try again.")
            while self.players_turn:
                self.playerchoice(player)
            if not player.isbusted:
                dealer.show_hand(True)
                while not self.players_turn:
                    if dealer.handscore_ace_adjusted < 17:
                        time.sleep(1)
                        print("\nDealer Hits")
                        self.hit(dealer)
                        time.sleep(1)
                    if dealer.handscore_ace_adjusted >= 17 and not dealer.isbusted:
                        print(f"\nDealer Sticks with hand of {str(dealer.handscore_ace_adjusted)}\n")
                        break
                    if dealer.isbusted:
                        self.playerwin(player)
                        break
                if not dealer.isbusted:
                    self.comparescores(player, dealer)
            again = self.playagain(player)
            if not again:
                running = False
            self.players_turn = True
            self.resetplayers()


def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
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
    # sets possible card suits and values

    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def fill_deck(self):
        for i in range(0, 6):
            for suit, value in itertools.product(self.suits, self.values):
                self.cards.append(Card(suit, value))
        # generates 6 decks to choose cards from when dealing

    def clear_deck(self):
        self.cards = []
        # clears the deck

    def shuffle(self):
        random.shuffle(self.cards)
        # shuffles the deck


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
        # calculates a cards score


class Player:
    def __init__(self):
        self.hand = []

    def show_hand(self):
        print("\nPlayer's Hand:")
        for n, card in enumerate(self.hand):
            print(str(self.hand[n]))
        print()
        # prints player's hand

    def reset(self):
        self.hand = []
        # clears player's hand

    @property
    def ace_count(self):
        return len([c for c in self.hand if c.value == "Ace"])
        # returns number of aces

    @property
    def handscore(self):
        return sum([c.cardscore for c in self.hand])
        # calculates hand score from cards in hand

    @property
    def handscore_ace_adjusted(self):
        score = self.handscore
        for ace in range(self.ace_count):
            if score < 12:
                score += 10
        return score
        # changes value of the ace automatically

    @property
    def isbusted(self):
        return self.handscore_ace_adjusted > 21
        # tells the game if the player is busted

    @handscore.setter
    def handscore(self, value):
        self._handscore = value
        # sets callable value for player's handscore


class Human(Player):
    def __init__(self, chips):
        super().__init__()
        self.chips = chips

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
        # menu to select bet amount. makes sure that you have enough chips for the bet provided


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.hand = []

    def show_hand(self, showall=False):
        print("\nDealer's Hand:")
        if showall:
            for n, card in enumerate(self.hand):
                print(str(self.hand[n]))
        else:
            print(str(self.hand[0]))
            print("???")
        # prints dealer's hand (able to be shown fully or partially)

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
        # deals cards to the player

    def hit(self, player):
        card = self.deck.cards.pop()
        player.hand.append(card)
        if isinstance(player, Dealer):
            player.show_hand(True)
        else:
            player.show_hand()
        self.checkbust(player)
        print(f"Handscore is {player.handscore_ace_adjusted}")
        # adds a card to current player hand

    def playerchoice(self, player):
        answer = input("Hit or Stick? H/S: ")
        if answer.lower() == "h":
            self.hit(player)
        elif answer.lower() == "s":
            print(f"Player Sticks with hand of {str(player.handscore_ace_adjusted)}\n")
            self.players_turn = False
        # gives player the choice to hit (add a card) or to stick (keep current hand)

    def checkbust(self, player):
        if player.isbusted:
            if isinstance(player, Human):
                print("Player Busts!")
                self.players_turn = False
                self.playerlose()
            if isinstance(player, Dealer):
                print("\nDealer Busts!")
        # checks is player is busted and checks if dealer is busted

    def playerwin(self, player):
        print(f"You win! \n{str(2 * self.playerbet)} chips added to your total.")
        player.chips += 2 * self.playerbet
        self.playerbet = 0
        # win pop-up for if player wins

    def playerlose(self):
        print(f"You lose!")
        # lose pop-up for if player loses

    def draw(self, player):
        print(f"It's a draw, you get your bet of {self.playerbet} back.")
        player.chips += self.playerbet
        # pop-up in case of a draw

    def comparescores(self, player, dealer):
        if player.handscore_ace_adjusted > dealer.handscore_ace_adjusted:
            self.playerwin(player)
        elif player.handscore_ace_adjusted == dealer.handscore_ace_adjusted:
            self.draw(player)
        else:
            self.playerlose()
        # compares dealer's hand score to player's hand score

    def resetplayers(self):
        for player in self.players:
            player.reset()
        self.playerbet = 0
        # resets players

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
        # menu to play again or to walk away

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

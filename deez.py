deckone = self.split_hand_deck1(player)
        decktwo = self.split_hand_deck2(player)
        print("these are the split decks: ")
        for i in range(1, len(deckone)):
            print(f"{deckone[i]}")
        if deckone > 21:
            if decktwo > 21:
                print("Both player hands bust!")
            if deckone <= 21:
                player.handscore = decktwo
            else:
                print("An error has occurred please try again.")
                Game.play()
        elif decktwo > 21:
            if deckone > 21:
                print("Both player hands bust!")
            if deckone <= 21:
                player.handscore = deckone
            else:
                print("An error has occurred please try again.")
                Game.play()
        else:
            print("An error has occurred please try again.")

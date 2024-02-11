import sys

from base import DatabaseManager as dbm


class DrinkMenu:

    _drinkDB = dbm.session.query(dbm.DrinkDBEntry)
    _allDrinks = _drinkDB.all()

    """
    Simple key words that can help us understand what our user wants to do.
    """
    startOrderWords = [
        "start",
        "begin",
        "order"
    ]

    finishedOrderWords = [
        "done",
        "checkout",
        "ready",
        "finish",
    ]

    cancelActionWords = [
        "nevermind",
        "cancel",
        "back",
        "exit",
        "quit",
    ]

    browseTerms = [
        "info",
        "about",
        "get",
        "find",
    ]

    yesActionWords = [
        "yes",
        "yeah",
        "ye",
        "ya",
    ]

    noActionWords = [
        "no",
        "nope",
        "nah",
        "nty",
    ]

    def __init__(self):
        self.showDrinks()
        self.promptUser()

    def showDrinks(self):
        print("-" * 50)
        print("- - - Menu - - -")
        for d in self._allDrinks:
            print("{} | {} | ${:,.2f}".format(d.id, d.name, d.price))
        print("-" * 50)

    def findDrink(self, drink_lookup):
        if drink_lookup.isnumeric():
            return self._drinkDB.filter_by(id = int(drink_lookup)).first()
        else:
            return self._drinkDB.filter(dbm.DrinkDBEntry.name.ilike(drink_lookup)).first()

    def showDrinkInfo(self, drink_lookup):
        foundDrink = self.findDrink(drink_lookup)
        if not foundDrink:
            print("Bartender: Sorry! I couldn't find a drink with that name. Let's try it again...")
            return
        print(f"Bartender: Alright, here's what I got for ya:")
        print("ID: {} | Name: {} | Price: ${:,.2f} | Color: {} | Description: {}".format(
            foundDrink.id, foundDrink.name, foundDrink.price, foundDrink.color, foundDrink.description
        ))

    def beginOrder(self):
        currentOrder = []
        drinkPrompt = input(
            "Bartender: Great! Just tell me the name or the ID of the drinks and "
            "I'll see what I can do for ya.\n"
            "Bartender: When you're finished ordering, just tell me you're ready to"
            " checkout, or just say 'done'.\n"
            "Bartender: If you'd like to bounce out, just tell me to go back or say 'nevermind'. I understand."
            "\nYou: "
        ).lower()
        while not any(word in drinkPrompt for word in self.finishedOrderWords):
            # Any time they say one of the cancel words (and doesn't collide into a drink name), cancel it all.
            wantsToCancel = any(word in drinkPrompt for word in self.cancelActionWords)
            foundDrink = self.findDrink(drinkPrompt)

            if foundDrink:
                currentOrder.append(foundDrink)

            elif wantsToCancel:
                print("Bartender: OK, I'll cancel your order.")
                return
            else:
                print("Bartender: Couldn't find the drink for that one, sorry.")

            drinkPrompt = input("You: ")

        if not currentOrder:
            print("Bartender: Err, you didn't order anything, let's try this again...")
        else:
            print("Bartender: OK, let me get your order:")
        return currentOrder

    def promptUser(self):
        running = True
        while running:
            option = input(
                "Bartender: Would you like to start an order, or get information about a drink?\n"
                "You: "
            ).lower()

            if any(word in option for word in self.cancelActionWords):
                running = False
                break

            # Do they want to begin an order?
            if any(word in option for word in self.startOrderWords):
                ordering = True
                while ordering:
                    orderedDrinks = self.beginOrder()
                    if not orderedDrinks:
                        break

                    totalCost = 0.0
                    totalAmt = 0
                    for drinkOrder in sorted(orderedDrinks, key = lambda drinkOrder: drinkOrder.name):
                        print("Drink Name: {} | Price: ${:,.2f}".format(
                            drinkOrder.name, drinkOrder.price
                        ))
                        totalCost += float(drinkOrder.price)
                        totalAmt += 1
                    print(f"Bartender: With {totalAmt} drinks, that's going to be a total of ${totalCost:,.2f}.")
                    repeatPrompt = input("Bartender: Would you like to order again?\nYou: ")
                    # Another while loop, because our user can't give us a yes or a no...
                    while repeatPrompt:
                        if any(word in repeatPrompt for word in self.yesActionWords):
                            break
                        elif any(word in repeatPrompt for word in self.noActionWords):
                            print("Bartender: OK, goodbye!")
                            sys.exit()
                        else:
                            repeatPrompt = input("Bartender: I didn't quite get that, just give me a yes or no.\nYou: ")

            # Do they want to get information about a drink.?
            elif any(word in option for word in self.browseTerms):
                drinkPrompt = ""
                while drinkPrompt != "back":
                    drinkPrompt = input(
                        "Bartender: What drink would you like to look up? You can query by it's name or ID. "
                        "(To go back, type 'back'.)"
                        "\nYou: "
                    ).lower()
                    if drinkPrompt != "back":
                        self.showDrinkInfo(drinkPrompt)
                continue
            else:
                # We couldn't understand what they wanted
                print("Bartender: Sorry, I couldn't understand what you were looking for. Let's try again...")
                pass

        print("Bartender: OK, Goodbye pal.")


if __name__ == "__main__":
    di = DrinkMenu()

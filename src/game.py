from grid import Grid
from player import Player
import pickups


#Skapar spelplan, och placerar spelaren i mitten av spelplanet
g = Grid()
player = Player(g.width // 2, g.height // 2)
#Variabler som håller koll på spelarens poäng och inventory
score = 0
inventory = []
grace_steps = 0 #Graceperiod - kommer göra så att spelaren kan gå 5 steg utan förlora poäng

#Lägger till spelaren på kartan och väggar runt planen
g.set_player(player)
g.make_walls()
pickups.randomize(g)
items_left = len(pickups.pickups)

# Exit för spelet
while True:
    ex = g.get_random_x()
    ey = g.get_random_y()
    if g.is_empty(ex, ey):
        g.set(ex, ey, "E")
        break


# TODO: flytta denna till en annan fil
def print_status(game_grid):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {score} points.")
    print(game_grid)


command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    print_status(g)

    command = input("Use WASD to move, Q/X to quit. ")
    command = command.casefold()[:1]

    moves = {"w": (0, -1), "s": (0,1), "a": (-1,0), "d": (1,0)}

    if command in moves:
        dx, dy = moves[command]

        if player.can_move(dx, dy, g):
            maybe_item = g.get(player.pos_x + dx, player.pos_y + dy)

            player.move(dx, dy)
            if grace_steps > 0:
                grace_steps -= 1
            else:
                score -= 1


            if isinstance(maybe_item, pickups.Item):
                score += maybe_item.value
                inventory.append(maybe_item.name)
                grace_steps += 5
                print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
                g.clear(player.pos_x, player.pos_y)

    elif command == "i":
        print("Inventory:")
        if inventory:
            for item in inventory:
                print("-", item)


# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")

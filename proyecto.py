import time
import threading
import random

# Config
INITIAL_MONEY = 20
START_HOUR = 7
START_MINUTE = 0

# Game state
money = INITIAL_MONEY
has_gotten_up = False
is_ready_for_work = False
day = 1

# Clock state
total_time = 0
hour = int(total_time / 100)
minute = total_time - hour * 100


def clock():
    """Return formatted game time and advance one minute."""
    global total_time, hour, minute
    if hour > 23:
        hour = 0
        minute = 0
    total_time = hour * 100 + minute
    minute += 1
    if minute >= 60:
        minute = 0
        hour += 1
    return f"it is {hour:02d}:{minute:02d}"


def keep_clock_on():
    """Background clock that ticks every 5 seconds."""
    while True:
        clock()
        time.sleep(5)


def menu():
    """Main menu. Welcome shown once."""
    print("\nWelcome to")
    print(r" _____ _                ___      _           _ __ _")
    print(r"/__   \ |__   ___      / _ \_ __(_)_ __   __| / _(_)_ __ ___ ")
    print(r"  / /\/ '_ \ / _ \    / /_\/ '__| | '_ \ / _` \ \| | '_ ` _ \ ")
    print(r" / /  | | | |  __/   / /_\\| |  | | | | | (_| |\ \ | | | | | |")
    print(r" \/   |_| |_|\___|   \____/|_|  |_|_| |_|\__,_\__/_|_| |_| |_|")
    while True:
        try:
            choice = int(input("New Game(1)  Load Game(2)  Instructions(3) "))
        except ValueError:
            print("Invalid input")
            continue
        if choice == 1:
            print("loading game...")
            time.sleep(1)
            wake_up()
        elif choice == 3:
            print("You have to work, time never stops. Move fast, don't starve, manage money.")
        elif choice == 2:
            print("This option is not available yet.")
        else:
            print("That option does not exist.")


def wake_up():
    """Handle alarm choice and set initial time."""
    global total_time, hour, minute
    print("Your alarm rings... you look at the clock and it is 7 in the morning")
    time.sleep(1)
    while True:
        try:
            choice = int(input("wake up(1)  snooze(2) "))
        except ValueError:
            print("Invalid input")
            continue
        if choice == 1:
            print("You woke up on time")
            hour = START_HOUR
            minute = START_MINUTE
            total_time = hour * 100 + minute
            time.sleep(1)
            apartment()
            return
        elif choice == 2:
            print("You snooze your alarm 5 minutes")
            time.sleep(2)
            print("Now it is 07:30")
            hour = 7
            minute = 30
            total_time = 730
            time.sleep(1)
            apartment()
            return
        else:
            print("That option does not exist.")


def apartment():
    """Apartment interaction loop. Returns to caller on leave."""
    global has_gotten_up
    if not has_gotten_up:
        print("You get up from your bed and look around")
        has_gotten_up = True
    else:
        print("You return to the apartment center")
    time.sleep(1)
    while True:
        try:
            action = int(input("view money(1)  view time(2)  go to bathroom(3)  go to kitchen(4)  leave apartment(5) "))
        except ValueError:
            print("Invalid input")
            continue
        if action == 1:
            print(money)
        elif action == 2:
            print(clock())
        elif action == 3:
            bathroom()
        elif action == 4:
            kitchen()
        elif action == 5:
            street()
        else:
            print("That option does not exist.")


def bathroom():
    """Bathroom actions. Allows getting ready for work."""
    global is_ready_for_work
    print("\nYou are in the bathroom.")
    while True:
        try:
            choice = int(input("wash hands(1)  get ready for work(2)  leave(3) "))
        except ValueError:
            print("Invalid input")
            continue
        if choice == 1:
            print("You wash your hands.")
        elif choice == 2:
            if is_ready_for_work:
                print("You are already ready for work.")
            else:
                is_ready_for_work = True
                print("You change clothes and get ready for work.")
        elif choice == 3:
            print("You leave the bathroom.")
            return
        else:
            print("That option does not exist.")


def kitchen():
    """Kitchen placeholder."""
    print("\nKitchen is not implemented yet.")
    while True:
        try:
            inp = input("leave kitchen? y/n: ").lower().strip()
        except:
            continue
        if inp == "y":
            return
        elif inp == "n":
            print("You stay in the kitchen.")
        else:
            print("Invalid input")


def street():
    """Street actions. Bus costs money, walking requires minesweeper."""
    global money
    print("\nyou are out on the street")
    while True:
        try:
            choice = int(input("go back to apartment(1)  take the bus(2)  go to job walking(3) "))
        except ValueError:
            print("Invalid input")
            continue
        if choice == 1:
            return
        elif choice == 2:
            if money < 5:
                print("Not enough money for the bus.")
                continue
            confirm = input("Bus costs 5 money. Are you sure? y/n: ").lower().strip()
            if confirm == "y":
                money -= 5
                print(f"Bus paid. Money left: {money}")
                city()
            else:
                print("You stay on the street.")
            return
        elif choice == 3:
            print("You start walking. A small minefield blocks the path...")
            if minesweeper_mini():
                print("You made it to work on foot.")
                city()
            else:
                print("You turn back to the street.")
            return
        else:
            print("That option does not exist.")


def print_board(board, revealed, rows, cols):
    """Print the minesweeper board with fixed width columns."""
    header = "   " + " ".join(f"{c:2}" for c in range(cols))
    print("\n" + header)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            if not revealed[r][c]:
                row_cells.append(" ?")
            else:
                val = board[r][c]
                if val == -1:
                    row_cells.append(" *")
                else:
                    row_cells.append(f"{val:2}")
        print(f"{r:2} " + " ".join(row_cells))
    print()


def minesweeper_mini(rows=5, cols=5, mines=3):
    """Mini minesweeper. First click is safe and zero cells flood fill."""
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    revealed = [[False]*cols for _ in range(rows)]
    first_click = True
    safe_cells = rows*cols - mines
    found = 0

    print("\n--- Minesweeper Mini - Clear to get to work ---")
    print("Enter row col from 0-4")

    def place_mines(forbidden):
        b = [[0 for _ in range(cols)] for _ in range(rows)]
        placed = 0
        while placed < mines:
            r, c = random.randrange(rows), random.randrange(cols)
            if (r, c) == forbidden or b[r][c] == -1:
                continue
            b[r][c] = -1
            placed += 1
        return b

    while found < safe_cells:
        print_board(board, revealed, rows, cols)
        try:
            r = int(input("row: "))
            c = int(input("col: "))
        except ValueError:
            print("Invalid input")
            continue
        if not 0 <= r < rows or not 0 <= c < cols:
            print("Out of bounds")
            continue
        if revealed[r][c]:
            print("Already revealed")
            continue

        if first_click:
            first_click = False
            board = place_mines((r, c))
            for i in range(rows):
                for j in range(cols):
                    if board[i][j] == -1:
                        continue
                    cnt = 0
                    for dr in [-1,0,1]:
                        for dc in [-1,0,1]:
                            nr, nc = i+dr, j+dc
                            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == -1:
                                cnt += 1
                    board[i][j] = cnt

        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            if revealed[cr][cc]:
                continue
            revealed[cr][cc] = True
            if board[cr][cc] == -1:
                print_board(board, revealed, rows, cols)
                print("BOOM! You hit a mine.")
                return False
            if board[cr][cc] == 0:
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        nr, nc = cr+dr, cc+dc
                        if 0 <= nr < rows and 0 <= nc < cols and not revealed[nr][nc]:
                            stack.append((nr, nc))
            found += 1

        if found >= safe_cells:
            print_board(board, revealed, rows, cols)
            print("Cleared! You arrive at work safely.")
            return True

    print_board(board, revealed, rows, cols)
    print("Cleared!")
    return True


def city():
    """City placeholder. Pay depends on is_ready_for_work."""
    global money, is_ready_for_work
    print("\n--- CITY ---")
    print("city not implemented yet")


if __name__ == "__main__":
    clock_thread = threading.Thread(target=keep_clock_on, daemon=True)
    clock_thread.start()
    menu()
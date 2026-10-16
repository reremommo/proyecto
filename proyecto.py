import time
import threading
import random
#nota para la persona que califica eso, puedes recalificar la entrega 2 en la que pusieron 0 por adelantarme porfa
# ==================== CONFIG ====================
INITIAL_MONEY = 20
START_HOUR = 7
START_MINUTE = 0
FOOD_PRICE = 10
SOLAR_CAR_PRICE = 500
BASE_PAY = 50
STARVATION_DAYS = 3

# ==================== GAME STATE ====================
money = INITIAL_MONEY
has_gotten_up = False
is_ready_for_work = False
day = 1
days_until_starvation = STARVATION_DAYS
food_stock = 2
has_solar_car = False
inventory = ["llave"]

total_time = 0
hour = int(total_time / 100)
minute = total_time - hour * 100

# ==================== STRING HELPERS - AVANCE 8 ====================
def normalize_input(text: str) -> str:
    """Limpia y normaliza entrada del usuario."""
    return text.strip().lower()

def is_valid_choice(choice: str, valid: list) -> bool:
    """Valida que la elección esté en la lista permitida."""
    return normalize_input(choice) in [str(v).lower() for v in valid]

def format_money(amount: int) -> str:
    """Presentación formateada de dinero."""
    return f"${amount:,}".replace(",", ".")

def format_status() -> str:
    """Presentación del estado del jugador."""
    status = (
        f"Day {day} | Money: {format_money(money)} | "
        f"Days until starvation: {days_until_starvation} | "
        f"Ready: {'Yes' if is_ready_for_work else 'No'} | "
        f"Solar car: {'Yes' if has_solar_car else 'No'}"
    )
    return status

def search_inventory(query: str):
    """Búsqueda case-insensitive en inventario."""
    q = normalize_input(query)
    return [item for item in inventory if q in normalize_input(item)]

def parse_client(name: str):
    """Parsea nombre de cliente para el delivery game."""
    name = normalize_input(name)
    mapping = {"client a":1, "a":1, "1":1,
               "client b":2, "b":2, "2":2,
               "client c":3, "c":3, "3":3}
    return mapping.get(name)


# ==================== CLOCK ====================
def clock():
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
    global day, days_until_starvation, hour, minute
    while True:
        prev_hour, prev_minute = hour, minute
        clock()
        if prev_hour == 23 and prev_minute == 59 and hour == 0 and minute == 0:
            day += 1
            days_until_starvation -= 1
            print(f"\n--- Day {day} begins ---")
            if days_until_starvation <= 0:
                print("You haven't eaten for 3 days. You starve to death.")
                exit()
        time.sleep(5)


# ==================== MINESWEEPER ====================
def print_board(board, revealed, rows, cols):
    header = "   " + " ".join(f"{c:2}" for c in range(cols))
    print("\n" + header)
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            if not revealed[r][c]:
                row_cells.append(" ?")
            else:
                val = board[r][c]
                row_cells.append(" *") if val == -1 else f"{val:2}"
        print(f"{r:2} " + " ".join(row_cells))
    print()


def minesweeper_mini(rows=5, cols=5, mines=3):
    """Mini minesweeper. First click safe, zero flood fill."""
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



# ==================== TRAVEL HOME ====================
def return_home():
    global money
    if has_solar_car:
        print("You drive your solar car home for free.")
        return True
    print("Travel back home requires bus or walk.")
    while True:
        m_in = input("take bus 5 money(1)  walk minesweeper(2)  cancel(3): ")
        if not is_valid_choice(m_in, ["1","2","3"]):
            print("Invalid input")
            continue
        m = int(m_in)
        if m == 1:
            if money < 5:
                print("Not enough money.")
                return False
            money -= 5
            print(f"Bus paid. Money left: {format_money(money)}")
            return True
        elif m == 2:
            print("You start walking home. Minefield blocks the way...")
            return minesweeper_mini()
        elif m == 3:
            print("You stay where you are.")
            return False


# ==================== CITY ====================
def delivery_route_game():
    nodes = ["Office", "Client A", "Client B", "Depot"]
    dist = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(i+1,4):
            d = random.randint(5,20)
            dist[i][j] = dist[j][i] = d
    if is_ready_for_work:
        print("\nRoute map preview:")
        for i in range(4):
            row = " ".join(f"{dist[i][j]:2}" for j in range(4))
            print(f"{nodes[i]:9} {row}")
    print("\nYou must start at Office and end at Depot.")
    order = []
    for i in range(3):
        remaining = [c for c in [1,2,3] if c not in order]
        names = [nodes[c] for c in remaining]
        choice = input(f"Next stop {i+1} - pick from {names}: ")
        pick = parse_client(choice)
        if pick is None or pick not in remaining:
            print("Invalid choice, picking random.")
            pick = random.choice(remaining)
        order.append(pick)
    total = dist[0][order[0]]
    for i in range(len(order)-1):
        total += dist[order[i]][order[i+1]]
    total += dist[order[-1]][3]
    best = min(dist[0][a]+dist[a][b]+dist[b][c]+dist[c][3] for a in [1,2,3] for b in [1,2,3] for c in [1,2,3] if len({a,b,c})==3)
    print(f"\nYour route distance: {total}")
    print(f"Optimal distance: {best}")
    if total == best:
        return 1.2
    elif total <= best + 5:
        return 1.0
    else:
        return 0.8

def work():
    global money, is_ready_for_work
    print("\n--- WORK - Delivery Route ---")
    if has_solar_car:
        print("Solar car equipped: you have a GPS hint.")
    multiplier = delivery_route_game()
    base_mult = 1.0 if is_ready_for_work else 0.8
    final_mult = base_mult * multiplier
    pay = int(BASE_PAY * final_mult)
    money += pay
    print(f"You earned {format_money(pay)}. Money total: {format_money(money)}")

def shop():
    global money, food_stock, days_until_starvation
    while True:
        print(f"\nShop - Food: {FOOD_PRICE} money. You have {format_money(money)}")
        choice = input("buy(1)  leave(2): ").strip()
        if not is_valid_choice(choice, ["1","2"]):
            print("Invalid")
            continue
        if choice == "1":
            if money < FOOD_PRICE:
                print("Not enough money.")
                continue
            money -= FOOD_PRICE
            food_stock += 1
            days_until_starvation = STARVATION_DAYS
            print(f"Bought 1 food. Money left: {format_money(money)}")
        else:
            return

def car_dealership():
    global money, has_solar_car
    while True:
        print(f"\nCar Dealership - Solar Car: {SOLAR_CAR_PRICE} money. Owned: {has_solar_car}")
        choice = input("buy(1)  leave(2): ").strip()
        if not is_valid_choice(choice, ["1","2"]):
            print("Invalid")
            continue
        if choice == "1":
            if has_solar_car:
                print("You already own a solar car.")
            elif money < SOLAR_CAR_PRICE:
                print("Not enough money.")
            else:
                money -= SOLAR_CAR_PRICE
                has_solar_car = True
                print(f"Solar car bought! Money left: {format_money(money)}")
            return
        else:
            return

def city():
    print("\n--- CITY ---")
    while True:
        print(format_status())
        choice = input("work(1)  shop(2)  car dealership(3)  leave(4): ").strip()
        if not is_valid_choice(choice, ["1","2","3","4"]):
            print("Invalid input")
            continue
        if choice == "1":
            work()
        elif choice == "2":
            shop()
        elif choice == "3":
            car_dealership()
        elif choice == "4":
            if return_home():
                return


# ==================== MENU & APARTMENT ====================
def menu():
    print("\nWelcome to")
    print(r" _____ _                ___      _           _ __ _")
    print(r"/__   \ |__   ___      / _ \_ __(_)_ __   __| / _(_)_ __ ___ ")
    print(r"  / /\/ '_ \ / _ \    / /_\/ '__| | '_ \ / _` \ \| | '_ ` _ \ ")
    print(r" / /  | | | |  __/   / /_\\| |  | | | | | (_| |\ \ | | | | | |")
    print(r" \/   |_| |_|\___|   \____/|_|  |_|_| |_|\__,_\__/_|_| |_| |_|")
    while True:
        choice = input("New Game(1)  Load Game(2)  Instructions(3): ").strip()
        if not is_valid_choice(choice, ["1","2","3"]):
            print("Invalid input")
            continue
        if choice == "1":
            print("loading game...")
            time.sleep(1)
            wake_up()
        elif choice == "3":
            print("You have to work, time never stops. Move fast, don't starve, manage money.")
        else:
            print("This option is not available yet.")

def wake_up():
    global total_time, hour, minute
    print("Your alarm rings... you look at the clock and it is 7 in the morning")
    time.sleep(1)
    while True:
        choice = input("wake up(1)  snooze(2): ").strip()
        if not is_valid_choice(choice, ["1","2"]):
            print("Invalid input")
            continue
        if choice == "1":
            hour = START_HOUR; minute = START_MINUTE
            total_time = hour * 100 + minute
            time.sleep(1)
            apartment()
            return
        else:
            print("You snooze your alarm 5 minutes")
            time.sleep(2)
            hour = 7; minute = 30
            total_time = 730
            time.sleep(1)
            apartment()
            return

def apartment():
    global has_gotten_up
    if not has_gotten_up:
        print("You get up from your bed and look around")
        has_gotten_up = True
    else:
        print("You return to the apartment center")
    time.sleep(1)
    while True:
        action = input("view money(1)  view time(2)  go to bathroom(3)  go to kitchen(4)  leave apartment(5)  search inventory(6): ").strip()
        if not is_valid_choice(action, ["1","2","3","4","5","6"]):
            print("Invalid input")
            continue
        if action == "1":
            print(f"Money: {format_money(money)} | Food stock: {food_stock} | Days until starvation: {days_until_starvation}")
        elif action == "2":
            print(clock())
        elif action == "3":
            bathroom()
        elif action == "4":
            kitchen()
        elif action == "5":
            street()
        elif action == "6":
            q = input("Search inventory: ")
            res = search_inventory(q)
            print("Found:", res if res else "Nothing")

def bathroom():
    global is_ready_for_work
    print("\nYou are in the bathroom.")
    while True:
        choice = input("wash hands(1)  get ready for work(2)  leave(3): ").strip()
        if not is_valid_choice(choice, ["1","2","3"]):
            print("Invalid input")
            continue
        if choice == "1":
            print("You wash your hands.")
        elif choice == "2":
            if is_ready_for_work:
                print("You are already ready for work.")
            else:
                is_ready_for_work = True
                print("You change clothes and get ready for work.")
        else:
            print("You leave the bathroom.")
            return

def kitchen():
    global food_stock, days_until_starvation
    print(f"\nKitchen - Food stock: {food_stock} | Days until starvation: {days_until_starvation}")
    while True:
        choice = input("eat(1)  view stock(2)  leave(3): ").strip()
        if not is_valid_choice(choice, ["1","2","3"]):
            print("Invalid input")
            continue
        if choice == "1":
            if food_stock <= 0:
                print("No food left!")
            else:
                food_stock -= 1
                days_until_starvation = STARVATION_DAYS
                print(f"You eat. Food left: {food_stock}. Starvation reset.")
        elif choice == "2":
            print(f"Food stock: {food_stock}")
        else:
            return

def street():
    global money
    print("\nyou are out on the street")
    while True:
        choice = input("go back to apartment(1)  take the bus(2)  go to job walking(3): ").strip()
        if not is_valid_choice(choice, ["1","2","3"]):
            print("Invalid input")
            continue
        if choice == "1":
            if return_home():
                return
        elif choice == "2":
            if has_solar_car:
                print("You drive your solar car to work for free.")
                city()
                return
            if money < 5:
                print("Not enough money for the bus.")
                continue
            confirm = input("Bus costs 5 money. Are you sure? y/n: ").strip()
            if normalize_input(confirm) == "y":
                money -= 5
                print(f"Bus paid. Money left: {format_money(money)}")
                city()
            else:
                print("You stay on the street.")
            return
        else:
            if has_solar_car:
                print("You drive your solar car to work for free.")
                city()
                return
            print("You start walking. A small minefield blocks the path...")
            if minesweeper_mini():
                print("You made it to work on foot.")
                city()
            else:
                print("You turn back to the street.")
            return


if __name__ == "__main__":
    clock_thread = threading.Thread(target=keep_clock_on, daemon=True)
    clock_thread.start()
    menu()

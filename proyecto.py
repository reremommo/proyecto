import time
import threading
import random
import json
import os

# ==================== CONFIG ====================
INITIAL_MONEY = 20
START_HOUR = 7
START_MINUTE = 0
FOOD_PRICE = 10
SOLAR_CAR_PRICE = 500
BASE_PAY = 50
STARVATION_DAYS = 3
ENERGY_MAX = 100
SAVE_FILE = "savegame.json"

# ==================== GAME STATE ====================
money = INITIAL_MONEY
has_gotten_up = False
is_ready_for_work = False
day = 1
days_until_starvation = STARVATION_DAYS
food_stock = 2
has_solar_car = False
inventory = ["llave"]

energy = ENERGY_MAX
job_level = 1
job_xp = 0
weather = "sunny"

total_time = 0
hour = int(total_time / 100)
minute = total_time - hour * 100


# ==================== STRING HELPERS ====================
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
    """Presentación del estado completo del jugador."""
    return (
        f"Day {day} | Weather: {weather} | Money: {format_money(money)} | "
        f"Energy: {energy}/{ENERGY_MAX} | Days until starvation: {days_until_starvation} | "
        f"Job Lv.{job_level} XP {job_xp}/100"
    )

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


# ==================== SAVE / LOAD ====================
def save_game():
    """Guarda el estado del juego en JSON. Pide confirmación si el archivo existe."""
    global money, day, energy, food_stock, has_solar_car, job_level, job_xp, days_until_starvation, inventory, is_ready_for_work, has_gotten_up, weather
    if os.path.exists(SAVE_FILE):
        confirm = input(f"{SAVE_FILE} exists. Overwrite? y/n: ").strip().lower()
        if confirm != "y":
            print("Save cancelled.")
            return
    data = {
        "money": money,
        "day": day,
        "energy": energy,
        "food_stock": food_stock,
        "has_solar_car": has_solar_car,
        "job_level": job_level,
        "job_xp": job_xp,
        "days_until_starvation": days_until_starvation,
        "inventory": inventory,
        "is_ready_for_work": is_ready_for_work,
        "has_gotten_up": has_gotten_up,
        "weather": weather
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Game saved to {SAVE_FILE}")

def load_game():
    """Carga el estado del juego desde JSON."""
    global money, day, energy, food_stock, has_solar_car, job_level, job_xp, days_until_starvation, inventory, is_ready_for_work, has_gotten_up, weather
    if not os.path.exists(SAVE_FILE):
        print("No save file found.")
        return False
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    money = data.get("money", INITIAL_MONEY)
    day = data.get("day", 1)
    energy = data.get("energy", ENERGY_MAX)
    food_stock = data.get("food_stock", 2)
    has_solar_car = data.get("has_solar_car", False)
    job_level = data.get("job_level", 1)
    job_xp = data.get("job_xp", 0)
    days_until_starvation = data.get("days_until_starvation", STARVATION_DAYS)
    inventory = data.get("inventory", ["llave"])
    is_ready_for_work = data.get("is_ready_for_work", False)
    has_gotten_up = data.get("has_gotten_up", False)
    weather = data.get("weather", "sunny")
    print(f"Game loaded from {SAVE_FILE}")
    return True


# ==================== CLOCK ====================
def clock():
    """Advance one minute and return formatted time."""
    global total_time, hour, minute
    if hour > 23:
        hour = 0; minute = 0
    total_time = hour * 100 + minute
    minute += 1
    if minute >= 60:
        minute = 0; hour += 1
    return f"it is {hour:02d}:{minute:02d}"

def keep_clock_on():
    """Background clock. Day changes at midnight."""
    global day, days_until_starvation, hour, minute, weather
    while True:
        prev_hour, prev_minute = hour, minute
        clock()
        if prev_hour == 23 and prev_minute == 59 and hour == 0 and minute == 0:
            day += 1
            days_until_starvation -= 1
            weather = random.choice(["sunny","rain","storm"])
            print(f"\n--- Day {day} begins - Weather: {weather} ---")
            if days_until_starvation <= 0:
                print("You haven't eaten for 3 days. You starve to death.")
                exit()
        time.sleep(5)


# ==================== MINESWEEPER ====================
def print_board(board, revealed, rows, cols):
    """Print board with fixed width columns."""
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
    """Mini minesweeper for travel. First click safe, zero flood fill."""
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    revealed = [[False]*cols for _ in range(rows)]
    first_click = True
    safe_cells = rows*cols - mines
    found = 0
    print("\n--- Minesweeper Mini - Clear to get to work ---")
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
        r_in = input("row: "); c_in = input("col: ")
        if not is_valid_choice(r_in, [str(i) for i in range(rows)]) or not is_valid_choice(c_in, [str(i) for i in range(cols)]):
            print("Invalid input"); continue
        r, c = int(r_in), int(c_in)
        if revealed[r][c]:
            print("Already revealed"); continue
        if first_click:
            first_click = False
            board = place_mines((r, c))
            for i in range(rows):
                for j in range(cols):
                    if board[i][j] == -1: continue
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
            if revealed[cr][cc]: continue
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
    return True


# ==================== TRAVEL HOME ====================
def return_home():
    """Travel back to apartment. Free with solar car, else bus or minesweeper."""
    global money
    if has_solar_car:
        print("You drive your solar car home for free.")
        return True
    print("Travel back home requires bus or walk.")
    while True:
        m_in = input("take bus 5 money(1)  walk minesweeper(2)  cancel(3): ")
        if not is_valid_choice(m_in, ["1","2","3"]):
            print("Invalid input"); continue
        m = int(m_in)
        if m == 1:
            bus_cost = 5 + (2 if weather == "rain" else 5 if weather == "storm" else 0)
            if money < bus_cost:
                print("Not enough money."); return False
            money -= bus_cost
            print(f"Bus paid {bus_cost}. Money left: {format_money(money)}")
            return True
        elif m == 2:
            mines = 3 + (1 if weather == "rain" else 2 if weather == "storm" else 0)
            print("You start walking home. Minefield blocks the way...")
            return minesweeper_mini(rows=5, cols=5, mines=mines)
        else:
            print("You stay where you are."); return False


# ==================== CITY ====================
def delivery_route_game():
    """Delivery route mini-game."""
    nodes = ["Office", "Client A", "Client B", "Depot"]
    dist = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(i+1,4):
            d = random.randint(5,20)
            if weather == "rain": d += 3
            if weather == "storm": d += 7
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
    print(f"\nYour route distance: {total} | Optimal: {best}")
    if total == best: return 1.2
    elif total <= best + 5: return 1.0
    else: return 0.8

def work():
    """Job with delivery route. Pay depends on ready, energy and job level."""
    global money, is_ready_for_work, energy, job_level, job_xp
    print("\n--- WORK - Delivery Route ---")
    print("Disclaimer: soon a minigame for the job will be added.")
    if energy < 20:
        print("You are too tired to work well.")
    energy = max(0, energy - 30)
    multiplier = delivery_route_game()
    base_mult = 1.0 if is_ready_for_work else 0.8
    final_mult = base_mult * multiplier
    pay = int(BASE_PAY * job_level * final_mult)
    money += pay
    job_xp += int(20 * multiplier)
    print(f"You earned {format_money(pay)}. Money total: {format_money(money)}")
    if job_xp >= 100:
        job_level += 1
        job_xp = 0
        print(f"Job leveled up! Now Lv.{job_level}")
    print(f"Energy: {energy}/{ENERGY_MAX}")

def shop():
    """Buy food in city."""
    global money, food_stock, days_until_starvation
    while True:
        print(f"\nShop - Food: {FOOD_PRICE} money. You have {format_money(money)}")
        choice = input("buy(1)  leave(2): ").strip()
        if not is_valid_choice(choice, ["1","2"]):
            print("Invalid"); continue
        if choice == "1":
            if money < FOOD_PRICE:
                print("Not enough money."); continue
            money -= FOOD_PRICE
            food_stock += 1
            days_until_starvation = STARVATION_DAYS
            print(f"Bought 1 food. Money left: {format_money(money)}")
        else:
            return

def car_dealership():
    """Buy solar car."""
    global money, has_solar_car
    while True:
        print(f"\nCar Dealership - Solar Car: {SOLAR_CAR_PRICE} money. Owned: {has_solar_car}")
        choice = input("buy(1)  leave(2): ").strip()
        if not is_valid_choice(choice, ["1","2"]):
            print("Invalid"); continue
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
    """City hub."""
    print("\n--- CITY ---")
    while True:
        print(format_status())
        choice = input("work(1)  shop(2)  car dealership(3)  save(4)  leave(5): ").strip()
        if not is_valid_choice(choice, ["1","2","3","4","5"]):
            print("Invalid input"); continue
        if choice == "1":
            work()
        elif choice == "2":
            shop()
        elif choice == "3":
            car_dealership()
        elif choice == "4":
            save_game()
        elif choice == "5":
            if return_home():
                return


# ==================== MENU & APARTMENT ====================
def menu():
    """Main menu."""
    print("\nWelcome to")
    print(r" _____ _                ___      _           _ __ _")
    print(r"/__   \ |__   ___      / _ \_ __(_)_ __   __| / _(_)_ __ ___ ")
    print(r"  / /\/ '_ \ / _ \    / /_\/ '__| | '_ \ / _` \ \| | '_ ` _ \ ")
    print(r" / /  | | | |  __/   / /_\\| |  | | | | | (_| |\ \ | | | | | |")
    print(r" \/   |_| |_|\___|   \____/|_|  |_|_| |_|\__,_\__/_|_| |_| |_|")
    while True:
        choice = input("New Game(1)  Load Game(2)  Instructions(3): ").strip()
        if not is_valid_choice(choice, ["1","2","3"]):
            print("Invalid input"); continue
        if choice == "1":
            print("loading game..."); time.sleep(1); wake_up()
        elif choice == "2":
            if load_game():
                wake_up()
            else:
                print("Returning to menu.")
        else:
            print("You have to work, time never stops. Move fast, don't starve, manage money.")

def wake_up():
    """Handle alarm."""
    global total_time, hour, minute, energy
    print("Your alarm rings... you look at the clock and it is 7 in the morning")
    time.sleep(1)
    energy = min(ENERGY_MAX, energy + 50)
    while True:
        choice = input("wake up(1)  snooze(2): ").strip()
        if not is_valid_choice(choice, ["1","2"]):
            print("Invalid input"); continue
        if choice == "1":
            hour = START_HOUR; minute = START_MINUTE
            total_time = hour * 100 + minute
            time.sleep(1); apartment(); return
        else:
            print("You snooze your alarm 5 minutes"); time.sleep(2)
            hour = 7; minute = 30; total_time = 730
            time.sleep(1); apartment(); return

def apartment():
    """Apartment hub."""
    global has_gotten_up
    if not has_gotten_up:
        print("You get up from your bed and look around"); has_gotten_up = True
    else:
        print("You return to the apartment center")
    time.sleep(1)
    while True:
        action = input("view money(1)  view time(2)  go to bathroom(3)  go to kitchen(4)  leave apartment(5)  search inventory(6)  save(7): ").strip()
        if not is_valid_choice(action, ["1","2","3","4","5","6","7"]):
            print("Invalid input"); continue
        if action == "1":
            print(f"Money: {format_money(money)} | Food stock: {food_stock} | Energy: {energy}/{ENERGY_MAX}")
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
        elif action == "7":
            save_game()

def bathroom():
    """Bathroom."""
    global is_ready_for_work, energy
    print("\nYou are in the bathroom.")
    while True:
        choice = input("wash hands(1)  get ready for work(2)  leave(3): ").strip()
        if not is_valid_choice(choice, ["1","2","3"]):
            print("Invalid input"); continue
        if choice == "1":
            print("You wash your hands.")
        elif choice == "2":
            if is_ready_for_work:
                print("You are already ready for work.")
            else:
                is_ready_for_work = True
                energy = max(0, energy - 5)
                print("You change clothes and get ready for work.")
        else:
            print("You leave the bathroom."); return

def kitchen():
    """Kitchen."""
    global food_stock, days_until_starvation, energy
    print(f"\nKitchen - Food stock: {food_stock} | Days until starvation: {days_until_starvation}")
    while True:
        choice = input("eat(1)  view stock(2)  leave(3): ").strip()
        if not is_valid_choice(choice, ["1","2","3"]):
            print("Invalid input"); continue
        if choice == "1":
            if food_stock <= 0:
                print("No food left!")
            else:
                food_stock -= 1
                days_until_starvation = STARVATION_DAYS
                energy = min(ENERGY_MAX, energy + 30)
                print(f"You eat. Food left: {food_stock}. Energy +30")
        elif choice == "2":
            print(f"Food stock: {food_stock}")
        else:
            return

def street():
    """Street travel."""
    global money
    print("\nyou are out on the street")
    while True:
        choice = input("go back to apartment(1)  take the bus(2)  go to job walking(3): ").strip()
        if not is_valid_choice(choice, ["1","2","3"]):
            print("Invalid input"); continue
        if choice == "1":
            if return_home(): return
        elif choice == "2":
            if has_solar_car:
                print("You drive your solar car to work for free."); city(); return
            bus_cost = 5 + (2 if weather == "rain" else 5 if weather == "storm" else 0)
            if money < bus_cost:
                print("Not enough money for the bus."); continue
            confirm = input(f"Bus costs {bus_cost} money. Are you sure? y/n: ").strip()
            if normalize_input(confirm) == "y":
                money -= bus_cost
                print(f"Bus paid. Money left: {format_money(money)}"); city()
            else:
                print("You stay on the street.")
            return
        else:
            if has_solar_car:
                print("You drive your solar car to work for free."); city(); return
            print("You start walking. A small minefield blocks the path...")
            mines = 3 + (1 if weather == "rain" else 2 if weather == "storm" else 0)
            if minesweeper_mini(rows=5, cols=5, mines=mines):
                print("You made it to work on foot."); city()
            else:
                print("You turn back to the street.")
            return

if __name__ == "__main__":
    clock_thread = threading.Thread(target=keep_clock_on, daemon=True)
    clock_thread.start()
    menu()

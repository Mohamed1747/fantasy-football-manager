# Fantasy Football Game - CSAI 101 Project
# Made by: [Mohamed Hany 202500396- Ahmed khalil 202500453- 202511836 Abdelrahman Mohamed]
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
import random
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
# Global Variables
CURRENT_GAMEWEEK = 1
MAX_GAMEWEEKS = 10
TRANSFERS_PER_WEEK = 15
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Function 1 - loadPlayers
# Reads player data from text file and returns list of all players
# Input: fileName (String)
# Output: List of players (List)
def loadPlayers(fileName):
    marketList = []
    try:
        with open(fileName, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 4:
                        player = {
                            'name': parts[0].strip(),
                            'price': float(parts[1].strip()),
                            'position': parts[2].strip(),
                            'points': 0,
                            'gw_points': 0
                        }
                        marketList.append(player)
        print(f"Loaded {len(marketList)} players from market!")
        return marketList
    except FileNotFoundError:
        print(f"File {fileName} not found!")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Function 2 - displayMarket
# Displays all available players in the market in organized format
# Input: marketList (List)
# Output: None (prints to screen)
def displayMarket(marketList):
    if not marketList:
        print("\nMarket is empty!")
        return
    
    print("\n" + "="*90)
    print("                           PLAYER MARKET")
    print("="*90)
    print(f"{'#':<5} {'Name':<25} {'Price':<10} {'Position':<15} {'Total Pts':<12} {'GW Pts':<10}")
    print("-"*90)
    
    for i, player in enumerate(marketList, 1):
        print(f"{i:<5} {player['name']:<25} ${player['price']:<9.1f} {player['position']:<15} {player['points']:<12} {player['gw_points']:<10}")
    
    print("="*90)
    print(f"Total available players: {len(marketList)}")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Function 3 - searchPlayer
# Searches for a specific player by name in the list
# Input: name (String), list (List)
# Output: Player index (int) or -1 if not found
def searchPlayer(name, list):
    name = name.lower().strip()
    for i, player in enumerate(list):
        if name in player['name'].lower():
            return i
    return -1
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Function 4 - checkBudget
# Checks if you have enough money to buy the player
# Input: price (float), budget (float)
# Output: True if affordable, False otherwise
def checkBudget(price, budget):
    return budget >= price
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Function 5 - filterByPosition
# Displays only players in a specific position
# Input: position (String), list (List)
# Output: None (prints to screen)
def filterByPosition(pos, list):
    pos = pos.strip().lower()
    filtered = [p for p in list if p['position'].lower() == pos]
    
    if not filtered:
        print(f"\nNo players found in position: {pos}")
        return
    
    print("\n" + "="*90)
    print(f"                    Players in position: {pos.upper()}")
    print("="*90)
    print(f"{'#':<5} {'Name':<25} {'Price':<10} {'Total Pts':<12} {'GW Pts':<10}")
    print("-"*90)
    
    for i, player in enumerate(filtered, 1):
        print(f"{i:<5} {player['name']:<25} ${player['price']:<9.1f} {player['points']:<12} {player['gw_points']:<10}")
    
    print("="*90)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Function 6 - buyPlayer
# Buys a player, adds to your team, and deducts price from budget
# Input: myTeam (List), player (Dictionary), budget (float), transfers_left (int)
# Output: Success (True/False), new budget (float), message (String), transfers_left (int)
def buyPlayer(myTeam, player, budget, transfers_left):
    if not checkTeamLimit(myTeam):
        return False, budget, "Team has reached maximum limit (15 players)!", transfers_left
    
    if any(p['name'] == player['name'] for p in myTeam):
        return False, budget, "Player already in your team!", transfers_left
    
    if not checkBudget(player['price'], budget):
        return False, budget, f"Insufficient budget! Need ${player['price']:.1f}, you have ${budget:.1f}", transfers_left
    
    if transfers_left <= 0:
        return False, budget, "No transfers remaining this gameweek!", transfers_left
    
    myTeam.append(player.copy())
    new_budget = budget - player['price']
    transfers_left -= 1
    return True, new_budget, f"Successfully bought {player['name']}!", transfers_left
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Function 7 - sellPlayer
# Sells a player from your team and refunds their price
# Input: myTeam (List), index (int)
# Output: Refunded amount (float)
def sellPlayer(myTeam, index):
    if 0 <= index < len(myTeam):
        player = myTeam.pop(index)
        print(f"Sold {player['name']} and refunded ${player['price']:.1f}")
        return player['price']
    else:
        print("Invalid player number!")
        return 0.0
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Function 8 - checkTeamLimit
# Checks if team hasn't reached 15 players limit
# Input: myTeam (List)
# Output: True if space available, False if full
def checkTeamLimit(myTeam):
    return len(myTeam) < 15
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Function 9 - calcTotalScore
# Calculates total points of all players in your team
# Input: myTeam (List)
# Output: Total score (int)
def calcTotalScore(myTeam):
    total = sum(player['points'] for player in myTeam)
    return total
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Function 10 - saveGame
# Saves your team and score to a text file
# Input: myTeam (List), budget (float), gameweek (int), fileName (String)
# Output: None (writes to file)
def saveGame(myTeam, budget, gameweek, starting11, captain_idx, fileName="saved_team.txt"):
    try:
        with open(fileName, 'w', encoding='utf-8') as file:
            file.write("="*70 + "\n")
            file.write("              MY FANTASY FOOTBALL TEAM\n")
            file.write("="*70 + "\n\n")
            
            file.write(f"Gameweek: {gameweek}\n")
            file.write(f"Remaining Budget: ${budget:.1f}\n")
            file.write(f"Number of Players: {len(myTeam)}/15\n")
            file.write(f"Total Score: {calcTotalScore(myTeam)}\n\n")
            
            file.write("-"*70 + "\n")
            file.write("STARTING 11:\n")
            file.write("-"*70 + "\n")
            file.write(f"{'Name':<25} {'Position':<15} {'Points':<10} {'GW Pts':<10}\n")
            file.write("-"*70 + "\n")
            
            for idx in starting11:
                player = myTeam[idx]
                captain_mark = " (C)" if idx == captain_idx else ""
                file.write(f"{player['name']:<25}{captain_mark:<15} {player['position']:<15} {player['points']:<10} {player['gw_points']:<10}\n")
            
            file.write("\n" + "-"*70 + "\n")
            file.write("BENCH:\n")
            file.write("-"*70 + "\n")
            
            for i, player in enumerate(myTeam):
                if i not in starting11:
                    file.write(f"{player['name']:<25} {player['position']:<15} {player['points']:<10} {player['gw_points']:<10}\n")
            
            file.write("="*70 + "\n")
        
        print(f"\nTeam saved to file: {fileName}")
    except Exception as e:
        print(f"Error saving file: {e}")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#  Function 11 - selectStarting11
# Allows user to select 11 players from their 15-player squad
# Input: myTeam (List)
# Output: List of indices for starting 11
def selectStarting11(myTeam):
    if len(myTeam) < 11:
        print(f"\nYou need at least 11 players! You have {len(myTeam)}")
        return []
    
    print("\n" + "="*70)
    print("                    SELECT YOUR STARTING 11")
    print("="*70)
    print("Formation rules:")
    print("- 1 Goalkeeper")
    print("- 3-5 Defenders")
    print("- 2-5 Midfielders")
    print("- 1-3 Strikers")
    print("="*70)
    
    displayMyTeam(myTeam, 0)
    
    starting11 = []
    positions_count = {'Goalkeeper': 0, 'Defender': 0, 'Midfielder': 0, 'Striker': 0}
    
    print("\nSelect 11 players (enter their numbers separated by spaces):")
    print("Example: 1 2 3 4 5 6 7 8 9 10 11")
    
    while True:
        try:
            choices = input("\nYour selection: ").strip().split()
            if len(choices) != 11:
                print(f"You must select exactly 11 players! You selected {len(choices)}")
                continue
            
            indices = [int(x) - 1 for x in choices]
            
            if any(i < 0 or i >= len(myTeam) for i in indices):
                print("Invalid player numbers!")
                continue
            
            if len(set(indices)) != 11:
                print("You selected duplicate players!")
                continue
            
            positions_count = {'Goalkeeper': 0, 'Defender': 0, 'Midfielder': 0, 'Striker': 0}
            for idx in indices:
                positions_count[myTeam[idx]['position']] += 1
            
            if positions_count['Goalkeeper'] != 1:
                print("You must have exactly 1 Goalkeeper!")
                continue
            if not (3 <= positions_count['Defender'] <= 5):
                print("You must have 3-5 Defenders!")
                continue
            if not (2 <= positions_count['Midfielder'] <= 5):
                print("You must have 2-5 Midfielders!")
                continue
            if not (1 <= positions_count['Striker'] <= 3):
                print("You must have 1-3 Strikers!")
                continue
            
            starting11 = indices
            print("\n✓ Starting 11 selected successfully!")
            print(f"Formation: {positions_count['Goalkeeper']}-{positions_count['Defender']}-{positions_count['Midfielder']}-{positions_count['Striker']}")
            break
            
        except ValueError:
            print("Please enter valid numbers!")
    
    return starting11
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Function 12 - selectCaptain
# Allows user to select a captain who gets double points
# Input: myTeam (List), starting11 (List)
# Output: Captain index (int)
def selectCaptain(myTeam, starting11):
    if not starting11:
        return -1
    
    print("\n" + "="*70)
    print("                    SELECT YOUR CAPTAIN")
    print("="*70)
    print("Captain gets DOUBLE points this gameweek!")
    print("="*70)
    
    for i, idx in enumerate(starting11, 1):
        player = myTeam[idx]
        print(f"{i}. {player['name']} ({player['position']}) - Total: {player['points']} pts")
    
    while True:
        try:
            choice = int(input("\nSelect captain number (from starting 11): ")) - 1
            if 0 <= choice < len(starting11):
                captain_idx = starting11[choice]
                print(f"\n✓ {myTeam[captain_idx]['name']} is now your captain!")
                return captain_idx
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a valid number!")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Function 13 - simulateGameweek
# Simulates a gameweek and generates random points for players
# Input: marketList (List)
# Output: None (updates player points)
def simulateGameweek(marketList):
    print("\n" + "="*70)
    print("                    SIMULATING GAMEWEEK...")
    print("="*70)
    
    for player in marketList:
        if player['position'] == 'Goalkeeper':
            gw_points = random.randint(0, 8)
        elif player['position'] == 'Defender':
            gw_points = random.randint(0, 10)
        elif player['position'] == 'Midfielder':
            gw_points = random.randint(0, 15)
        else:
            gw_points = random.randint(0, 20)
        
        player['gw_points'] = gw_points
        player['points'] += gw_points
    
    print("✓ Gameweek simulation complete!")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Function 14 - calculateGameweekScore
# Calculates points for starting 11 with captain bonus
# Input: myTeam (List), starting11 (List), captain_idx (int)
# Output: Total gameweek points (int)
def calculateGameweekScore(myTeam, starting11, captain_idx):
    total = 0
    for idx in starting11:
        points = myTeam[idx]['gw_points']
        if idx == captain_idx:
            points *= 2
        total += points
    return total


def displayMenu():
    print("\n" + "="*70)
    print("                       MAIN MENU")
    print("="*70)
    print(f"                    GAMEWEEK {CURRENT_GAMEWEEK}")
    print("="*70)
    print("1. Display Market (All Players)")
    print("2. Search for Player")
    print("3. Filter by Position")
    print("4. Buy Player")
    print("5. Sell Player")
    print("6. Display My Team (All 15)")
    print("7. Select Starting 11")
    print("8. Select Captain")
    print("9. Display Team Statistics")
    print("10. Simulate Gameweek")
    print("11. Save Game")
    print("12. Exit")
    print("="*70)


def displayMyTeam(myTeam, budget):
    print("\n" + "="*90)
    print("                           MY TEAM (15 PLAYERS)")
    print("="*90)
    print(f"Remaining Budget: ${budget:.1f}")
    print(f"Number of Players: {len(myTeam)}/15")
    print(f"Total Score: {calcTotalScore(myTeam)}")
    print("-"*90)
    
    if not myTeam:
        print("Your team is empty! Start buying players.")
    else:
        print(f"{'#':<5} {'Name':<25} {'Price':<10} {'Position':<15} {'Total Pts':<12} {'GW Pts':<10}")
        print("-"*90)
        for i, player in enumerate(myTeam, 1):
            print(f"{i:<5} {player['name']:<25} ${player['price']:<9.1f} {player['position']:<15} {player['points']:<12} {player['gw_points']:<10}")
    
    print("="*90)


def displayStarting11(myTeam, starting11, captain_idx):
    if not starting11:
        print("\nYou haven't selected your starting 11 yet!")
        return
    
    print("\n" + "="*90)
    print("                         MY STARTING 11")
    print("="*90)
    print(f"{'#':<5} {'Name':<25} {'Price':<10} {'Position':<15} {'Total Pts':<12} {'GW Pts':<10}")
    print("-"*90)
    
    for i, idx in enumerate(starting11, 1):
        player = myTeam[idx]
        captain_mark = " (C)" if idx == captain_idx else ""
        print(f"{i:<5} {player['name'] + captain_mark:<25} ${player['price']:<9.1f} {player['position']:<15} {player['points']:<12} {player['gw_points']:<10}")
    
    print("="*90)
    if captain_idx >= 0:
        print(f"Captain: {myTeam[captain_idx]['name']} (Gets double points!)")
    print("="*90)


def main():
    global CURRENT_GAMEWEEK
    
    print("\n🎉 Welcome to Fantasy Football Game! 🎉\n")
    
    marketList = loadPlayers("Players.txt")
    if not marketList:
        print("Warning: No players loaded. Make sure players.txt exists")
        return
    
    myTeam = []
    budget = 100.0
    starting11 = []
    captain_idx = -1
    transfers_left = TRANSFERS_PER_WEEK
    
    print(f"\nStarting Budget: ${budget:.1f}")
    print("Goal: Build a team of 15 players, select your best 11, and get the highest score!")
    print(f"You have {transfers_left} free transfer per gameweek")
    
    while True:
        displayMenu()
        choice = input("\nChoose an option: ").strip()
        
        if choice == '1':
            displayMarket(marketList)
        
        elif choice == '2':
            name = input("\nEnter player name to search: ")
            index = searchPlayer(name, marketList)
            if index != -1:
                player = marketList[index]
                print(f"\nPlayer found:")
                print(f"   Name: {player['name']}")
                print(f"   Price: ${player['price']:.1f}")
                print(f"   Position: {player['position']}")
                print(f"   Total Points: {player['points']}")
                print(f"   Gameweek Points: {player['gw_points']}")
            else:
                print(f"\nPlayer not found: {name}")
        
        elif choice == '3':
            print("\nAvailable positions: Goalkeeper, Defender, Midfielder, Striker")
            pos = input("Enter position: ")
            filterByPosition(pos, marketList)
        
        elif choice == '4':
            name = input("\nEnter player name to buy: ")
            index = searchPlayer(name, marketList)
            if index != -1:
                player = marketList[index]
                print(f"\nPlayer: {player['name']} - ${player['price']:.1f}")
                print(f"Transfers remaining: {transfers_left}")
                confirm = input("Do you want to buy? (y/n): ").lower()
                if confirm == 'y':
                    success, budget, message, transfers_left = buyPlayer(myTeam, player, budget, transfers_left)
                    print(f"\n{message}")
                    if success:
                        print(f"Remaining Budget: ${budget:.1f}")
                        print(f"Transfers left: {transfers_left}")
            else:
                print(f"\nPlayer not found: {name}")
        
        elif choice == '5':
            if not myTeam:
                print("\nYour team is empty!")
            else:
                displayMyTeam(myTeam, budget)
                try:
                    index = int(input("\nEnter player number to sell: ")) - 1
                    refund = sellPlayer(myTeam, index)
                    budget += refund
                    if refund > 0:
                        print(f"New Budget: ${budget:.1f}")
                        starting11 = []
                        captain_idx = -1
                        print("Note: Starting 11 and Captain selection reset!")
                except ValueError:
                    print("Please enter a valid number!")
        
        elif choice == '6':
            displayMyTeam(myTeam, budget)
        
        elif choice == '7':
            if len(myTeam) < 11:
                print(f"\nYou need at least 11 players! You have {len(myTeam)}")
            else:
                starting11 = selectStarting11(myTeam)
                captain_idx = -1
        
        elif choice == '8':
            if not starting11:
                print("\nPlease select your starting 11 first!")
            else:
                captain_idx = selectCaptain(myTeam, starting11)
        
        elif choice == '9':
            print("\n" + "="*70)
            print("                    TEAM STATISTICS")
            print("="*70)
            print(f"Gameweek: {CURRENT_GAMEWEEK}")
            print(f"Remaining Budget: ${budget:.1f}")
            print(f"Number of Players: {len(myTeam)}/15")
            print(f"Total Score: {calcTotalScore(myTeam)}")
            print(f"Transfers left this week: {transfers_left}")
            print("="*70)
            
            if starting11:
                displayStarting11(myTeam, starting11, captain_idx)
        
        elif choice == '10':
            if not starting11:
                print("\nPlease select your starting 11 first!")
            elif captain_idx == -1:
                print("\nPlease select your captain first!")
            else:
                print(f"\nSimulating Gameweek {CURRENT_GAMEWEEK}...")
                simulateGameweek(marketList)
                
                for i, player in enumerate(myTeam):
                    for market_player in marketList:
                        if player['name'] == market_player['name']:
                            myTeam[i]['gw_points'] = market_player['gw_points']
                            myTeam[i]['points'] = market_player['points']
                
                gw_score = calculateGameweekScore(myTeam, starting11, captain_idx)
                
                print("\n" + "="*70)
                print(f"            GAMEWEEK {CURRENT_GAMEWEEK} RESULTS")
                print("="*70)
                displayStarting11(myTeam, starting11, captain_idx)
                print(f"\nYour Gameweek Score: {gw_score} points")
                print(f"(Captain {myTeam[captain_idx]['name']} points were doubled!)")
                print("="*70)
                
                CURRENT_GAMEWEEK += 1
                transfers_left = TRANSFERS_PER_WEEK
                starting11 = []
                captain_idx = -1
                
                if CURRENT_GAMEWEEK > MAX_GAMEWEEKS:
                    print("\n🏆 SEASON COMPLETE! 🏆")
                    print(f"Final Score: {calcTotalScore(myTeam)} points")
                    saveGame(myTeam, budget, CURRENT_GAMEWEEK-1, [], -1)
                    break
                
                print(f"\nGameweek {CURRENT_GAMEWEEK} begins! You have {transfers_left} free transfer.")
        
        elif choice == '11':
            if starting11 and captain_idx >= 0:
                saveGame(myTeam, budget, CURRENT_GAMEWEEK, starting11, captain_idx)
            else:
                print("\nPlease select Starting 11 and Captain before saving!")
        
        elif choice == '12':
            print("\nThank you! Do you want to save the game before exiting?")
            save = input("(y/n): ").lower()
            if save == 'y' and starting11 and captain_idx >= 0:
                saveGame(myTeam, budget, CURRENT_GAMEWEEK, starting11, captain_idx)
            print("\nGoodbye!\n")
            break
        
        else:
            print("\nInvalid choice! Please try again.")


class FantasyFootballGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fantasy Football Manager")
        self.root.geometry("1240x780")
        self.root.minsize(1100, 700)
        self.root.configure(bg="#07111f")

        self.project_dir = Path(__file__).resolve().parent
        self.marketList = loadPlayers(str(self.project_dir / "Players.txt"))
        self.myTeam = []
        self.budget = 100.0
        self.gameweek = CURRENT_GAMEWEEK
        self.transfers_left = TRANSFERS_PER_WEEK
        self.starting11 = []
        self.captain_idx = -1
        self.active_position = "All"
        self.search_text = tk.StringVar()

        self.colors = {
            "bg": "#07111f",
            "panel": "#0f1b2d",
            "panel2": "#13243a",
            "line": "#23364f",
            "text": "#eef6ff",
            "muted": "#9fb2ca",
            "green": "#00e676",
            "pink": "#ff2e88",
            "gold": "#ffd166",
            "blue": "#37a2ff",
            "pitch": "#0b8f58",
            "pitch2": "#087247",
        }

        self.setup_style()
        self.build_layout()
        self.refresh_all()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Fantasy.Treeview",
            background="#0f1b2d",
            fieldbackground="#0f1b2d",
            foreground=self.colors["text"],
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Fantasy.Treeview.Heading",
            background="#182b45",
            foreground=self.colors["text"],
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Fantasy.Treeview",
            background=[("selected", self.colors["green"])],
            foreground=[("selected", "#07111f")],
        )

    def build_layout(self):
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        sidebar = tk.Frame(self.root, bg=self.colors["panel"], width=270)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        main = tk.Frame(self.root, bg=self.colors["bg"])
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(2, weight=1)

        tk.Label(
            sidebar,
            text="FANTASY\nFOOTBALL",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Segoe UI", 25, "bold"),
            justify="left",
        ).pack(anchor="w", padx=24, pady=(28, 6))
        tk.Label(
            sidebar,
            text="Build the squad. Pick the XI. Chase glory.",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            font=("Segoe UI", 10),
            wraplength=210,
            justify="left",
        ).pack(anchor="w", padx=24, pady=(0, 24))

        self.stat_labels = {}
        for key, title in [
            ("score", "Total Points"),
            ("players", "Squad"),
            ("budget", "Budget"),
            ("transfers", "Transfers"),
            ("gameweek", "Gameweek"),
        ]:
            card = tk.Frame(sidebar, bg=self.colors["panel2"], highlightthickness=1, highlightbackground=self.colors["line"])
            card.pack(fill="x", padx=18, pady=6)
            tk.Label(card, text=title.upper(), bg=self.colors["panel2"], fg=self.colors["muted"], font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=14, pady=(10, 0))
            self.stat_labels[key] = tk.Label(card, text="-", bg=self.colors["panel2"], fg=self.colors["text"], font=("Segoe UI", 18, "bold"))
            self.stat_labels[key].pack(anchor="w", padx=14, pady=(0, 10))

        button_box = tk.Frame(sidebar, bg=self.colors["panel"])
        button_box.pack(side="bottom", fill="x", padx=18, pady=20)
        self.primary_button(button_box, "Save Game", self.save_game, self.colors["gold"], "#07111f").pack(fill="x", pady=5)
        self.primary_button(button_box, "Simulate Gameweek", self.simulate_week, self.colors["pink"], "white").pack(fill="x", pady=5)

        header = tk.Frame(main, bg=self.colors["bg"])
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 10))
        header.grid_columnconfigure(0, weight=1)
        tk.Label(header, text="Manager Dashboard", bg=self.colors["bg"], fg=self.colors["text"], font=("Segoe UI", 25, "bold")).grid(row=0, column=0, sticky="w")
        tk.Label(header, text="Search, transfer, pick your starting XI, and run the season.", bg=self.colors["bg"], fg=self.colors["muted"], font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")

        controls = tk.Frame(main, bg=self.colors["bg"])
        controls.grid(row=1, column=0, sticky="ew", padx=24, pady=8)
        controls.grid_columnconfigure(0, weight=1)
        search = tk.Entry(controls, textvariable=self.search_text, bg="#101f33", fg=self.colors["text"], insertbackground=self.colors["text"], relief="flat", font=("Segoe UI", 12))
        search.grid(row=0, column=0, sticky="ew", ipady=10, padx=(0, 12))
        search.insert(0, "")
        search.bind("<KeyRelease>", lambda _event: self.refresh_market())

        position_bar = tk.Frame(controls, bg=self.colors["bg"])
        position_bar.grid(row=0, column=1, sticky="e")
        self.position_buttons = {}
        for pos in ["All", "Goalkeeper", "Defender", "Midfielder", "Striker"]:
            btn = tk.Button(position_bar, text=pos, command=lambda p=pos: self.set_position(p), relief="flat", bd=0, padx=12, pady=9, cursor="hand2", font=("Segoe UI", 9, "bold"))
            btn.pack(side="left", padx=3)
            self.position_buttons[pos] = btn

        content = tk.PanedWindow(main, orient="horizontal", sashwidth=8, bg=self.colors["bg"], bd=0)
        content.grid(row=2, column=0, sticky="nsew", padx=24, pady=(6, 24))

        market_panel = self.panel(content)
        squad_panel = self.panel(content)
        content.add(market_panel, minsize=520)
        content.add(squad_panel, minsize=420)

        self.build_market_panel(market_panel)
        self.build_squad_panel(squad_panel)

    def panel(self, parent):
        return tk.Frame(parent, bg=self.colors["panel"], highlightthickness=1, highlightbackground=self.colors["line"])

    def primary_button(self, parent, text, command, bg, fg):
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg, activebackground=bg, activeforeground=fg, relief="flat", bd=0, padx=14, pady=11, cursor="hand2", font=("Segoe UI", 10, "bold"))

    def build_market_panel(self, parent):
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        top = tk.Frame(parent, bg=self.colors["panel"])
        top.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))
        tk.Label(top, text="Player Market", bg=self.colors["panel"], fg=self.colors["text"], font=("Segoe UI", 16, "bold")).pack(side="left")
        self.primary_button(top, "Buy Selected", self.buy_selected, self.colors["green"], "#07111f").pack(side="right")

        columns = ("name", "price", "position", "points", "gw")
        self.market_tree = ttk.Treeview(parent, columns=columns, show="headings", style="Fantasy.Treeview")
        for col, text, width in [
            ("name", "NAME", 220),
            ("price", "PRICE", 80),
            ("position", "POSITION", 115),
            ("points", "TOTAL", 70),
            ("gw", "GW", 60),
        ]:
            self.market_tree.heading(col, text=text)
            self.market_tree.column(col, width=width, anchor="w")
        self.market_tree.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 10))
        self.market_tree.bind("<Double-1>", lambda _event: self.buy_selected())
        market_scroll = ttk.Scrollbar(parent, orient="vertical", command=self.market_tree.yview)
        market_scroll.grid(row=1, column=1, sticky="ns", pady=(0, 10))
        self.market_tree.configure(yscrollcommand=market_scroll.set)

    def build_squad_panel(self, parent):
        parent.grid_rowconfigure(2, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        top = tk.Frame(parent, bg=self.colors["panel"])
        top.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))
        tk.Label(top, text="Your Club", bg=self.colors["panel"], fg=self.colors["text"], font=("Segoe UI", 16, "bold")).pack(side="left")
        self.primary_button(top, "Sell", self.sell_selected, self.colors["pink"], "white").pack(side="right", padx=(8, 0))
        self.primary_button(top, "Captain", self.make_captain, self.colors["gold"], "#07111f").pack(side="right", padx=(8, 0))
        self.primary_button(top, "Start/Bench", self.toggle_starting, self.colors["blue"], "white").pack(side="right")

        self.pitch = tk.Canvas(parent, height=270, bg=self.colors["pitch"], highlightthickness=0)
        self.pitch.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.pitch.bind("<Configure>", lambda _event: self.draw_pitch())

        columns = ("name", "price", "position", "points", "gw", "status")
        self.team_tree = ttk.Treeview(parent, columns=columns, show="headings", style="Fantasy.Treeview")
        for col, text, width in [
            ("name", "NAME", 190),
            ("price", "PRICE", 70),
            ("position", "POS", 95),
            ("points", "PTS", 55),
            ("gw", "GW", 50),
            ("status", "STATUS", 90),
        ]:
            self.team_tree.heading(col, text=text)
            self.team_tree.column(col, width=width, anchor="w")
        self.team_tree.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 16))
        team_scroll = ttk.Scrollbar(parent, orient="vertical", command=self.team_tree.yview)
        team_scroll.grid(row=2, column=1, sticky="ns", pady=(0, 16))
        self.team_tree.configure(yscrollcommand=team_scroll.set)

    def set_position(self, pos):
        self.active_position = pos
        self.refresh_market()
        self.refresh_position_buttons()

    def refresh_all(self):
        self.refresh_stats()
        self.refresh_market()
        self.refresh_team()
        self.refresh_position_buttons()
        self.draw_pitch()

    def refresh_stats(self):
        self.stat_labels["score"].config(text=str(calcTotalScore(self.myTeam)))
        self.stat_labels["players"].config(text=f"{len(self.myTeam)}/15")
        self.stat_labels["budget"].config(text=f"${self.budget:.1f}m")
        self.stat_labels["transfers"].config(text=str(self.transfers_left))
        self.stat_labels["gameweek"].config(text=f"{self.gameweek}/{MAX_GAMEWEEKS}")

    def refresh_position_buttons(self):
        for pos, btn in self.position_buttons.items():
            active = pos == self.active_position
            btn.config(bg=self.colors["green"] if active else self.colors["panel2"], fg="#07111f" if active else self.colors["text"])

    def refresh_market(self):
        self.market_tree.delete(*self.market_tree.get_children())
        query = self.search_text.get().strip().lower()
        for idx, player in enumerate(self.marketList):
            if query and query not in player["name"].lower():
                continue
            if self.active_position != "All" and player["position"] != self.active_position:
                continue
            self.market_tree.insert("", "end", iid=str(idx), values=(player["name"], f"${player['price']:.1f}m", player["position"], player["points"], player["gw_points"]))

    def refresh_team(self):
        self.team_tree.delete(*self.team_tree.get_children())
        for idx, player in enumerate(self.myTeam):
            status = "Starting" if idx in self.starting11 else "Bench"
            if idx == self.captain_idx:
                status += " / C"
            self.team_tree.insert("", "end", iid=str(idx), values=(player["name"], f"${player['price']:.1f}m", player["position"], player["points"], player["gw_points"], status))

    def selected_market_player(self):
        selection = self.market_tree.selection()
        if not selection:
            messagebox.showwarning("No player selected", "Choose a player from the market first.")
            return None
        return self.marketList[int(selection[0])]

    def selected_team_index(self):
        selection = self.team_tree.selection()
        if not selection:
            messagebox.showwarning("No player selected", "Choose a player from your club first.")
            return None
        return int(selection[0])

    def buy_selected(self):
        player = self.selected_market_player()
        if player is None:
            return
        success, self.budget, msg, self.transfers_left = buyPlayer(self.myTeam, player, self.budget, self.transfers_left)
        if success:
            messagebox.showinfo("Transfer complete", msg)
            self.refresh_all()
        else:
            messagebox.showwarning("Transfer blocked", msg)

    def sell_selected(self):
        idx = self.selected_team_index()
        if idx is None:
            return
        player_name = self.myTeam[idx]["name"]
        if not messagebox.askyesno("Confirm sale", f"Sell {player_name}?"):
            return
        self.budget += sellPlayer(self.myTeam, idx)
        self.starting11 = []
        self.captain_idx = -1
        self.refresh_all()

    def toggle_starting(self):
        idx = self.selected_team_index()
        if idx is None:
            return
        if idx in self.starting11:
            self.starting11.remove(idx)
            if self.captain_idx == idx:
                self.captain_idx = -1
        else:
            if len(self.starting11) >= 11:
                messagebox.showwarning("Starting XI full", "You already selected 11 starters.")
                return
            self.starting11.append(idx)
        self.validate_starting(show_success=False)
        self.refresh_all()

    def make_captain(self):
        idx = self.selected_team_index()
        if idx is None:
            return
        if idx not in self.starting11:
            messagebox.showwarning("Captain must start", "Pick this player in the starting XI first.")
            return
        self.captain_idx = idx
        self.refresh_all()

    def formation_counts(self):
        counts = {"Goalkeeper": 0, "Defender": 0, "Midfielder": 0, "Striker": 0}
        for idx in self.starting11:
            counts[self.myTeam[idx]["position"]] += 1
        return counts

    def validate_starting(self, show_success=True):
        if len(self.starting11) != 11:
            return False
        counts = self.formation_counts()
        valid = (
            counts["Goalkeeper"] == 1
            and 3 <= counts["Defender"] <= 5
            and 2 <= counts["Midfielder"] <= 5
            and 1 <= counts["Striker"] <= 3
        )
        if not valid:
            messagebox.showwarning("Invalid formation", "Rules: 1 GK, 3-5 DEF, 2-5 MID, 1-3 STR.")
            return False
        if show_success:
            messagebox.showinfo("Formation ready", f"Formation: {counts['Goalkeeper']}-{counts['Defender']}-{counts['Midfielder']}-{counts['Striker']}")
        return True

    def draw_pitch(self):
        if not hasattr(self, "pitch"):
            return
        canvas = self.pitch
        canvas.delete("all")
        width = max(canvas.winfo_width(), 500)
        height = max(canvas.winfo_height(), 260)
        canvas.create_rectangle(0, 0, width, height, fill=self.colors["pitch"], outline="")
        for x in range(0, width, 90):
            canvas.create_rectangle(x, 0, x + 45, height, fill=self.colors["pitch2"], outline="")
        canvas.create_rectangle(18, 18, width - 18, height - 18, outline="white", width=2)
        canvas.create_line(width / 2, 18, width / 2, height - 18, fill="white", width=2)
        canvas.create_oval(width / 2 - 50, height / 2 - 50, width / 2 + 50, height / 2 + 50, outline="white", width=2)

        grouped = {"Goalkeeper": [], "Defender": [], "Midfielder": [], "Striker": []}
        for idx in self.starting11:
            grouped[self.myTeam[idx]["position"]].append(idx)
        rows = [("Goalkeeper", height - 42), ("Defender", height - 105), ("Midfielder", height - 170), ("Striker", 50)]
        for position, y in rows:
            players = grouped[position]
            if not players:
                continue
            gap = width / (len(players) + 1)
            for number, idx in enumerate(players, 1):
                x = gap * number
                player = self.myTeam[idx]
                fill = self.colors["gold"] if idx == self.captain_idx else self.colors["panel"]
                text_fill = "#07111f" if idx == self.captain_idx else "white"
                canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill=fill, outline="white", width=2)
                canvas.create_text(x, y - 2, text="C" if idx == self.captain_idx else player["position"][0], fill=text_fill, font=("Segoe UI", 13, "bold"))
                short_name = player["name"].split()[-1][:11]
                canvas.create_text(x, y + 36, text=short_name, fill="white", font=("Segoe UI", 9, "bold"))

        if not self.starting11:
            canvas.create_text(width / 2, height / 2, text="Pick starters from your club list", fill="white", font=("Segoe UI", 15, "bold"))

    def simulate_week(self):
        if not self.validate_starting(show_success=False):
            messagebox.showwarning("Team not ready", "Select a valid starting XI before simulating.")
            return
        if self.captain_idx == -1:
            messagebox.showwarning("Captain missing", "Choose a captain before simulating.")
            return

        simulateGameweek(self.marketList)
        for i, player in enumerate(self.myTeam):
            for market_player in self.marketList:
                if player["name"] == market_player["name"]:
                    self.myTeam[i]["gw_points"] = market_player["gw_points"]
                    self.myTeam[i]["points"] = market_player["points"]

        gw_score = calculateGameweekScore(self.myTeam, self.starting11, self.captain_idx)
        captain_name = self.myTeam[self.captain_idx]["name"]
        messagebox.showinfo("Gameweek result", f"Gameweek {self.gameweek} score: {gw_score} points\nCaptain bonus: {captain_name}")

        self.gameweek += 1
        self.transfers_left = TRANSFERS_PER_WEEK
        self.starting11 = []
        self.captain_idx = -1

        if self.gameweek > MAX_GAMEWEEKS:
            messagebox.showinfo("Season complete", f"Final score: {calcTotalScore(self.myTeam)} points")
            self.gameweek = MAX_GAMEWEEKS
        self.refresh_all()

    def save_game(self):
        if not self.validate_starting(show_success=False) or self.captain_idx == -1:
            messagebox.showwarning("Save blocked", "Select a valid starting XI and captain before saving.")
            return
        file_name = self.project_dir / "saved_team.txt"
        saveGame(self.myTeam, self.budget, self.gameweek, self.starting11, self.captain_idx, str(file_name))
        messagebox.showinfo("Saved", f"Team saved to:\n{file_name}")


def launch_gui():
    root = tk.Tk()
    FantasyFootballGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()

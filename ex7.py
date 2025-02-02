import csv

# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input.isdigit():  # Ensures only numeric input is accepted
            return int(user_input)
        print("Invalid input.")

def get_poke_dict_by_id(poke_id):
    for poke in HOENN_DATA:
        if poke["ID"] == poke_id:
            return poke.copy()
    print(f"ID {poke_id} not found in Honen data.")
    return None  # Ensure None is returned instead of printing extra messages

def get_poke_dict_by_name(name):
    name = name.strip().lower()
    for poke in HOENN_DATA:
        if poke["Name"].lower() == name:
            return poke.copy()
    print(f"Pokemon '{name.capitalize()}' not found in Hoenn data.")
    return None  # Ensure None is returned if name is not found

def display_pokemon_list(poke_list):
    if not poke_list:
        print("There are no Pokemons in this Pokedex that match the criteria.")
        return

    for poke in poke_list:
        print(f"ID: {poke['ID']}, Name: {poke['Name']}, Type: {poke['Type']}, "
              f"HP: {poke['HP']}, Attack: {poke['Attack']}, Can Evolve: {poke['Can Evolve']}")

########################
# 2) BST (By Owner Name)
########################
def create_pokedex():
    global ownerRoot  # The BST root

    # Get owner name
    owner_name = input("Owner name: ").strip()

    # Check if owner already exists in BST
    if find_owner_bst(ownerRoot, owner_name.lower()) is not None:
        print(f"Owner '{owner_name}' already exists. No new Pokedex created.")
        return

    # Ask for a starter Pokémon
    print("Choose your starter Pokemon:")
    print("1) Treecko")
    print("2) Torchic")
    print("3) Mudkip")

    starter_choice = read_int_safe("Your choice: ")

    # Map choice to Pokémon name & ID
    starter_pokemon = None
    if starter_choice == 1:
        starter_pokemon = get_poke_dict_by_name("Treecko")
    elif starter_choice == 2:
        starter_pokemon = get_poke_dict_by_name("Torchic")
    elif starter_choice == 3:
        starter_pokemon = get_poke_dict_by_name("Mudkip")
    else:
        print("Invalid choice. No Pokedex created.")
        return

    # Create a new BST node for the owner with the chosen starter
    new_owner_node = create_owner_node(owner_name, starter_pokemon)

    # Insert into the BST
    ownerRoot = insert_owner_bst(ownerRoot, new_owner_node)

    print(f"New Pokedex created for {owner_name} with starter {starter_pokemon['Name']}.")

def create_owner_node(owner_name, first_pokemon=None):
    return {
        "owner_lower": owner_name.lower(),  # Used for comparison
        "owner_original": owner_name,  # Preserving the original format for printing
        "pokedex": [first_pokemon] if first_pokemon else [],
        "left": None,
        "right": None
    }

def insert_owner_bst(root, new_node):
    if root is None:
        return new_node  # Tree is empty → New node becomes root

    if new_node["owner_lower"] < root["owner_lower"]:
        root["left"] = insert_owner_bst(root["left"], new_node)
    elif new_node["owner_lower"] > root["owner_lower"]:
        root["right"] = insert_owner_bst(root["right"], new_node)

    return root

def find_owner_bst(root, owner_name):
    if root is None:
        return None

    owner_name = owner_name.lower()  # Convert input to lowercase for comparison

    if owner_name < root["owner_lower"]:
        return find_owner_bst(root["left"], owner_name)
    elif owner_name > root["owner_lower"]:
        return find_owner_bst(root["right"], owner_name)
    else:
        return root  # Found the owner


def min_node(node):
    while node["left"] is not None:
        node = node["left"]
    return node


def delete_owner_bst(root, owner_name):
    if root is None:
        return None

    owner_name = owner_name.lower()  # Convert input to lowercase for searching

    if owner_name < root["owner_lower"]:
        root["left"] = delete_owner_bst(root["left"], owner_name)
    elif owner_name > root["owner_lower"]:
        root["right"] = delete_owner_bst(root["right"], owner_name)
    else:
        # Node found, apply BST deletion rules
        if root["left"] is None:
            return root["right"]
        elif root["right"] is None:
            return root["left"]
        else:
            successor = min_node(root["right"])
            root["owner_lower"] = successor["owner_lower"]
            root["owner_original"] = successor["owner_original"]
            root["pokedex"] = successor["pokedex"]
            root["right"] = delete_owner_bst(root["right"], successor["owner_lower"])

    return root

########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    if root is None:
        return

    queue = [root]

    while queue:
        current = queue.pop(0)
        print(f"Owner: {current['owner_original']}")  # Preserve original capitalization
        display_pokemon_list(current["pokedex"])

        if current["left"]:
            queue.append(current["left"])
        if current["right"]:
            queue.append(current["right"])

def pre_order(root):
    if root is None:
        return

    print(f"\nOwner: {root['owner_original']}")  # Preserve original capitalization
    display_pokemon_list(root["pokedex"])

    pre_order(root["left"])
    pre_order(root["right"])

def in_order(root):
    if root is None:
        return

    in_order(root["left"])
    print(f"\nOwner: {root['owner_original']}")  # Preserve original capitalization
    display_pokemon_list(root["pokedex"])
    in_order(root["right"])

def post_order(root):
    if root is None:
        return

    post_order(root["left"])
    post_order(root["right"])
    print(f"\nOwner: {root['owner_original']}")  # Preserve original capitalization
    display_pokemon_list(root["pokedex"])

########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    poke_id = read_int_safe("Enter Pokemon ID to add: ")
    pokemon = get_poke_dict_by_id(poke_id)  # This already prints if not found

    if pokemon is None:
        return

    # Check for duplicates
    if any(p["ID"] == poke_id for p in owner_node["pokedex"]):
        print("Pokemon already in the list. No changes made.\n")
        return

    # Add to the end of the list
    owner_node["pokedex"].append(pokemon)
    print(f"Pokemon {pokemon['Name']} (ID {pokemon['ID']}) added to {owner_node['owner_original']}'s Pokedex.\n")
def release_pokemon_by_name(owner_node):
    poke_name = input("Enter Pokemon Name to release: ").strip().lower()  # ✅ Convert input to lowercase

    for i, pokemon in enumerate(owner_node["pokedex"]):
        if pokemon["Name"].lower() == poke_name:  # ✅ Compare case-insensitively
            print(f"Releasing {pokemon['Name']} from {owner_node['owner_original']}.")
            del owner_node["pokedex"][i]
            return

    print(f"No Pokemon named '{poke_name}' in {owner_node['owner_original']}'s Pokedex.")  # ✅ Ensures lowercase input
def evolve_pokemon_by_name(owner_node):
    poke_name = input("Enter Pokemon Name to evolve: ").strip().lower()

    for i, poke in enumerate(owner_node["pokedex"]):
        if poke["Name"].lower() == poke_name:
            if poke["Can Evolve"] == "FALSE":
                print(f"{poke['Name']} cannot evolve further.")
                return

            evolved_pokemon = get_poke_dict_by_id(poke["ID"] + 1)

            if evolved_pokemon is None:
                print(f"{poke['Name']} has no further evolution.")
                return

            # Remove old Pokémon and add evolved Pokémon
            del owner_node["pokedex"][i]

            # If the evolved Pokémon is already present, release it immediately
            if any(p["ID"] == evolved_pokemon["ID"] for p in owner_node["pokedex"]):
                print(f"Pokemon evolved from {poke['Name']} (ID {poke['ID']}) to {evolved_pokemon['Name']} (ID {evolved_pokemon['ID']}).")
                print(f"{evolved_pokemon['Name']} was already present; releasing it immediately.")
            else:
                owner_node["pokedex"].append(evolved_pokemon)
                print(f"Pokemon evolved from {poke['Name']} (ID {poke['ID']}) to {evolved_pokemon['Name']} (ID {evolved_pokemon['ID']}).")
            return

    print(f"No Pokemon named '{poke_name}' in {owner_node['owner_original']}'s Pokedex.")

def delete_pokedex():
    global ownerRoot

    # Get owner name (case insensitive)
    owner_name = input("Enter owner to delete: ").strip()

    # Find the owner with the correct casing
    owner_node = find_owner_bst(ownerRoot, owner_name.lower())

    if owner_node is None:
        print(f"Owner '{owner_name}' not found.")
        return

    # Use the original name casing
    original_name = owner_node["owner_original"]

    # Delete the owner from BST
    ownerRoot = delete_owner_bst(ownerRoot, owner_name.lower())
    print(f"Deleting {original_name}'s entire Pokedex...\nPokedex deleted.")

########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    if root is None:
        return

    gather_all_owners(root["left"], arr)  # Visit left
    arr.append(root)  # Store owner
    gather_all_owners(root["right"], arr)  # Visit right


def sort_owners_by_num_pokemon():
    owners_list = []
    gather_all_owners(ownerRoot, owners_list)

    if not owners_list:
        print("No owners at all.")
        return

    # Sort first by Pokémon count, then by name (case-insensitive) using a simple bubble sort
    n = len(owners_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            owner1 = owners_list[j]
            owner2 = owners_list[j + 1]

            if len(owner1["pokedex"]) > len(owner2["pokedex"]) or (
                len(owner1["pokedex"]) == len(owner2["pokedex"]) and owner1["owner_lower"] > owner2["owner_lower"]
            ):
                owners_list[j], owners_list[j + 1] = owners_list[j + 1], owners_list[j]

    print("=== The Owners we have, sorted by number of Pokemons ===")
    for owner in owners_list:
        print(f"Owner: {owner['owner_original']} (has {len(owner['pokedex'])} Pokemon)\n")

#######################
# 6) Print All
#######################

def print_all_owners():
    print("1) BFS")
    print("2) Pre-Order")
    print("3) In-Order")
    print("4) Post-Order")

    choice = read_int_safe("Your choice: ")

    print()

    if choice == 1:
        bfs_traversal(ownerRoot)
    elif choice == 2:
        pre_order(ownerRoot)
    elif choice == 3:
        in_order(ownerRoot)
    elif choice == 4:
        post_order(ownerRoot)

def pre_order_print(node):
    if node is None:
        return

    # Print owner and their Pokemon
    print(f"\nOwner: {node['owner'].capitalize()}\n")
    if node["pokedex"]:
        display_pokemon_list(node["pokedex"])
    else:
        print("There are no Pokemons in this Pokedex that match the criteria.")

    # Recurse left and right
    pre_order_print(node["left"])
    pre_order_print(node["right"])

def in_order_print(node):
    if node is None:
        return

    in_order_print(node["left"])

    # Print owner and their Pokémon
    print(f"\nOwner: {node['owner'].capitalize()}\n")
    if node["pokedex"]:
        display_pokemon_list(node["pokedex"])
    else:
        print("There are no Pokemons in this Pokedex that match the criteria.")

    in_order_print(node["right"])

def post_order_print(node):
    if node is None:
        return

    post_order_print(node["left"])
    post_order_print(node["right"])

    # Print owner and their Pokémon
    print(f"\nOwner: {node['owner'].capitalize()}\n")
    if node["pokedex"]:
        display_pokemon_list(node["pokedex"])
    else:
        print("There are no Pokemons in this Pokedex that match the criteria.")

########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    """ Display Pokémon based on filter criteria. """
    while True:
        print("\n-- Display Filter Menu --")
        print("1. Only a certain Type")
        print("2. Only Evolvable")
        print("3. Only Attack above __")
        print("4. Only HP above __")
        print("5. Only names starting with letter(s)")
        print("6. All of them!")
        print("7. Back")

        choice = read_int_safe("Your choice: ")

        if choice == 1:
            poke_type = input("Which Type? (e.g. GRASS, WATER): ").strip().lower()
            filtered = [p for p in owner_node["pokedex"] if p["Type"].lower() == poke_type]

        elif choice == 2:
            filtered = [p for p in owner_node["pokedex"] if p["Can Evolve"] == "TRUE"]

        elif choice == 3:
            while True:
                attack_threshold = input("Enter Attack threshold: ").strip()

                if attack_threshold.isdigit():
                    attack_threshold = int(attack_threshold)
                    break

                print("Invalid input.")
            filtered = [p for p in owner_node["pokedex"] if p["Attack"] > attack_threshold]

        elif choice == 4:
            while True:
                hp_threshold = input("Enter HP threshold: ").strip()

                if hp_threshold.isdigit():
                    hp_threshold = int(hp_threshold)
                    break

                print("Invalid input.")
            filtered = [p for p in owner_node["pokedex"] if p["HP"] > hp_threshold]

        elif choice == 5:
            prefix = input("Starting letter(s): ").strip().lower()
            filtered = [p for p in owner_node["pokedex"] if p["Name"].lower().startswith(prefix)]

        elif choice == 6:
            filtered = owner_node["pokedex"]  # Show all

        elif choice == 7:
            print("Back to Pokedex Menu.")
            return

        else:
            print("Invalid choice. Try again.")
            continue

        if filtered:
            display_pokemon_list(filtered)
        else:
            print("There are no Pokemons in this Pokedex that match the criteria.")

########################
# 8) Sub-menu & Main menu
########################
def format_owner_name(name):
    return " ".join([word.capitalize() for word in name.split()])


def pokedex_menu(owner_node):
    while True:
        print(f"\n-- {owner_node['owner_original']}'s Pokedex Menu --")
        print("1. Add Pokemon")
        print("2. Display Pokedex")
        print("3. Release Pokemon")
        print("4. Evolve Pokemon")
        print("5. Back to Main")

        while True:  # Keep asking until a valid integer is entered
            choice = input("Your choice: ").strip()

            try:
                choice = int(choice)  # ✅ Try converting input to an integer
                break  # ✅ If successful, break out of the loop
            except ValueError:
                print("Invalid input.")  # ✅ Only for non-numeric input (e.g., "abc", "$$")

        if choice < 0:  # ✅ Treat negative numbers as "Invalid choice."
            print("Invalid choice.")
        elif choice == 1:
            add_pokemon_to_owner(owner_node)
        elif choice == 2:
            display_filter_sub_menu(owner_node)
        elif choice == 3:
            release_pokemon_by_name(owner_node)
        elif choice == 4:
            evolve_pokemon_by_name(owner_node)
        elif choice == 5:
            print("Back to Main Menu.")  # ✅ Ensures correct message before returning
            return
        else:
            print("Invalid choice.")  # ✅ Handles numbers outside 1-5

def existing_pokedex():
    global ownerRoot

    # Get owner name
    owner_name = input("Owner name: ").strip().lower()

    # Search for the owner in BST
    owner_node = find_owner_bst(ownerRoot, owner_name)

    if owner_node is None:
        print(f"Owner '{owner_name}' not found.")
        return

    # Owner found - Show Pokedex menu
    pokedex_menu(owner_node)

def main_menu():
    # main menu func
    while True:
        print("\n=== Main Menu ===")
        print("1. New Pokedex")
        print("2. Existing Pokedex")
        print("3. Delete a Pokedex")
        print("4. Display owners by number of Pokemon")
        print("5. Print All")
        print("6. Exit")

        choice = read_int_safe("Your choice: ")

        if choice == 1:
             create_pokedex()
        elif choice == 2:
            existing_pokedex()
        elif choice == 3:
             delete_pokedex()
        elif choice == 4:
            sort_owners_by_num_pokemon()
        elif choice == 5:
            print_all_owners()
        elif choice == 6:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

def main():
    main_menu()

if __name__ == "__main__":
    main()

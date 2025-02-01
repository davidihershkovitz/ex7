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
        if user_input.isdigit():  # Ensure input contains only nums
            return int(user_input)
        print("Invalid input.")

def get_poke_dict_by_id(poke_id):
    for poke in HOENN_DATA:
        if poke["ID"] == poke_id:
            return poke.copy()
    return None  # Return None if ID is not found

def get_poke_dict_by_name(name):
    name = name.strip().lower()
    for poke in HOENN_DATA:
        if poke["Name"].lower() == name:
            return poke.copy()
    return None  # Return None if name is not found

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
    owner_name = input("Owner name: ").strip().lower()

    # Check if owner already exists in BST
    if find_owner_bst(ownerRoot, owner_name) is not None:
        print(f"Owner '{owner_name}' already exists. No new Pokedex created.")
        return

    # Ask for a starter Pokemon
    print("Choose your starter Pokémon:")
    print("1) Treecko")
    print("2) Torchic")
    print("3) Mudkip")

    starter_choice = read_int_safe("Your choice: ")

    # Map choice to Pokemon name & ID
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

    print(f"New Pokedex created for {owner_name.capitalize()} with starter {starter_pokemon['Name']}.")

def create_owner_node(owner_name, first_pokemon=None):
    return {
        "owner": owner_name,
        "pokedex": [first_pokemon] if first_pokemon else [],
        "left": None,
        "right": None
    }
def insert_owner_bst(root, new_node):
    if root is None:
        return new_node  # If tree is empty, new node is the root

    if new_node["owner"] < root["owner"]:
        root["left"] = insert_owner_bst(root["left"], new_node)
    elif new_node["owner"] > root["owner"]:
        root["right"] = insert_owner_bst(root["right"], new_node)

    return root  # Return the root (unchanged)

def find_owner_bst(root, owner_name):
    if root is None:
        return None

    if owner_name < root["owner"]:
        return find_owner_bst(root["left"], owner_name)
    elif owner_name > root["owner"]:
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

    # Navigate to the correct node
    if owner_name < root["owner"]:
        root["left"] = delete_owner_bst(root["left"], owner_name)
    elif owner_name > root["owner"]:
        root["right"] = delete_owner_bst(root["right"], owner_name)
    else:
        # Node found
        if root["left"] is None:  # Case 1: No left child
            return root["right"]
        elif root["right"] is None:  # Case 2: No right child
            return root["left"]
        else:
            # Case 3: Node has two children
            successor = min_node(root["right"])
            root["owner"] = successor["owner"]  # Replace with successor
            root["pokedex"] = successor["pokedex"]  # Copy Pokedex data
            root["right"] = delete_owner_bst(root["right"], successor["owner"])  # Delete successor

    return root

########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    if root is None:
        print("No owners to display.")
        return

    queue = [root]

    while queue:
        current = queue.pop(0)
        print(f"Owner: {current['owner'].capitalize()}, Number of Pokemon: {len(current['pokedex'])}")

        if current["left"]:
            queue.append(current["left"])
        if current["right"]:
            queue.append(current["right"])
def pre_order(root):
    if root is None:
        return

    print(f"Owner: {root['owner'].capitalize()}, Number of Pokemon: {len(root['pokedex'])}")
    pre_order(root["left"])
    pre_order(root["right"])

def in_order(root):
    if root is None:
        return

    in_order(root["left"])
    print(f"Owner: {root['owner'].capitalize()}, Number of Pokemon: {len(root['pokedex'])}")
    in_order(root["right"])

def post_order(root):
    if root is None:
        return

    post_order(root["left"])
    post_order(root["right"])
    print(f"Owner: {root['owner'].capitalize()}, Number of Pokemon: {len(root['pokedex'])}")


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    poke_id = read_int_safe("Enter Pokemon ID to add: ")
    pokemon = get_poke_dict_by_id(poke_id)

    if pokemon is None:
        print("Invalid Pokemon ID.")
        return

    # Check for duplicates
    if any(p["ID"] == poke_id for p in owner_node["pokedex"]):
        print("Pokemon already in the list. No changes made.")
        return

    # Add to the end of the list
    owner_node["pokedex"].append(pokemon)
    print(f"Pokemon {pokemon['Name']} (ID {pokemon['ID']}) added to {owner_node['owner'].capitalize()}'s Pokedex.")

def release_pokemon_by_name(owner_node):
    poke_name = input("Enter Pokemon Name to release: ").strip().lower()

    for i, poke in enumerate(owner_node["pokedex"]):
        if poke["Name"].lower() == poke_name:
            del owner_node["pokedex"][i]  # Remove the Pokemon
            print(f"Releasing {poke['Name']} from {owner_node['owner'].capitalize()}.")
            return

    print(f"No Pokemon named '{poke_name}' in {owner_node['owner'].capitalize()}'s Pokedex.")

def evolve_pokemon_by_name(owner_node):
    poke_name = input("Enter Pokemon Name to evolve: ").strip().lower()

    for i, poke in enumerate(owner_node["pokedex"]):
        if poke["Name"].lower() == poke_name:
            if poke["Can Evolve"] == "FALSE":
                print("This Pokemon cannot evolve.")
                return

            # Get the evolved Pokémon from HOENN_DATA
            evolved_pokemon = get_poke_dict_by_id(poke["ID"] + 1)  # Assuming evolution is next ID

            if evolved_pokemon is None:
                print("This Pokemon cannot evolve further.")
                return

            # If evolution is already in Pokedex, remove the old one
            if any(p["ID"] == evolved_pokemon["ID"] for p in owner_node["pokedex"]):
                print(f"Pokemon evolved from {poke['Name']} (ID {poke['ID']}) to {evolved_pokemon['Name']} (ID {evolved_pokemon['ID']}).")
                print(f"{evolved_pokemon['Name']} was already present; releasing it immediately.")
                del owner_node["pokedex"][i]
                return

            # Replace the Pokémon at the end of the list
            del owner_node["pokedex"][i]  # Remove old Pokémon
            owner_node["pokedex"].append(evolved_pokemon)  # Add evolved Pokemon
            print(f"Pokemon evolved from {poke['Name']} (ID {poke['ID']}) to {evolved_pokemon['Name']} (ID {evolved_pokemon['ID']}).")
            return

    print(f"No Pokemon named '{poke_name}' in {owner_node['owner'].capitalize()}'s Pokedex.")

def delete_pokedex():
    global ownerRoot

    # Get owner name (case insensitive)
    owner_name = input("Enter owner to delete: ").strip().lower()

    # Check if the owner exists in BST
    if find_owner_bst(ownerRoot, owner_name) is None:
        print(f"Owner '{owner_name}' not found.")
        return

    # Delete the owner from BST
    ownerRoot = delete_owner_bst(ownerRoot, owner_name)
    print(f"Deleting {owner_name.capitalize()}'s entire Pokedex...\nPokedex deleted.")

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

    # Sorting: First by Pokedex size (Descending), then by name (Alphabetically)
    owners_list.sort(key=lambda x: (-len(x["pokedex"]), x["owner"]))

    if not owners_list:
        print("No owners to display.")
        return

    # Print owners
    for owner in owners_list:
        print(f"Owner: {owner['owner'].capitalize()}, Number of Pokemon: {len(owner['pokedex'])}")


########################
# 6) Print All
########################

def print_all_owners():
    while True:
        print("\n-- Choose BST Traversal --")
        print("1. BFS (Level-Order)")
        print("2. Pre-Order")
        print("3. In-Order")
        print("4. Post-Order")
        print("5. Back to Main Menu")

        choice = read_int_safe("Your choice: ")

        if choice == 1:
            bfs_traversal(ownerRoot)
        elif choice == 2:
            pre_order(ownerRoot)
        elif choice == 3:
            in_order(ownerRoot)
        elif choice == 4:
            post_order(ownerRoot)
        elif choice == 5:
            print("Back to Main Menu.")
            return
        else:
            print("Invalid choice. Please enter a number between 1-5.")

def pre_order_print(node):
    if node is None:
        return

    # Print owner and their Pokemon
    print(f"\nOwner: {node['owner'].capitalize()}")
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
    print(f"\nOwner: {node['owner'].capitalize()}")
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
    print(f"\nOwner: {node['owner'].capitalize()}")
    if node["pokedex"]:
        display_pokemon_list(node["pokedex"])
    else:
        print("There are no Pokemons in this Pokedex that match the criteria.")

########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
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
            attack_threshold = read_int_safe("Enter Attack threshold: ")
            filtered = [p for p in owner_node["pokedex"] if p["Attack"] > attack_threshold]

        elif choice == 4:
            hp_threshold = read_int_safe("Enter HP threshold: ")
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

        # Display filtered Pokemon
        if filtered:
            display_pokemon_list(filtered)
        else:
            print("There are no Pokemons in this Pokedex that match the criteria.")


########################
# 8) Sub-menu & Main menu
########################
def pokedex_menu(owner_node):
    while True:
        print(f"\n-- {owner_node['owner'].capitalize()}'s Pokedex Menu --")
        print("1. Add Pokemon")
        print("2. Display Pokedex")
        print("3. Release Pokemon")
        print("4. Evolve Pokemon")
        print("5. Back to Main")

        choice = read_int_safe("Your choice: ")

        if choice == 1:
            add_pokemon_to_owner(owner_node)
        elif choice == 2:
            display_filter_sub_menu(owner_node)
        elif choice == 3:
            release_pokemon_by_name(owner_node)
        elif choice == 4:
            evolve_pokemon_by_name(owner_node)
        elif choice == 5:
            print("Back to Main Menu.")
            return
        else:
            print("Invalid choice.")

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
            print("Invalid choice. Please enter a number between 1-6.")

def main():
    main_menu()

if __name__ == "__main__":
    main()

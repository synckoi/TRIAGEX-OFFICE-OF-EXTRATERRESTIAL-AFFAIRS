DEFAULT_CHARACTERISTICS = {
    "Body type": ["Humanoid", "Machine", "Swarm", "Energy being"],
    "Size": ["Small", "Medium", "Large", "Colossal"],
    "Hazard": ["None", "Mild radiation", "Toxic emission", "Pathogen", "Unknown"],
    "Weapons": ["None", "Defensive only", "Offensive"],
    "Behavior": ["Peaceful", "Evasive", "Hostile", "Unknown"],
    "Group size": ["Single", "Small group", "Fleet"],
}

CLASSIFICATIONS = ("Harmless", "Low risk", "Dangerous", "Extreme threat")

RESPONSE_TYPES = ("Tolerate", "Observe", "Negotiate", "Contain", "Expel", "Terminate")

"""
PROCESS FUNCTIONS 
"""
# Get an answer from user input, will re-prompt if answer is empty.
def get_text(prompt):
    while True:
        temp = input(f"{prompt}\n").strip()
        if temp != "":
            return temp
        print("[X] Answer cannot be empty. Please re-enter.")
    
# Get the user choice (in integer)
def get_choicenum(prompt, lowbound, highbound):
    while True:
        temp = input(f"{prompt}")
        if temp.isdigit():
            temp = int(temp)
            if temp >= lowbound and temp <= highbound:
                return temp
        print("[X] Choice is not within the boundary, please re-enter.")    

# Display a list and prompts the user to choose one (using get_choicenum)
def choose_from_list(options):
    number = 1
    for option in options:
        print(f"[ {str(number)} ] ", option)
        number += 1
    choice = get_choicenum(" Enter choice: ", 1, len(options))
    return options[choice - 1]

# A computer automatically checks 'enter' as finishing an input. 
def pause():
    input("\n Press Enter to continue...")

"""
DISPLAY/COSMETIC FUNCTIONS
"""

def print_header(title):
    print()
    print("=" * 56)
    print("  " + title)
    print("=" * 56)

def print_line(label, value):
    # ljust(16) pads the label to 16 characters so the values line up
    print(" " + label.ljust(16) + ": " + str(value))

def show_summary(entity):
    print()
    print("=" * 45)
    print("           ENTITY SUMMARY")
    print("=" * 45)

    print_line("Codename", entity["codename"])
    print_line("Origin", entity["origin"])

    # Traits (nested dictionary)
    print("\n --- Characteristics ---")
    for category in entity["traits"]:
        print_line(category, entity["traits"][category])

    # Classification
    print("\n --- Classification ---")
    print_line("Classification", entity["classification"])
    print_line("Reason", entity["reason"])

    # Response
    print("\n --- Response ---")
    print_line("Strategy", entity["response_type"])
    print_line("Personnel sent", entity["personnel"])
    print_line("Plan", entity["response"])

    print("=" * 45)

# Cosmetic for main, MAIN header
def header(title, subtitle=None, width=50):
    inner = width - 2
    print("╔" + "═" * inner + "╗")
    print("║" + title.upper().center(inner) + "║")
    if subtitle:
        print("╟" + "─" * inner + "╢")
        print("║" + subtitle.center(inner) + "║")
    print("╚" + "═" * inner + "╝")

# DETECTION FUNCTIONS
def detection_menu():
    print_header("MANUAL ENTRY")
    entity = {}
    traits = {} 
    entity["codename"] = get_text(" Codename of the entity : ")
    entity["origin"] = get_text(" Origin (sector/location): ")

    for category in DEFAULT_CHARACTERISTICS:
        print("\n--- Category:", category, "---")
        traits[category] = choose_from_list(DEFAULT_CHARACTERISTICS[category])
        entity["traits"] = traits

    return entity

# CLASSIFY FUNCTIONS
def classify_menu(entity):
    print_header("CLASSIFICATION OF ENTITY")
    print("Classify", entity["codename"], ":")

    entity["classification"] = choose_from_list(CLASSIFICATIONS)
    entity["reason"] = get_text("Why did you choose this classification?")

# RESPONSE FUNCTIONS
def choose_response(entity):
    print("\n Choose a response strategy:")
    entity["response_type"] = choose_from_list(RESPONSE_TYPES)
    entity["response"] = get_text("Describe your plan in detail:")

def send_team(entity):
    if entity["classification"] == "Harmless":
        personnel = 5
    elif entity["classification"] == "Low risk":
        personnel = 10
    elif entity["classification"] == "Dangerous":
        personnel = 20
    elif entity["classification"] == "Extreme threat":
        personnel = 50
    print("\nUnder your current provision, you have", personnel, "OEA personnel allocated for this entity.")
    entity["personnel"] = get_choicenum(" How many will you send? ", 0, personnel)

def response_menu(entity):
    print_header("RESPONSE COMMAND")
    print("Response for", entity["codename"], ":")
    choose_response(entity)
    send_team(entity)


header("TRIAGEX", "OFFICE OF EXTRATERRESTIAL AFFAIRS")
running = True
while running:
    print_header("MAIN MENU")
    print(" [1] Detect a new arrival")
    print(" [0] Exit")
    choice = get_choicenum(" Enter your choice: ", 0, 1)

    if choice == 1:
        entity = detection_menu()
        classify_menu(entity)
        response_menu(entity)
        show_summary(entity)
        pause()
    elif choice == 0:
        print_header("Session terminated. Goodbye.")
        exit()

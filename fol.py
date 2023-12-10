from logic import *
from utils import *
import os


def clear_terminal():
    os.system('cls')


class FolKB(KB):
    def __init__(self, initial_clauses=[]):
        self.clauses = []
        for clause in initial_clauses:
            self.tell(clause)

    def tell(self, sentence):
        if is_definite_clause(sentence):
            self.clauses.append(sentence)
        else:
            raise Exception("Not a definite clause: {}".format(sentence))

    def ask_generator(self, query):
        q = expr(query)
        test_variables = variables(q)
        answers = fol_bc_ask(self, q)
        return sorted([dict((x, v) for x, v in list(a.items())
                            if x in test_variables)
                       for a in answers], key=repr)

    def retract(self, sentence):
        self.clauses.remove(sentence)

    def fetch_rules_for_goal(self, goal):
        return self.clauses


def get_characteristics(animal_name, kb):
    query = f'Characteristics({animal_name.lower()}, x)'
    result = kb.ask_generator(query)
    return result


def update_kb_with_new_animal(animal_name, kb):
    characteristics = []
    print(f"Let's add {animal_name} to our knowledge base.")

    # General characteristics
    has_fur = input("Does it have fur? (yes/no): ").lower() == 'yes'
    gives_milk = input("Does it give milk? (yes/no): ").lower() == 'yes'
    warm_blooded = input("Is it warm-blooded? (yes/no): ").lower() == 'yes'
    cold_blooded = input("Is it cold-blooded? (yes/no): ").lower() == 'yes'
    has_wings = input("Does it have wings? (yes/no): ").lower() == 'yes'
    lays_eggs = input("Does it lay eggs? (yes/no): ").lower() == 'yes'
    has_scales = input("Does it have scales? (yes/no): ").lower() == 'yes'
    has_exoskeleton = input("Does it have an exoskeleton? (yes/no): ").lower() == 'yes'
    has_slimy_skin = input("Does it have slimy skin? (yes/no): ").lower() == 'yes'

    # Update the knowledge base based on user input
    if has_fur:
        kb.tell(expr(f'HasFur({animal_name.lower()})'))
        characteristics.append('HasFur')
    if gives_milk:
        kb.tell(expr(f'GivesMilk({animal_name.lower()})'))
        characteristics.append('GivesMilk')
    if warm_blooded:
        kb.tell(expr(f'WarmBlooded({animal_name.lower()})'))
        characteristics.append('WarmBlooded')
    if cold_blooded:
        kb.tell(expr(f'ColdBlooded({animal_name.lower()})'))
        characteristics.append('ColdBlooded')
    if has_wings:
        kb.tell(expr(f'HasWings({animal_name.lower()})'))
        characteristics.append('HasWings')
    if lays_eggs:
        kb.tell(expr(f'LaysEggs({animal_name.lower()})'))
        characteristics.append('LaysEggs')
    if has_scales:
        kb.tell(expr(f'HasScales({animal_name.lower()})'))
        characteristics.append('HasScales')
    if has_exoskeleton:
        kb.tell(expr(f'HasExoskeleton({animal_name.lower()})'))
        characteristics.append('HasExoskeleton')
    if has_slimy_skin:
        kb.tell(expr(f'SlimySkin({animal_name.lower()})'))
        characteristics.append('SlimySkin')
    kb.tell(expr(f'Animal({animal_name.lower()})'))
    return characteristics


def determine_class(animal_name, kb):
    # Use a tuple instead of a list for constants
    classes = ("Mammal", "Bird", "Reptile", "Fish", "Insect")
    for c in classes:
        # Use string formatting instead of f-strings for compatibility
        query = f'{c}({animal_name.lower()})'
        # print(query)
        if kb.ask_generator(query):
            return c
    # Use None instead of "Unknown" for no match
    return None


# Knowledge Base
animal_kb = FolKB(
    map(expr, [
        '(HasFur(m) & GivesMilk(m) & WarmBlooded(m)) ==> Mammal(m)',
        '(HasWings(b) & LaysEggs(b) & WarmBlooded(b)) ==> Bird(b)',
        '(HasScales(r) & LaysEggs(r) & ColdBlooded(r)) ==> Reptile(r)',
        '(SlimySkin(a) & LayEggs(a) & WarmBlooded(a)) ==> Amphibians(a)',
        '(HasScales(f) & LaysEggs(f) & WarmBlooded(f)) ==> Fish(f)',
        '(HasExoskeleton(i) & LaysEggs(i) & ColdBlooded(i)) ==> Insect(i)',
    ])
)


# Define characteristics for each animal
characteristics_dict = {
    'dog': ['HasFur', 'GivesMilk', 'WarmBlooded'],
    'dat': ['HasFur', 'GivesMilk', 'WarmBlooded'],
    'bat': ['HasFur', 'HasWings', 'WarmBlooded'],
    'eagle': ['HasWings', 'LaysEggs', 'WarmBlooded'],
    'catfish': ['HasScales', 'LaysEggs', 'ColdBlooded'],
    'spider': ['HasExoskeleton', 'LaysEggs', 'ColdBlooded'],
}
choose = 0

while choose != '4':
    clear_terminal()
    print("\nWelcome to the animal classification app!!\n")
    print("What are we gonna do today:")
    print("1.) Animalia Class")
    print("2.) Identify Animal")
    print("3.) Animal Dictionary")
    choose = input("Your choice (1/2/3): ")
    if choose == '1':
        print("- Amphibians are vertebrates known for their dual life stages, starting in water as larvae with gills and transitioning to land as adults with lungs, moist skin, and typically undergoing metamorphosis.")
        print("- Aves, or birds, are characterized by feathers, beaks, and laying hard-shelled eggs.")
        print("- Fish are aquatic vertebrates with gills, fins, and scales, utilizing these adaptations for respiration, movement, and protection in their underwater habitat.")
        print("- Insects, the largest class of arthropods, are characterized by six legs, a three-part body (head, thorax, and abdomen), and often wings, playing crucial roles in pollination, decomposition, and various ecological processes.")
        print('- Mammals are distinguished by their possession of fur or hair, the ability to produce milk for their young, and being warm-blooded.')
        print('- Reptiles are cold-blooded animals with scales or scutes, and they typically lay eggs for reproduction.')
        input("\nPress Enter to continue...")
    if choose == '2':
        # User input for animal name
        animal_name = input("Enter the name of the animal: ")

        # Get the characteristics
        characteristics = get_characteristics(animal_name.capitalize(), animal_kb)

        # Display the result or update the knowledge base
        if characteristics:
            print(f"{animal_name} has the following characteristics:")
            for char in characteristics:
                print(f"- {char}")
        else:
            characteristics = update_kb_with_new_animal(animal_name, animal_kb)
            if characteristics:
                print("\n")
                print(f"{animal_name} has been added with the following characteristics:")
                for char in characteristics:
                    print(f"- {char}")
            else:
                print(f"Unable to add '{animal_name}' to the knowledge base.")

        # Determine and print the class of the animal
        animal_class = determine_class(animal_name, animal_kb)
        print(f"The class of {animal_name} is: {animal_class}")
        # input("\nPress Enter to continue...")
        break

    if choose == "3":
        dictInput = input("What kind of species do you want to know? ").lower()
        animalDictionary = characteristics_dict.get(dictInput)
        if animalDictionary:
            print(f"{dictInput} has the following characteristics:")
            for char in animalDictionary:
                print(f"- {char}")
        else:
            print(f"{dictInput} is not recognized in the knowledge base.")
        input("\nPress Enter to continue...")

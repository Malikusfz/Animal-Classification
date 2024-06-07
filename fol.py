from logic import *
from utils import *
import os
import pickle


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


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
        return sorted([dict((x, v) for x, v in list(a.items()) if x in test_variables)], key=repr)

    def retract(self, sentence):
        self.clauses.remove(sentence)

    def fetch_rules_for_goal(self, goal):
        return self.clauses


def save_to_cache(data, filename='animal_cache.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def load_from_cache(filename='animal_cache.pkl'):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return {}


def update_kb_with_new_animal(animal_name, kb):
    characteristics = []
    print(f"Let's add {animal_name} to our knowledge base.")

    questions = {
        "HasFur": "Does it have fur? (yes/no): ",
        "GivesMilk": "Does it give milk? (yes/no): ",
        "WarmBlooded": "Is it warm-blooded? (yes/no): ",
        "ColdBlooded": "Is it cold-blooded? (yes/no): ",
        "HasWings": "Does it have wings? (yes/no): ",
        "LaysEggs": "Does it lay eggs? (yes/no): ",
        "HasScales": "Does it have scales? (yes/no): ",
        "HasExoskeleton": "Does it have an exoskeleton? (yes/no): ",
        "SlimySkin": "Does it have slimy skin? (yes/no): ",
        "LiveLand": "Does it live on land? (yes/no): ",
        "LiveWater": "Does it live in water? (yes/no): ",
    }

    for characteristic, question in questions.items():
        if input(question).lower() == 'yes':
            kb.tell(expr(f'{characteristic}({animal_name.lower()})'))
            characteristics.append(characteristic)

    kb.tell(expr(f'Animal({animal_name.lower()})'))
    return characteristics


def determine_class(animal_name, kb):
    classes = ("Mammal", "Bird", "Reptile", "Fish", "Insect", "Amphibian")
    for c in classes:
        query = f'{c}({animal_name.lower()})'
        if kb.ask_generator(query):
            return c
    return "Unknown"


def display_animal_table(animal_dict):
    animals = list(animal_dict.keys())
    num_rows = (len(animals) + 4) // 5

    print("\nTable of Animals:")
    for i in range(num_rows):
        row_start = i * 5
        row_end = min(row_start + 5, len(animals))
        row_animals = animals[row_start:row_end]
        print("".join("{:<20}".format(animal) for animal in row_animals))


def main():
    animal_kb = FolKB(
        map(expr, [
            '(HasFur(m) & GivesMilk(m) & WarmBlooded(m) & LiveLand(m)) ==> Mammal(m)',
            '(HasWings(b) & LaysEggs(b) & WarmBlooded(b) & LiveLand(b)) ==> Bird(b)',
            '(HasScales(r) & LaysEggs(r) & ColdBlooded(r) & LiveLand(r)) ==> Reptile(r)',
            '(SlimySkin(a) & LaysEggs(a) & ColdBlooded(a) & LiveLand(a) & LiveWater(a)) ==> Amphibian(a)',
            '(HasScales(f) & LaysEggs(f) & ColdBlooded(f) & LiveWater(f)) ==> Fish(f)',
            '(HasExoskeleton(i) & LaysEggs(i) & ColdBlooded(i) & LiveLand(i)) ==> Insect(i)',
        ])
    )

    characteristics_dict = load_from_cache()

    while True:
        clear_terminal()
        print("\nWelcome to the animal classification app!!\n")
        print("What are we gonna do today:")
        print("1.) Learn about Animal Classes")
        print("2.) Identify Animal")
        print("3.) View Animal Dictionary")
        print("4.) Exit")
        choice = input("Your choice (1/2/3/4): ")

        if choice == '1':
            print("- Amphibians are vertebrates known for their dual life stages, starting in water as larvae with gills and transitioning to land as adults with lungs, moist skin, and typically undergoing metamorphosis.")
            print("- Birds are characterized by feathers, beaks, and laying hard-shelled eggs.")
            print("- Fish are aquatic vertebrates with gills, fins, and scales, utilizing these adaptations for respiration, movement, and protection in their underwater habitat.")
            print("- Insects, the largest class of arthropods, are characterized by six legs, a three-part body (head, thorax, and abdomen), and often wings, playing crucial roles in pollination, decomposition, and various ecological processes.")
            print('- Mammals are distinguished by their possession of fur or hair, the ability to produce milk for their young, and being warm-blooded.')
            print('- Reptiles are cold-blooded animals with scales or scutes, and they typically lay eggs for reproduction.')
            input("\nPress Enter to continue...")

        elif choice == '2':
            animal_name = input("Enter the name of the animal: ").lower()
            if animal_name in characteristics_dict:
                print(f"{animal_name} already exists in the knowledge base.")
            else:
                characteristics = update_kb_with_new_animal(animal_name, animal_kb)
                if characteristics:
                    print(f"\n{animal_name} has been added with the following characteristics:")
                    for char in characteristics:
                        print(f"- {char}")
                    characteristics_dict[animal_name] = characteristics
                    save_to_cache(characteristics_dict)
                else:
                    print(f"Unable to add '{animal_name}' to the knowledge base.")
                animal_class = determine_class(animal_name, animal_kb)
                print(f"The class of {animal_name} is: {animal_class}")
            input("\nPress Enter to continue...")

        elif choice == '3':
            display_animal_table(characteristics_dict)
            dict_input = input("\nWhich animal do you want to know about? ").lower()
            if dict_input in characteristics_dict:
                animal_dictionary = characteristics_dict[dict_input]
                print(f"\n{dict_input} has the following characteristics:")
                for char in animal_dictionary:
                    print(f"- {char}")
                print(f"\nThe class of {dict_input} is: {animal_dictionary[-1]}")
            else:
                print(f"{dict_input} is not recognized in the knowledge base.")
            input("\nPress Enter to continue...")

        elif choice == '4':
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

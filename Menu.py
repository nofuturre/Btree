from BTree import BTree
from Record import Record


class Menu:
    def __init__(self, verbose, d):
        self.file = "test.txt"
        self.verbose = verbose
        self.quit = False
        self.tree = BTree(d)

    def print_menu(self):
        if self.verbose:
            print("\nVerbose mode ON\n")
        source = input("Instructions source: \n the keyboard -> press k \n the file -> press f\n")

        if source == 'k':
            self.custom_menu()
        elif source == 'f':
            self.file_menu()
        else:
            return

    def custom_menu(self):
        while not self.quit:
            print("\nChoose action: ")
            print("add record         -> press a")
            print("delete record      -> press d")
            print("actualize record   -> press c")
            print("reorganize records -> press o")
            print("read record        -> press r")
            print("read file          -> press f")
            print("read index         -> press i")
            print("QUIT               -> press q")

            instruction = input()

            if instruction == 'a':
                key = input("Key value: ")
                record = Record(key)
                self.tree.insert(record)
            elif instruction == 'r':
                key = input("Key value: ")
                self.tree.print_record(key)
            elif instruction == 'q':
                self.quit = True

            if self.verbose:
                self.tree.print_tree(self.tree.root)

    def file_menu(self):
        with open(self.file) as f:
            for line in f:
                instruction = line[0]
                if instruction == 'a':
                    key = int(line.split(" ")[1])
                    print(f"\n\tAdd record: {key}")
                    self.tree.insert(Record(key))
                elif instruction == 'r':
                    key = int(line.split(" ")[1])
                    print(f"\n\tPrint {key}. record's data")
                    self.tree.print_record(key)
                if self.verbose:
                    self.tree.print_tree(self.tree.root)



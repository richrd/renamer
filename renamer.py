"""
Command line file renamer.

Usage: python renamer.py path_to_files operation [arguments]
"""

import os
import sys

class Renamer:
    def __init__(self):
        self.old_names = []
        self.new_names = []
        self.operation = []
        self.path = ""
        self.target = ""

    def log(self, s):
        """Prints to console."""
        print s

    def delete(self, name):
        """Remove a string from filename."""
        return name.replace(self.operation[0], "")

    def append(self, name):
        """Append a string to the filename."""
        return name + self.operation[0]

    def prepend(self, name):
        """Prepend a string to the filename."""
        return self.operation[0] + name

    def make_numeric(self, name):
        """Drop all characters except digits."""
        new_name = ""
        for char in name:
            if char in ["0","1","2","3","4","5","6","7","8","9"]:
                new_name = new_name + char
        return new_name

    def subtract(self, name):
        """Subtract a number from an all numeric filename."""
        value = int(self.operation[0])
        return str(int(name)-value)

    def add(self, name):
        """Add a number to an all numeric filename."""
        value = int(self.operation[0])
        return str(int(name)+value)

    def truncate(self, name):
        """Keep the specified amount of characters, and delete the rest."""
        length = int(self.operation[0])
        return name[:length]

    def list_files(self, path):
        """Return list of files in path. Omits dotfiles."""
        unfiltered = os.listdir(path)
        filtered = []
        for name in unfiltered:
            full_path = path + name
            if os.path.isfile(full_path):
                if name[0] == ".":
                    continue
                filtered.append(name)
        return filtered

    def process_files(self, action):
        """Generates new filenames by filtering existing names."""
        self.old_names = self.list_files(self.path)
        for name in self.old_names:
            new_name = action(name)
            self.new_names.append(new_name)
        self.commit_renames()

    def commit_renames(self, dummy = False):
        """Commits changes to file names."""
        i = 0
        while i < len(self.old_names):
            old, new = self.old_names[i], self.new_names[i]
            old_path = self.path + old
            new_path = self.path + new
            self.log("renaming " + old + "\t\t->\t\t" + new)
            if not dummy:
                os.rename(old_path, new_path)
            i += 1

    def run(self):
        """Runs the app."""
        args = sys.argv[1:]
        self.operation = []
        if len(args) < 2:
            self.log("please at least specify path and operation")
            sys.exit(0)

        if len(args) > 2:
            self.operation = args[2:]

        self.path = args[0]
        if self.path[-1] != "/":
            self.path += "/"


        action = args[1]
        actions = {
            "del": self.delete,
            "append": self.append,
            "prepend": self.prepend,
            "make_numeric": self.make_numeric,
            "truncate": self.truncate,
            "add": self.add,
            "subtract": self.subtract,
        }

        if not action in actions.keys():
            self.log("unknown action. use one of: "+(", ".join(actions.keys())))
            sys.exit(0)

        self.process_files(actions[action])

if __name__ == "__main__":
    app = Renamer()
    app.run()
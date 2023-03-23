import dataclasses

class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.directories = {}
        self.files = {}
        self.total_size = None

    def get_total_size(self):
        if self.total_size is not None:
            return self.total_size
        self.total_size = 0
        for d in self.directories.values():
            self.total_size += d.get_total_size()
        for size in self.files.values():
            self.total_size += size
        return self.total_size

    def cd(self, name):
        if name == "..":
            return self.parent
        if name not in self.directories:
            self.directories[name] = Directory(name, parent=self)
        return self.directories[name]

    def get_all_subdirs_recursively(self):
        subdirs = []
        for d in self.directories.values():
            subdirs += d.get_all_subdirs_recursively()
        subdirs += list(self.directories.values())
        return subdirs

root_dir = Directory("/")
current_dir = root_dir
with open("07/input.txt") as f:
    for line in f:
        line = line.strip()
        if line.startswith("$ cd"):
            target = line[5:]
            if target == "/":
                current_dir = root_dir
            else:
                current_dir = current_dir.cd(target)
        elif line.startswith("$ ls"):
            continue
        elif line.startswith("dir"):
            continue
        else:
            size, fname = line.split(" ")
            current_dir.files[fname] = int(size)

# part1
max_dir_size = 100_000
all_dirs = [root_dir, *root_dir.get_all_subdirs_recursively()]
filtered_dirs = [d for d in all_dirs if d.get_total_size() <= max_dir_size]
print(sum([d.total_size for d in filtered_dirs]))

#part2
required_space = 30000000
total_space = 70000000
required_deletion = required_space - (total_space - root_dir.total_size)
filtered_dirs = [d for d in all_dirs if d.total_size >= required_deletion]
smallest_dir = min(filtered_dirs, key=lambda d: d.total_size)
print(smallest_dir.total_size)



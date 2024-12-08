#!/usr/bin/env python3

import argparse
import datetime
import os


def main():
    parser = argparse.ArgumentParser(description="Create a new Advent of Code day.")
    parser.add_argument("--day", type=int, help="The day to create", default=0)
    parser.add_argument("--year", type=int, help="The year to create the day in", default=0)
    args = parser.parse_args()

    day = args.day or datetime.datetime.now().day
    year = args.year or datetime.datetime.now().year

    directory = f"{year}/{day:02d}"
    if os.path.exists(directory):
        print(f"Directory {directory} already exists.")
        return
    else:
        print(f"Creating directory {directory}")
        os.makedirs(directory)
        open(f"{directory}/input.txt", "w").close()
        open(f"{directory}/test_input.txt", "w").close()
        open(f"{directory}/{day:02d}.py", "w").close()


if __name__ == "__main__":
    main()

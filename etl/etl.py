import random
import time

AVENGERS = ("Hulk", "Black Widow", "Hawkeye", "Iron Man", "Thor", "Black Panther", "Captain America")


def get_team(number_of_avengers):
    return random.sample(AVENGERS, number_of_avengers)


def write_team():
    with open(f"avenger_files/{str(int(time.time()))}.txt", "w") as f:
        f.write(str(get_team(4)))


if __name__ == "__main__":
    write_team()

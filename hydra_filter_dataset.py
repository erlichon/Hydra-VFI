import os
import random
from sys import argv
import numpy as np

DELIMITER = ";;;"

def split_list_random_block(data_list, block_percentage=30):
    """
    Splits the input list into a random continuous block of a specified percentage
    and the remaining elements.

    Parameters:
    - data_list: The list to be split
    - block_percentage: The size of the block as a percentage of the list's length (between 0 and 100)

    Returns:
    A tuple (random_block, remaining).
    """
    if not (0 < block_percentage < 100):
        raise ValueError("block_percentage must be between 0 and 100")

    # Calculate the size of the block
    block_size = int(round(len(data_list) * (block_percentage / 100)))
    if block_size < 3:
        print("one of the videos has less than 15 images")

    # Ensure the block size is at least 3
    block_size = max(3, block_size)

    # Calculate the maximum starting index to ensure the block fits within the list
    max_start_index = len(data_list) - block_size - 3

    # Randomly select a starting index
    start_index = random.randint(3, max_start_index)

    # Get the continuous block
    random_block = data_list[start_index:start_index + block_size]

    # Get the remaining elements
    before_random_block = data_list[:start_index] 
    after_random_block = data_list[start_index + block_size:]

    if len(before_random_block) < 3 or len(after_random_block) < 3:
        print("bad random selection of random block")

    return before_random_block, random_block, after_random_block



def generate_continuous_triplets(input_list):
    # Create a list to hold the continuous triplets
    triplets = []

    # Loop through the list, only up to the third to last element
    for i in range(len(input_list) - 2):
        # Append a slice of three elements to the triplets list
        triplets.append(input_list[i:i + 3])

    return triplets

def split_list_by_percentage(lst, percent1):
    """
    Splits a list into two random sub-lists based on the given percentage.

    Parameters:
    - lst: Input list to split.
    - percent1: Percentage of elements to include in the first sub-list. 
                 Should be a float between 0 and 100.

    Returns:
    - Two sub-lists split by the specified percentage.
    """
    # Validate percentage input
    if not (0 <= percent1 <= 100):
        raise ValueError("The percentage must be between 0 and 100.")

    length = len(lst)
    size1 = int(round(length * (percent1 / 100.0)))
    size2 = length - size1

    # Shuffle the original list to randomize elements
    shuffled_list = lst[:]
    random.shuffle(shuffled_list)

    # Split the shuffled list into two parts
    sub_list1 = shuffled_list[:size1]
    sub_list2 = shuffled_list[size1:]

    return sub_list1, sub_list2




LONGEST_VIDEOS = ['2023_11_20_pos2', '2022_11_03_pos1', '2020_08_03_pos4', '2020_08_03_pos3', '2020_08_03_pos1']

# line to sort videos by number of frames:  db_dir_folders_sorted = sorted([i for i in os.listdir("./") if os.path.isdir(i)], key=lambda x: len(os.listdir(os.path.join("./", x))))
# line to verify it works:  [len(os.listdir(os.path.join("./", i))) for i in db_dir_folders_sorted]

def write_all_good_lines(src_fd, dst_fd):
    src_fd_lines = src_fd.readlines()
    random.shuffle(src_fd_lines)
    for line in src_fd_lines:
        line = line.strip()
        if any([i in line for i in LONGEST_VIDEOS]):
            dst_fd.write(line + "\n")

def main(db_dir, trainlist_filename="tri_trainlist.txt", testlist_filename="tri_testlist.txt", vallist_filename="tri_vallist.txt"):
    train_fd = open(os.path.join(db_dir, trainlist_filename), "r")
    test_fd = open(os.path.join(db_dir, testlist_filename), "r")
    val_fd = open(os.path.join(db_dir, vallist_filename), "r")
    filtered_train_fd = open(os.path.join(db_dir, trainlist_filename + ".filtered"), "w")
    filtered_test_fd = open(os.path.join(db_dir, testlist_filename + ".filtered"), "w")
    filtered_val_fd = open(os.path.join(db_dir, vallist_filename + ".filtered"), "w")
    write_all_good_lines(train_fd, filtered_train_fd)
    write_all_good_lines(test_fd, filtered_test_fd)
    write_all_good_lines(val_fd, filtered_val_fd)
    train_fd.close()
    test_fd.close()
    val_fd.close()
    filtered_train_fd.close()
    filtered_test_fd.close()
    filtered_val_fd.close()

if __name__ == "__main__":
    if len(argv) != 2:
        print(f"Usage: {argv[0]} db_dirpath")
        exit(-1)
    main(argv[1])
        





        
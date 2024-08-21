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




def main(db_dir, trainlist_filename="tri_trainlist.txt", testlist_filename="tri_testlist.txt", vallist_filename="tri_vallist.txt"):
    train_fd = open(os.path.join(db_dir, trainlist_filename), "w")
    test_fd = open(os.path.join(db_dir, testlist_filename), "w")
    val_fd = open(os.path.join(db_dir, vallist_filename), "w")
    db_dir_folders_sorted = sorted([i for i in os.listdir(db_dir) if os.path.isdir(i)], key=lambda x: len(os.listdir(os.path.join(db_dir, x))))
    for i in os.listdir(db_dir):
        single_video_dir = os.path.abspath(os.path.join(db_dir, i))
        if os.path.isdir(single_video_dir):
            video_sorted_imgs = sorted([os.path.join(single_video_dir, i) for i in os.listdir(single_video_dir)])
            train_before_test_imgs, test_imgs, train_after_test_imgs = split_list_random_block(video_sorted_imgs)
            train_triplets = generate_continuous_triplets(train_before_test_imgs) + generate_continuous_triplets(train_after_test_imgs)
            test_triplets = generate_continuous_triplets(test_imgs)
            train_fd.write("\n".join([DELIMITER.join(triplet) for triplet in train_triplets]) + "\n")
            test_fd.write("\n".join([DELIMITER.join(triplet) for triplet in test_triplets]) + "\n")
    train_fd.close()
    test_fd.flush()
    test_fd.close()
    test_fd = open(os.path.join(db_dir, testlist_filename), "r")
    test_triplets_lines = [i.strip() for i in test_fd.readlines()]
    test_triplets_lines, val_triplets_lines = split_list_by_percentage(test_triplets_lines, 60)
    test_fd = open(os.path.join(db_dir, testlist_filename), "w")
    test_fd.write("\n".join(test_triplets_lines) + "\n")
    val_fd.write("\n".join(val_triplets_lines) + "\n")
    test_fd.close()
    val_fd.close()

if __name__ == "__main__":
    if len(argv) != 2:
        print(f"Usage: {argv[0]} db_dirpath")
        exit(-1)
    main(argv[1])
        





        
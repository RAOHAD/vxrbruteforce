import time
import os
import random
import threading
from colorama import Fore, init
from tqdm import tqdm
from queue import Queue
import sys

# Colorama initialization for colored output
init(autoreset=True)

# BIG BANNER
def print_banner():
    print("\n" + "=" * 60)
    print(" " * 20 + "RAOHAD")
    print("=" * 60 + "\n")

# User input (username and password)
def get_user_input():
    username_input = input("Enter username: ")
    password_input = input("Enter password: ")
    return username_input, password_input

# Correct username and password
correct_username = "RAOHAD"
correct_password = "Void X Raven"

# User input validation
def validate_credentials(username_input, password_input):
    if username_input == correct_username and password_input == correct_password:
        return True
    return False

# File existence check
def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        print(Fore.RED + "\nFile not found! Please provide the correct path.")
        return False

# Get random password list
def get_random_password_list(password_list, max_size=1000):
    return random.sample(password_list, min(max_size, len(password_list)))

# Password check thread function
def check_password_thread(password_list, result_queue):
    for password in password_list:
        time.sleep(0.01)  # Speed up checking
        if password == "correct_password_from_link":  # Correct password check
            result_queue.put(f"Password found: {password}")
            break
    else:
        result_queue.put("Password not found.")

# File output
def write_to_file(result):
    with open("password_check_results.txt", "a", encoding="utf-8") as result_file:
        result_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {result}\n")

# Password check function
def check_passwords(password_list_location):
    print("\nPassword checking started...\n")
    try:
        with open(password_list_location, "r", encoding="utf-8") as file:
            password_list = file.read().splitlines()

        # Sample the random password list
        max_size = int(input("How many passwords do you want to check? (Less than 1000): "))
        password_list = get_random_password_list(password_list, max_size)

        # Threading queue and thread creation
        result_queue = Queue()
        num_threads = 4  # Number of threads
        threads = []
        chunk_size = len(password_list) // num_threads

        # Start multi-threading
        for i in range(num_threads):
            chunk = password_list[i * chunk_size: (i + 1) * chunk_size]
            thread = threading.Thread(target=check_password_thread, args=(chunk, result_queue))
            threads.append(thread)
            thread.start()

        # Collect thread results
        for thread in threads:
            thread.join()

        # Read results from queue
        while not result_queue.empty():
            result = result_queue.get()
            print(result)
            write_to_file(result)

    except FileNotFoundError:
        print(Fore.RED + "Password list file not found!")

# Main Function to run the tool
def main():
    print_banner()

    username_input, password_input = get_user_input()

    if validate_credentials(username_input, password_input):
        print("\nSuccessfully logged in!")

        # Facebook account link input
        account_link = input("\nNow enter the Facebook account link: ")

        # Password list file location input
        password_list_location = input("Enter the password list file location: ")

        # File existence check
        if file_exists(password_list_location):
            check_passwords(password_list_location)
    else:
        print(Fore.RED + "\nWrong Password, Fuck You!")

if __name__ == "__main__":
    main()
import argparse
import hashlib
from itertools import product
import logging
import concurrent.futures
from typing import Callable, Generator, Optional
import string

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_hash_function(mode: int) -> Optional[Callable[[], hashlib.scrypt]]:
    """
    Retrieve the appropriate hash function based on the given mode.

    Args:
        mode (int): The hash mode (0=MD5, 1=SHA-1, 2=SHA-256, 3=SHA-512).

    Returns:
        Optional[Callable[[], hashlib.Hash]]: The hash function if mode is valid, otherwise None.
    """
    hash_funcs = {
        0: hashlib.md5,
        1: hashlib.sha1,
        2: hashlib.sha256,
        3: hashlib.sha512
    }
    return hash_funcs.get(mode)

def hash_password(password: str, hash_func: Callable[[], hashlib.scrypt]) -> str:
    """
    Hash a password using the specified hash function.

    Args:
        password (str): The password to hash.
        hash_func (Callable[[], hashlib.Hash]): The hash function to use.

    Returns:
        str: The hexadecimal digest of the hashed password.
    """
    hasher = hash_func()
    hasher.update(password.encode())
    return hasher.hexdigest()

def generate_passwords(charset: str, max_length: int) -> Generator[str, None, None]:
    """
    Generate passwords of lengths from 1 to max_length using the charset.

    Args:
        charset (str): The set of characters to use for generating passwords.
        max_length (int): The maximum length of passwords to generate.

    Yields:
        Generator[str, None, None]: A generator yielding passwords.
    """
    for length in range(1, max_length + 1):
        for candidate in product(charset, repeat=length):
            yield ''.join(candidate)

def attempt_password(password: str, hash_func: Callable[[], hashlib.scrypt], target_hash: str) -> Optional[str]:
    """
    Attempt to hash the password and check against the target hash.

    Args:
        password (str): The password to attempt.
        hash_func (Callable[[], hashlib.Hash]): The hash function to use.
        target_hash (str): The target hash to compare against.

    Returns:
        Optional[str]: The password if it matches the target hash, otherwise None.
    """
    hashed = hash_password(password, hash_func)
    if hashed == target_hash:
        return password
    return None

def brute_force_attack(hash_func: Callable[[], hashlib.scrypt], target_hash: str, charset: str, max_length: int) -> Optional[str]:
    """
    Perform a brute-force attack to find the password that matches the target hash.

    Args:
        hash_func (Callable[[], hashlib.Hash]): The hash function to use.
        target_hash (str): The target hash to crack.
        charset (str): The set of characters to use for generating passwords.
        max_length (int): The maximum length of passwords to test.

    Returns:
        Optional[str]: The found password if one matches the target hash, otherwise None.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(attempt_password, password, hash_func, target_hash): password 
                   for password in generate_passwords(charset, max_length)}

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                return result

    return None

def dictionary_attack(hash_func: Callable[[], hashlib.scrypt], target_hash: str, dictionary_file: str) -> Optional[str]:
    """
    Perform a dictionary attack to find the password that matches the target hash.

    Args:
        hash_func (Callable[[], hashlib.Hash]): The hash function to use.
        target_hash (str): The target hash to crack.
        dictionary_file (str): The file containing potential passwords.

    Returns:
        Optional[str]: The found password if one matches the target hash, otherwise None.
    """
    try:
        with open(dictionary_file, 'r') as file:
            for line in file:
                password = line.strip()
                hashed = hash_password(password, hash_func)
                if hashed == target_hash:
                    return password
    except FileNotFoundError:
        logging.error(f"Dictionary file '{dictionary_file}' not found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return None

def main() -> None:
    """
    Main function to parse arguments and start the hash cracking process.
    """
    parser = argparse.ArgumentParser(description="Simple hash cracker.")
    parser.add_argument("-m", "--mode", type=int, required=True, choices=[0, 1, 2, 3], help="Hash mode: 0=MD5, 1=SHA-1, 2=SHA-256, 3=SHA-512")
    parser.add_argument("-a", "--attack", type=int, required=True, choices=[0, 1], help="Attack mode: 0=Brute-Force, 1=Dictionary")
    parser.add_argument("--hash", type=str, help="Target hash (use with --hash-file)")
    parser.add_argument("--hash-file", type=str, help="File containing target hash (use with --hash)")
    parser.add_argument("--dictionary", type=str, help="Dictionary file for dictionary attack")
    parser.add_argument("--max-length", type=int, default=4, help="Maximum length for brute-force attack")
    parser.add_argument("--charset", type=str, default=string.ascii_letters + string.digits, help="Charset for brute-force attack")

    args = parser.parse_args()

    target_hash = args.hash if args.hash else None
    if args.hash_file:
        try:
            with open(args.hash_file, 'r') as file:
                target_hash = file.read().strip()
        except FileNotFoundError:
            logging.error(f"Hash file '{args.hash_file}' not found.")
            return

    if not target_hash:
        parser.error("No hash provided. Use --hash or --hash-file.")

    hash_func = get_hash_function(args.mode)
    if hash_func is None:
        parser.error(f"Invalid hash mode '{args.mode}'.")

    if args.attack == 0:
        logging.info("Starting brute-force attack...")
        result = brute_force_attack(hash_func, target_hash, args.charset, args.max_length)
        if result:
            logging.info(f"Password found: {result}")
        else:
            logging.info("Password not found. Try increasing --max-length or modifying the charset.")
    elif args.attack == 1:
        if not args.dictionary:
            parser.error("Dictionary file required for dictionary attack.")
        logging.info("Starting dictionary attack...")
        result = dictionary_attack(hash_func, target_hash, args.dictionary)
        if result:
            logging.info(f"Password found: {result}")
        else:
            logging.info("Password not found. Check the dictionary file and ensure it contains the correct passwords.")

if __name__ == "__main__":
    main()

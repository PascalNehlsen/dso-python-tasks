# My `hydra` Tool

This repository contains the source code for my own implementation of the `hydra` tool, a network logon cracker used for brute-force attacks against various protocols. This lightweight implementation focuses on SSH brute-force and dictionary attacks.

> [!CAUTION]  
> **Only for Testing Purposes.**  
> This tool is intended for educational and authorized penetration testing purposes only. Unauthorized use of this tool against systems that you do not have explicit permission to test is illegal and unethical.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage Examples](#usage-examples)
  - [Options](#options)
  - [Dictionary Attack](#dictionary-attack)
  - [Brute-Force Attack](#brute-force-attack)
- [Logging](#logging)
- [Contact](#contact)

## Features

This implementation covers the following features/options:

- **SSH Brute-Force Attack**: Attempts to crack SSH passwords by trying all combinations within a given length and character set.
- **Dictionary Attack**: Uses a provided wordlist to attempt to find the correct password.
- **Configurable Parameters**: Allows customization of minimum and maximum password lengths, as well as character sets.
- **Logging**: Provides detailed logs of all connection attempts and outcomes.

## Getting Started

To get started with the `hydra` tool, follow these steps:

1. **Clone the Repository**:

```shell
bash
git clone https://github.com/yourusername/hydra.git
cd hydra
```

2. **Install Dependencies**:
   Ensure you have **paramiko** installed. You can install it using pip:

```shell
bash
pip install paramiko
```

## Usage Examples

### Options

| Option                   | Description                                    | Required |
| ------------------------ | ---------------------------------------------- | -------- |
| `-u` <br> `--username`   | Username for SSH login                         | x        |
| `-s` <br> `--server`     | Server IP address or DNS                       | x        |
| `-p` <br> `--port`       | Port for SSH connection (default is 22)        |          |
| `-w` <br> `--wordlist`   | Path to the wordlist for dictionary attack     |          |
| `-c` <br> `--character`  | Charset for brute force attack                 |          |
| `--min` <br> `--minimum` | Minimum password length for brute force attack |          |
| `--max` <br> `--maximum` | Maximum password length for brute force attack |          |

### Dictionary Attack

To perform a dictionary attack using a wordlist, use the following command:

```shell
python hydra.py \
    -u <username> \
    -s <server> \
    -p <port> \
    -w <path_to_wordlist>
```

- username: The SSH username.
- server: The IP address or DNS name of the SSH server.
- port: The port for SSH connection (default is 22 if not specified).
- path_to_wordlist: Path to the wordlist file.

Example:

```shell
python hydra.py \
    -u root \
    -s localhost\
    -p 2222 \
    -w ./password.txt
```

### Brute-Force Attack

To perform a brute-force attack without a wordlist, use the following command:

```shell
python hydra.py \
    -u <username> \
    -s <server> \
    -p <port> \
    --min <min_length> \
    --max <max_length> \
    -c <charset>
```

- username: The SSH username.
- server: The IP address or DNS name of the SSH server.
- port: The port for SSH connection (default is 22 if not specified).
- min_length: Minimum length of the password.
- max_length: Maximum length of the password.
- charset: Characters to use in the password generation (default is alphanumeric).

Example:

```shell
python hydra.py \
    -u root \
    -s localhost \
    -p 2222 \
    --min 1 \
    --max 4 \
    -c abc123
```

## Logging

Logs are written to **hydra.log**. You can check this file to review detailed information about the connection attempts and outcomes.

## Contact

- Pascal Nehlsen - [LinkedIn](https://www.linkedin.com/in/pascal-nehlsen) - [mail@pascal-nehlsen.de](mailto:mail@pascal-nehlsen.de)
- Project Link: [https://github.com/PascalNehlsen/dso-python-tasks/tree/main/module-5/hydra](https://github.com/PascalNehlsen/dso-python-tasks/tree/main/module-5/hydra)

# My `hashcat` Tool

This repository contains the source code for my own implementation of the **hashcat** tool.

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

- **Brute-Force Attack**: Attempts to crack passwords by trying all combinations within a given length and character set.
- **Dictionary Attack**: Uses a provided wordlist to attempt to find the correct password.
- **Configurable Parameters**: Allows customization of password length, character set, and hash modes (MD5, SHA-1, SHA-256, SHA-512).
- **Logging**: Provides detailed logs of all connection attempts and outcomes.

## Getting Started

To get started with the `hashcat` tool, follow these steps:

1. **Clone the Repository**:

```shell
git clone https://github.com/yourusername/hashcat.git
cd hydra
```

2. **Install Dependencies**:
   Ensure you have **Python 3** installed. The required Python packages can be installed using pip:

```shell
pip install hashlib
```

## Usage Examples

### Options

| Option               | Description                                     | Required |
| -------------------- | ----------------------------------------------- | -------- |
| `-m` <br> `--mode`   | Hash mode: 0=MD5, 1=SHA-1, 2=SHA-256, 3=SHA-512 | x        |
| `-a` <br> `--attack` | Attack mode: 0=Brute-Force, 1=Dictionary        | x        |
| `--hash`             | Target hash (use with `--hash-file`)            | x        |
| `--hash-file`        | File containing target hash (use with `--hash`) | x        |
| `--dictionary`       | Dictionary file for dictionary attack           |          |
| `--max-length`       | Maximum length for brute-force attack           |          |
| `--charset`          | Charset for brute-force attack                  |          |

### Dictionary Attack

To perform a dictionary attack using a wordlist, use the following command:

```shell
python hashcat.py \
    -m <mode> \
    -a <attack> \
    --hash <target_hash> \
    -dictionary <path_to_dictionary>
```

- mode: The hash mode (0=MD5, 1=SHA-1, 2=SHA-256, 3=SHA-512).
- target_hash: The hash you are attempting to crack.
- path_to_dictionary: Path to the wordlist file.

Example:

```shell
python hashcat.py \
    -m 0 \
    -a 1 \
    --hash 5f4dcc3b5aa765d61d8327deb882cf99 \
    -dictionary ./passwords.txt
```

### Brute-Force Attack

To perform a brute-force attack without a wordlist, use the following command:

```shell
python hashcat.py \
    -m <mode> \
    -a <attack> \
    --hash <target_hash> \
    --max-length <max_length> \
    --charset <charset>
```

- mode: The hash mode (0=MD5, 1=SHA-1, 2=SHA-256, 3=SHA-512).
- target_hash: The hash you are attempting to crack.
- max_length: Maximum length of the password.
- charset: Characters to use in the password generation.

Example:

```shell
python hashcat.py \
    -m 2 \
    -a 0 \
    --hash 826ecad4ae11c8196ab3432ccbb22400691c248131b97fa4fe6f02dcf20f6049 \
    --max-length 7 \
    --charset 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
```

## Logging

Logs are written to the console. You can modify the logging level in the code if you need to adjust the verbosity of the output.

## Contact

- Pascal Nehlsen - [LinkedIn](https://www.linkedin.com/in/pascal-nehlsen) - [mail@pascal-nehlsen.de](mailto:mail@pascal-nehlsen.de)
- Project Link: [https://github.com/PascalNehlsen/dso-python-tasks/tree/main/module-5/hashcat](https://github.com/PascalNehlsen/dso-python-tasks/tree/main/module-5/hashcat)

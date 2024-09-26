# My `hashcat` Tool

This repository contains the source code for my own implementation of the **hashcat** tool.

> [!CAUTION]  
> **Only for Testing Purposes.**  
> This tool is intended for educational and authorized penetration testing purposes only. Unauthorized use of this tool against systems that you do not have explicit permission to test is illegal and unethical.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage Examples](#usage-examples)
  - [Brute-Force Attack](#brute-force-attack)
  - [Dictionary Attack](#dictionary-attack)
  - [Hashcat-Options](#options)
- [Logging](#logging)
- [Contact](#contact)

## Features

This implementation covers the following features/options:

- **Brute-Force Attack**: Attempts to crack passwords by trying all combinations within a given length and character set.
- **Dictionary Attack**: Uses a provided wordlist to attempt to find the correct password.
- **Configurability**: Allows customization of password length, character set, and hash modes (MD5, SHA-1, SHA-256, SHA-512).
- **Logging**: Provides unstructured detailed logs of all connection attempts and outcomes.

**Technologies**:

- Python 3

## Getting Started

To get started with the `hashcat` tool, follow these steps:

1. **Clone the Repository**:

```shell
git clone https://github.com/pascalnehlsen/hashcat.git
cd hashcat
```

## Usage Examples

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

Example:

```shell
python hashcat.py \
    -m 2 \
    -a 0 \
    --hash 826ecad4ae11c8196ab3432ccbb22400691c248131b97fa4fe6f02dcf20f6049 \
    --max-length 7 \
    --charset 'abcdefghijklmnopqrstuvwxyz'
```

### Dictionary Attack

To perform a dictionary attack using a wordlist, use the following command:

```shell
python hashcat.py \
    -m <mode> \
    -a <attack> \
    --hash <target_hash> \
    -dictionary <path_to_dictionary>
```

- path_to_wordlist (`-dictionary`): Path to the dictionary file (required for dictionary attack)

Example:

```shell
python hashcat.py \
    -m 0 \
    -a 1 \
    --hash 826ecad4ae11c8196ab3432ccbb22400691c248131b97fa4fe6f02dcf20f6049 \
    -dictionary ./small-password-list.txt
```

### Options

| Option         | Shorthand | Description                                     | Default value | Required |
| -------------- | --------- | ----------------------------------------------- | ------------- | -------- |
| `--mode`       | `-m`      | Hash mode: 0=MD5, 1=SHA-1, 2=SHA-256, 3=SHA-512 | 2             |          |
| `--attack`     | `-a`      | Attack mode: 0=Brute-Force, 1=Dictionary        | 0             |          |
| `--hash`       | -         | Target hash                                     | -             | x        |
| `--hash-file`  | -         | File path containing target hash                | -             | x        |
| `--dictionary` | `-d`      | Dictionary file path for dictionary attack      | -             |          |
| `--max-length` | `-ml`     | Maximum length for brute-force attack           | 4             |          |
| `--charset`    | `-c`      | Charset for brute-force attack                  | alphanumeric  |          |

- One of the two is required: `--hash` or `--hash-file`

## Logging

Logs are written to the console. You can modify the logging level in the code if you need to adjust the verbosity of the output.

## Contact

- Pascal Nehlsen - [LinkedIn](https://www.linkedin.com/in/pascal-nehlsen) - [mail@pascal-nehlsen.de](mailto:mail@pascal-nehlsen.de)
- Project Link: [https://github.com/PascalNehlsen/dso-python-tasks/tree/main/module-5/hashcat](https://github.com/PascalNehlsen/dso-python-tasks/tree/main/module-5/hashcat)

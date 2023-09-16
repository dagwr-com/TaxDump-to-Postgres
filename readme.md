# NCBI TaxDump to Postgres Database Importer

## Overview

This tool facilitates the importation of data from NCBI TaxDump files into a Postgres database, enabling easier querying and analysis of GenBank taxonomy database information.

An attempt to build an NCBI to Postgres Importer using ChatGPT. [View conversation](https://chat.openai.com/share/df9a0853-af9f-4b27-ac40-0b60a6cd7432).

## Strategy

I start by asking GPT to not reply with anything other than "understood" until I give an "execute" command. This gives me time to build up context and consider after each message if I am confident yet.

---

## Features

- **Programmic Download:** Interactively choose the dump file to import or set it via command line arguments.
- **CLI Interface:** Interactively choose the dump file to import or set it via command line arguments.
- **Data Type Casting:** Automatically casts fields to the correct data types before database insertion.
- **Database Table Creation:** Quickly set up your database with the necessary tables using the `--create-tables` flag.
- **Flexible File Path:** Set a custom file path for the dump files, with a default path of `./taxdump`.

## Installation

(Describe the steps needed to install your software, including any prerequisites such as Python version, Postgres version, etc.)

## Usage

After installation (clone and pip), you can run the tool with the following command:

### Download
```
python download_taxdump.py
```

### NCBI Import
```
python ncbi_import.py
python ncbi_import.py --create-tables
python ncbi_import.py --path ./taxdump --file-choice 1
```

### Arguments

`--create-tables`: Create the necessary database tables before importing.
`--path`: Specify the path to the taxdump files (default: ./taxdump).
`--file-choice`: Specify which file to import (choices from '1' to '8', corresponding to different .dmp files).


### Interactive Mode

When run without arguments, the tool operates in interactive mode, prompting the user to make choices through a series of command line prompts.

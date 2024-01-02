# get_bibtex.py

This is a Python program that can be used to find BibTeX information through crossref and copy the entry to the clipboard.

## Setup

1. Ensure you have Python 3 installed on your machine. You can download it from [here](https://www.python.org/downloads/).
2. Clone this repository to your local machine.
3. Copy the `get_bibtex.py` file to some directory in your `PATH`.

## Requirements

This program requires the following Python packages:

- requests
- json
- sys
- argparse
- re
- pyperclip

You can install these packages using pip:

```bash
pip install requests json sys argparse re pyperclip
```

## Help

You can get a list of all the command-line arguments by running the script with the `-h` or `--help` option:

```bash
get_bibtex.py -h
```

## Basic Usage

Here are some examples of how to use this program:

- Search for works by author 'John Doe' and print the top 20 matches:

```bash
get_bibtex.py -a 'John Doe'
```

- Specify some keywords from the title of the paper to search for:

```bash
get_bibtex.py -a 'John Doe' -k 'machine learning'
```

- Change the number of matches to show (for example, 10):

```bash
get_bibtex.py -a 'John Doe' -k 'machine learning' -m 10
```

- Use the `-c` argument to save the BibTeX entry to the clipboard:

```bash
get_bibtex.py -a 'John Doe' -k 'machine learning' -m 10 -c
```

- Already know which match you want (e.g. the second)? Select that match and only get the BibTeX entry:

```bash
get_bibtex.py -a 'John Doe' -k 'machine learning' -m 10 -c -s 2
```

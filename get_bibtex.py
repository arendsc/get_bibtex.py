#!/bin/python3

# get_bibtex.py - A command-line-based program to fetch BibTeX entries.
# Copyright (C) 2024 Christian Arends

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
import json
import sys
import argparse
import re
import pyperclip

USAGE_EXAMPLES = f"""
Examples:
---------
    Search for works by author 'John Doe' and print the top 20 matches:
    {sys.argv[0]} -a 'John Doe'
    Then you can choose a match and save the BibTeX entry to the clipboard.

    Specify some keywords from the title of the paper to search for:
    {sys.argv[0]} -a 'John Doe' -k 'machine learning'

    Change the number of matches to show (for example, 10):
    {sys.argv[0]} -a 'John Doe' -k 'machine learning' -m 10

    Use the -c argument to save the BibTeX entry to the clipboard:
    {sys.argv[0]} -a 'John Doe' -k 'machine learning' -m 10 -c

    Already know which match you want (e.g. the second)? Select that match and only get the BibTeX entry:
    {sys.argv[0]} -a 'John Doe' -k 'machine learning' -m 10 -c -s 2
"""

def get_bibtex_crossref(doi, clipboard=False):
    # Create the query string
    query = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"

    # Send the GET request
    response = requests.get(query)

    # Check if the request was successful
    if response.status_code == 200:
        bibtex = response.content.decode('utf-8')

        # Add newlines before each field
        bibtex = re.sub(r',(?=\s*\w+\s*=)', ',\n  ', bibtex)

        # Copy the BibTeX entry to the clipboard if clipboard is True
        if clipboard:
            pyperclip.copy(bibtex)
            print("\nThe following BibTeX entry has been copied to the clipboard:\n\n" + bibtex)
        else:
            print("\n" + bibtex)

        # Return the BibTeX entry
        return bibtex
    else:
        print("An error occurred.")
        return None

def get_doi(author_name, keywords=None, num_matches=20, clipboard=False, select=None):
    # Replace spaces with "+"
    author = author_name.replace(" ", "+")

    # Create the query string
    query = f"https://api.crossref.org/works?query.author={author}"
    if keywords:
        query += f"&query.title={keywords}"

    # Send the GET request
    response = requests.get(query)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Get the top matches
        matches = data['message']['items'][:num_matches]

        if select:
            choice = select - 1
        else:
            # Print the matches and ask the user to choose one
            for i, match in enumerate(matches, start=1):
                authors = [f"{a['given']} {a['family']}" for a in match['author']]
                pub_date = match.get('created', {}).get('date-time', 'Unknown')
                update_date = match.get('updated', {}).get('date-time', 'Unknown')
                print(f"{i}\n-\nAuthors: {authors}\nTitle: {match['title'][0]}\nPublished: {pub_date}\nUpdated: {update_date}\nDOI: {match['DOI']}\n")

            try:
                choice = int(input(f"Choose a match (1-{num_matches}): ")) - 1
            except ValueError:
                print("Invalid input. Please enter a number.")
                return None

        if choice not in range(num_matches):
            print(f"Invalid choice. Please enter a number between 1 and {num_matches}.")
            return None

        # Get the BibTeX entry for the chosen match
        return get_bibtex_crossref(matches[choice]['DOI'], clipboard)
    else:
        print("An error occurred.")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog=USAGE_EXAMPLES, description='Get BibTeX information.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-a', '--author', default="", help="""specifies (parts of) the author's names""")
    parser.add_argument('-k', '--keywords', help="""specifies some keywords from the title of the paper to search for""")
    parser.add_argument('-m', '--num_matches', type=int, default=20, help="""specifies the number of matches to show (default: 20)""")
    parser.add_argument('-c', '--clipboard', action='store_true', help="""if this argument is included, the BibTeX entry will be copied to the clipboard""")
    parser.add_argument('-s', '--select', type=int, help="""specifies the match to select; if not given, the script will ask the user to choose a match""")

    args = parser.parse_args()

    get_doi(args.author, args.keywords, args.num_matches, args.clipboard, args.select)

# Python Book Picker 📚

This CLI tool is for randomly picking a book to read next from a Goodreads.com 'to-read' list.

## Usage

1. Open Goodreads.com and go to your 'to-read' shelf.
2. Copy the entire URL (incl. https://)
3. Paste the URL into the program ('Ctrl' + 'Shift' = 'S' on most terminals).
4. Select 'y' for the program to randomly pick a book.
5. If unhappy with the choice (ie. book is part of a series not yet started), select 'y' to re-roll the pick.

## Info

- Project manager: 'uv'
- Web Requests: 'requests'
- HTML Parser: 'BeautifulSoup4'
- Random Pick: 'random.choice()'

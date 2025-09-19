import random
import sys
import requests
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def scrape_all_pages(base_url):
    """Scrape all pages if pagination exists"""
    all_books = []
    page = 1

    while True:
        if '?' in base_url:
            url = f"{base_url}&page={page}"
        else:
            url = f"{base_url}?page={page}"

        print(f"Scraping page {page}: {url}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            book_links = soup.find_all('a', title=True, href=lambda x: x and '/book/show/' in x)

            if not book_links:
                print(f"No more books found on page {page}")
                break

            page_books = []
            for link in book_links:
                title_text = link.get_text(strip=True)
                if title_text and title_text not in [book['title'] for book in all_books]:
                    page_books.append({
                        'title': title_text,
                        'url': link.get('href'),
                        'full_title': link.get('title', '').strip()
                    })

            if not page_books:
                print(f"No new books found on page {page}")
                break

            all_books.extend(page_books)
            print(f"Found {len(page_books)} books on page {page}")

            page += 1
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f'Error on page {page}: {e}')
            break

    return all_books


def main():
    print("python-book-picker")
    url = input("Please add your goodreads url: ")

    all_books = scrape_all_pages(url)

    if all_books:
        print(30 * '#')
        print(f"\nFound {len(all_books)} books in total.")
        # print("-" * 50)
        # for i, book in enumerate(all_books, 1):
        #     print(f"{i}. {book['title']}")
    else:
        print("No books found. Trying single page scrape...")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            print('Request successful')

            soup = BeautifulSoup(response.content, 'html.parser')
            book_links = soup.find_all('a', title=True, href=lambda x: x and '/book/show/' in x)

            if book_links:
                print(f"Found {len(book_links)} book title links on single page")
                for i, link in enumerate(book_links, 1):
                    title_text = link.get_text(strip=True)
                    print(f"{i}. {title_text}")
            else:
                print("No book titles found.")

        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')

    print(30 * '#')
    while True:
        print('Do you want to randomly pick a book to read next?')
        choice = input('y = yes / n = no (quit) > ')
        if choice == 'n':
            sys.exit()
        else:
            print('Randomly picked book:')
            picked_book = random.choice(all_books)
            print(30 * '-')
            print(picked_book['title'])
            print(30 * '-')

        print('Re-roll?')
        choice2 = input('y = yes / n = no (quit) > ')
        if choice2 == 'n':
            sys.exit()
        else:
            print('Randomly picked book:')
            picked_book = random.choice(all_books)
            print(30 * '-')
            print(picked_book['title'])
            print(30 * '-')

if __name__ == "__main__":
    main()

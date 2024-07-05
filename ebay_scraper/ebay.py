import argparse
import requests
import json
import csv
from bs4 import BeautifulSoup

def parse_numeric_value(text, keep_decimal=False):
    """ Extracts and returns the first numeric value found in the input text. """
    result = ''.join([c for c in text if c.isdigit() or (keep_decimal and c == '.')])
    return float(result) if keep_decimal else int(result) if result else None

def parse_items_sold(text):
    return parse_numeric_value(text) if 'sold' in text else None

def parse_price(text):
    return parse_numeric_value(text.replace('$', '').split()[0], keep_decimal=True) * 100 if text.startswith('$') else None

def parse_shipping(text):
    return parse_numeric_value(text[1:], keep_decimal=True) * 100 if text.startswith('+') else 0

def fetch_page_items(search_term, page_number):
    url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={search_term}&_sacat=0&LH_TitleDesc=0&_pgn={page_number}&rt=nc"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.select('.s-item')[1:]

def extract_item_details(tag_item):
    item = {
        'name': tag_item.select_one('.s-item__title').text if tag_item.select_one('.s-item__title') else None,
        'price': parse_price(tag_item.select_one('.s-item__price').text if tag_item.select_one('.s-item__price') else ''),
        'status': tag_item.select_one('.SECONDARY_INFO').text if tag_item.select_one('.SECONDARY_INFO') else None,
        'shipping': parse_shipping(tag_item.select_one('.s-item__shipping, .s-item__freeXDays').text if tag_item.select_one('.s-item__shipping, .s-item__freeXDays') else ''),
        'free_returns': bool(tag_item.select('.s-item__free-returns')),
        'items_sold': parse_items_sold(tag_item.select_one('.s-item__hotness, .s-item__additionalItemHotness').text if tag_item.select_one('.s-item__hotness, .s-item__additionalItemHotness') else '0')
    }
    return item

def write_to_file(items, filename, format_type):
    with open(f"{filename}.{format_type}", 'w', encoding='utf-8') as file:
        if format_type == 'csv':
            writer = csv.DictWriter(file, fieldnames=items[0].keys())
            writer.writeheader()
            writer.writerows(items)
        else:
            file.write(json.dumps(items, indent=4))

def main(search_term, num_pages, output_format):
    items = []
    for page_number in range(1, num_pages + 1):
        print(f"Starting page {page_number}")
        page_items = fetch_page_items(search_term, page_number)
        for tag_item in page_items:
            item_details = extract_item_details(tag_item)
            items.append(item_details)

    write_to_file(items, search_term, 'csv' if output_format else 'json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('search_term', help="Search term for eBay")
    parser.add_argument('--num_pages', default=10, type=int, help="Number of pages to scrape")
    parser.add_argument('--csv', action='store_true', help="Output in CSV format")
    args = parser.parse_args()
    main(args.search_term, args.num_pages, args.csv)

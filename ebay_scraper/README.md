# eBay Listing Scraper

## Overview
This Python script scrapes eBay to collect data on listings based on a search term provided by the user. The data includes details such as item name, price, shipping cost, sale status, and whether the item has free returns. The script outputs this data in either JSON or CSV format.

## Features
- Scrape eBay listings based on a user-specified search term.
- Output the data in a structured format (JSON or CSV).
- Handle multiple pages of eBay listings.
- Easy to use with command-line arguments for various configurations.

## Requirements
- Python 3.x
- Libraries: `requests`, `bs4` (BeautifulSoup)

## Installation
First, ensure Python 3.x is installed on your system. You can then install the required Python libraries using pip:
```bash
pip install requests beautifulsoup4
```

## Usage
Run the script from the command line, specifying the search term and optionally the number of pages to scrape and the output format.

### Basic Command
```bash
python ebay_scraper.py "search term"
```

### Optional

--num_pages: Specifies the number of pages to scrape (default is 10) \
--csv: Outputs the data in CSV format. If not specified, the data will be in JSON format.
# WebScraper Overview:

- Web scraper built using BeautifulSoup and requests library.
- Caching implemented for space optimization.
- Multithreading implemented for time optimization.
- Also compared the results of multithreading and multiprocessing

# About the WebScraper:

The scraper gets an input from the user for a site and then gets all the necessary data in specified HTML tags from all the sites present in the sitemap of that website.

# Multithreading

Multithreading was used to reduce the scraping time.

# Caching

Once a site has been scraped the data is stored as a cache file. If the user requests to scrape that site again within a timespan of one day then the data in the cache file is directly displayed to the user in a tabular format in an HTML file using the pandas library with all the HTML tags and their data otherwise if it has been more than one day the site is scraped again.
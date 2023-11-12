# Overview

This software is a Python-based web scraper designed for extracting text from biblehub.com. Its primary function is to scrape different interpretations and translations of specific Bible chapters, starting with a focus on Isaiah 10. The core objective is to assist in translation analysis, especially useful for scholars studying biblical texts in original languages like Hebrew and Greek.

The motivation behind this software is to provide an efficient and automated method for collecting biblical texts in various translations. This tool is particularly useful for researchers and students who require an in-depth comparative study of biblical passages.

[Software Demo Video](https://youtu.be/TvM8HcwIFCE)

# Development Environment

The development of this software was carried out using Python, a versatile and widely-used programming language well-suited for web scraping tasks. The key libraries utilized in this project include:

- Requests: For handling HTTP requests to access the web pages.
- BeautifulSoup: For parsing HTML content and extracting necessary data.
- csv: For writing the scraped data into a CSV file format, making it easy to view and analyze the data.

The software development was done in the Visual Studio Code, an IDE that supports Python, ensuring efficient coding and debugging.

# Useful Websites

- [ChatGPT](https://chat.openai.com): Provided valuable guidance and troubleshooting tips for Python and web scraping techniques.
- [Python Requests](https://docs.python-requests.org/en/latest/): Official documentation for the Requests library.
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Comprehensive guide and reference for BeautifulSoup.

# Future Work

- Compare Greek versions of the Septuagint
- Scrape multiple chapters without getting banned by rate limiting
- Figure out site's rate limiting properties
- Fix spacing issues between some words that occurs rarely

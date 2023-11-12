from bs4 import BeautifulSoup
import csv
import requests
import threading
import tkinter as tk
from tkinter import font, messagebox

## GLOBALS ##
TRANSALTIONS = ['NIV', 'ESV', 'NASB', 'KJV', 'HCSB']
HEADER = ['Verse Number'] + TRANSALTIONS

def scrape_bible(book: str, chapter: int):
    filename = f'{book.lower()}_{chapter}.csv'

    # Use a BibleHub parallel url here or it will not work
    url = f'https://biblehub.com/parallel/{book.lower()}/{chapter}.htm'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.ok:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the verse rows
        rows = soup.find_all('tr')

        # Open a CSV file to write the verses in
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write the header row with the version names
            writer.writerow(HEADER)
            
            # Loop through each row (verse) and extract text from each version
            for row in rows:
                tds = row.find_all('td')
                if not tds:
                    continue

                # reftext class in tr/td/span should hold verse number
                verse_number = tds[0].find('span', class_='reftext').get_text(strip=True) if tds[0].find('span', class_='reftext') else ''
                if not verse_number:
                    continue

                verse_texts = [verse_number]

                # btext[1-5] classes in tr/td/span should hold the text for each of the 5 translations
                for td in tds:
                    text_span = td.find('span', class_=lambda x: x and x.startswith('btext'))
                    verse_text = text_span.get_text(strip=True) if text_span else ''
                    verse_texts.append(verse_text)

                # Ensure the length of verse_texts matches the number of columns in the header
                if len(verse_texts) == len(HEADER): 
                    writer.writerow(verse_texts)

        messagebox.showinfo("Success", f"File {filename} has been created successfully.")
    else:
        messagebox.showerror("Error", "Failed to retrieve the webpage")

def start_scrape():
    book = book_entry.get()
    chapter = chapter_entry.get()

    if not book or not chapter:
        messagebox.showwarning("Warning", "Please enter both book and chapter.")
        return
    
    threading.Thread(target=scrape_bible, args=(book, chapter)).start()

# Create the main window
root = tk.Tk()
root.title("Bible Scraper")
root.geometry("500x300")  # Adjust the size as needed
root.configure(bg='#f0f0f0')  # Light grey background

# Custom font
labelFont = font.Font(family="Arial", size=12)
entryFont = font.Font(family="Arial", size=10)
buttonFont = font.Font(family="Arial", size=10, weight="bold")

# Title label
title_label = tk.Label(root, text="Bible Version Scraper", bg='#f0f0f0', font=font.Font(family="Arial", size=16, weight="bold"))
title_label.pack(pady=(20, 10))

# Instructions label
instructions_label = tk.Label(root, text="Enter the Book and Chapter to scrape:", bg='#f0f0f0', font=labelFont)
instructions_label.pack(pady=(0, 10))

# Input frame
input_frame = tk.Frame(root, bg='#f0f0f0', padx=20, pady=20)
input_frame.pack()

# Book Entry
tk.Label(input_frame, text="Book:", bg='#f0f0f0', font=labelFont).grid(row=0, column=0, sticky="e", padx=(0,10))
book_entry = tk.Entry(input_frame, font=entryFont)
book_entry.grid(row=0, column=1, sticky="ew")

# Chapter Entry
tk.Label(input_frame, text="Chapter:", bg='#f0f0f0', font=labelFont).grid(row=1, column=0, sticky="e", padx=(0,10))
chapter_entry = tk.Entry(input_frame, font=entryFont)
chapter_entry.grid(row=1, column=1, sticky="ew")

# Scrape button
scrape_button = tk.Button(root, text="Scrape", command=start_scrape, font=buttonFont, bg='#0078D7', fg='white')
scrape_button.pack(pady=20)

# Make the input frame column expandable
input_frame.columnconfigure(1, weight=1)

# Run the GUI
root.mainloop()
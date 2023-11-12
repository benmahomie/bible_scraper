from bs4 import BeautifulSoup
import csv
import re
import requests
import threading
import tkinter as tk
from tkinter import font, messagebox

## GLOBALS ##
# Swete's Septuagint
TRANSALTIONS = ['SweteLXX']
HEADER = TRANSALTIONS

def split_on_integers(text):
    # Find all occurrences of one or more digits
    integers = re.findall(r'\d+', text)

    # Split the text at each integer
    split_text = re.split(r'\d+', text)
    split_text.pop(0)

    # Optionally, re-insert the integers into the split results
    result = []
    for i in range(len(split_text)):
        result.append(f'{integers[i]} {split_text[i]}')

    return result

def scrape_bible(book: str, chapter: int):
    filename = f'{TRANSALTIONS[0]}_{book.lower()}_{chapter}.csv'

    # Use a BibleHub parallel url here or it will not work
    url = f'https://biblehub.com/sepd/{book.lower()}/{chapter}.htm'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.ok:
        # Parse the HTML content
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the container that holds the verses
        leftbox = soup.find('div', id='leftbox')
        if not leftbox:
            print("Failed to find the text container.")
            return
        
        # Extracting verses from the specified structure
        verses = leftbox.find_all('div', class_='chap')

        # Open a CSV file to write the verses in
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write the header row with the version names
            writer.writerow(HEADER)
            
            for verse_div in verses:
                for p_tag in verse_div.find_all('p', class_='reg'):
                    # Extracting verse number and text
                    verse_text = p_tag.get_text(strip=True)
                    verses_by_number = split_on_integers(verse_text)

                    for verse in verses_by_number:
                        # Writing to CSV
                        cleaned_verse = verse.replace('"', '')
                        writer.writerow([cleaned_verse])

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
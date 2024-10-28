# Game-Data-Scraping-and-Analysis

This project consists of three Python scripts that demonstrate data scraping and analysis techniques, with the results stored in an Excel file. The project is divided into three parts, each with a specific purpose related to data collection and processing.

## Project Overview

### Part A - Basic Scraping
The script `main.py` is responsible for:
- Collecting information from a selected website, such as game titles, prices, release dates, and content categories.
- Displaying the scraped data from the main page of the website.

### Part B - Data Analysis and Storage
The script `main2.py` performs the following actions:
- Saves the scraped data in an Excel file using the Pandas library.
- Analyzes the data, displaying the percentage of null values.
- Creates and shows a scatter plot to visualize specific aspects of the data.

### Part C - Advanced Scraping with External Libraries
The script `main3.py` repeats the scraping process from Part A but without the original limitations. This part incorporates additional external libraries for more robust data collection.

## Project Structure

- `main.py` - Script for Part A: Basic data scraping and display.
- `main2.py` - Script for Part B: Data analysis, saving to Excel, and plotting.
- `main3.py` - Script for Part C: Advanced data scraping.
- `pandas_to_excel.xlsx` - Excel file containing the collected data.


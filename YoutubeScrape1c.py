import time
from selenium import webdriver
from bs4 import BeautifulSoup
import xlsxwriter
import pandas as pd
from selenium.webdriver.chrome.service import Service

# List of YouTube URLs
urls = [
    'https://www.youtube.com/@ApnaCollegeOfficial'
]

# Initialize lists to store data
t = []
v = []
d = []

# Initialize Chrome driver using the Service class
# chrome_driver_path = "C:/Users/Praveshika/OneDrive/Praveshika/chromedriver.exe"
chrome_driver_path = "C:/Users/Praveshika/OneDrive/Praveshika/chromedriver-win32/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Loop through each URL
for url in urls:
    times = 0  # Reset scroll counter for each URL
    driver.get(f'{url}/videos?view=0&sort=p&flow=grid')

    # Scroll the page 5 times to load more videos
    while times < 5:
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        times += 1

    # Get page source after scrolling
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'lxml')

    # Extract video titles
    titles = soup.findAll('a', id='video-title')
    for i in titles:
        t.append(i.text.strip())  # Strip extra spaces

    # Extract video views
    views = soup.findAll('span', class_='style-scope ytd-grid-video-renderer')
    count = 0
    for i in range(len(views)):
        if i % 2 == 0:  # Views are present at every alternate index
            v.append(views[i].text.strip())
        else:
            continue

    # Extract video durations
    duration = soup.findAll('span', class_='style-scope ytd-thumbnail-overlay-time-status-renderer')
    for i in duration:
        d.append(i.text.strip())

# Save data to Excel file
workbook = xlsxwriter.Workbook('file.xlsx')
worksheet = workbook.add_worksheet()

# Write headers
worksheet.write(0, 0, "Title")
worksheet.write(0, 1, "Views")
worksheet.write(0, 2, "Duration")

# Write data to worksheet
row = 1
for title, view, dura in zip(t, v, d):
    worksheet.write(row, 0, title)
    worksheet.write(row, 1, view)
    worksheet.write(row, 2, dura)
    row += 1

workbook.close()

# Load data into pandas and display the first few rows
data = pd.read_excel('file.xlsx')
print(data.head())

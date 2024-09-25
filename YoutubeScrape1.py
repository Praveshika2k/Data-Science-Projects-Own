import time 
from selenium import webdriver 
from bs4 import BeautifulSoup 
import xlsxwriter
import pandas as pd 

urls = [ 
    'https://www.youtube.com/@ApnaCollegeOfficial'
]
times = 0
row = 0
t = v = d = [] 
driver = webdriver.Chrome(executable_path="C:/Users/Praveshika/OneDrive/Praveshika/chromedriver.exe") 
for url in urls: 
	driver.get('{}/videos?view=0&sort=p&flow=grid'.format(url)) 
	while times < 5: 
		time.sleep(1) 
		driver.execute_script( 
			"window.scrollTo(0, document.documentElement.scrollHeight);") 
		times += 1
	content = driver.page_source.encode('utf-8').strip() 
	soup = BeautifulSoup(content, 'lxml')

#Title 
titles = soup.findAll('a', id='video-title') 
t =[] 
for i in titles: 
	t.append(i.text) 

#Views 
views = soup.findAll('span', class_='style-scope ytd-grid-video-renderer') 
v = [] 
count = 0
for i in range(len(views)): 
	if i%2 == 0: 
		v.append(views[i].text) 
	else: 
		continue

#Duration 
duration = soup.findAll( 
	'span', class_='style-scope ytd-thumbnail-overlay-time-status-renderer') 
d = [] 
for i in duration: 
	d.append(i.text) 
	
workbook = xlsxwriter.Workbook('file.xlsx') 
worksheet = workbook.add_worksheet() 

worksheet.write(0, 0, "Title") 
worksheet.write(0, 1, "Views") 
worksheet.write(0, 2, "Duration") 

row = 1
for title, view, dura in zip(t,v,d): 
	worksheet.write(row, 0, title) 
	worksheet.write(row, 1, view) 
	worksheet.write(row, 2, dura) 
	row += 1
workbook.close()
data = pd.read_excel('file.xlsx') 
data.head()

# data['Views'] = data['Views'].str.replace(" views","") 

# new = [] 

# for i in data['Views']: 
# 	if(i.endswith('K')): 
# 		i = i.replace('K','') 
# 		new.append(float(i) * 1000) 
# 	else : 
# 		new.append(i) 

# data['Views'] = new

# #Duration column cleaning 
# data['Duration'] = data['Duration'].str.replace("\n","") 

# new2 = [] 

# for i in data['Duration']: 
# 	if(i=='SHORTS' or len(i.split(':'))==1): 
# 		new2.append(i) 
# 	elif(len(i.split(':'))==2): 
# 		i = i.split(':') 
# 		tim = int(i[0])*60 + int(i[1]) 
# 		new2.append(tim) 
# 	elif(len(i.split(':'))==3): 
# 		i = i.split(':') 
# 		tim = int(i[0])*3600 + int(i[1])*60 + int(i[2]) 
# 		new2.append(tim) 
		
# data['Duration'] = new2

# #Duration column categorization 
# for i in data['Duration'].index: 
# 	val = data['Duration'].iloc[i] 
# 	if(val==' SHORTS'): 
# 		continue
# 	elif(val in range(0,900)): 
# 		data.loc[i,'Duration'] = 'Mini-Videos'
# 	elif(val in range(901,3600)): 
# 		data.loc[i,'Duration'] = 'Long-Videos'
# 	else: 
# 		data.loc[i,'Duration'] = 'Very-Long-Videos'

# data.head()



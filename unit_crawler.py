from bs4 import BeautifulSoup as soup
import requests


current_year = '2025'
unit_search_url = f"https://handbook.deakin.edu.au/courses-search/unit-search.php?hidCurrentYear={current_year}&hidYear={current_year}&hidType=min&txtUnit=&txtTitle=+&txtKeyword=&selLevel=Select&selSemester=Select&selMode=Select&selLocation=Select&chkSortby=unit_cd&btnSubmit="
unit_url = "https://handbook.deakin.edu.au/courses-search/{href}"

# Get unit list
r = requests.get(unit_search_url)
unit_search_page = soup(r.content, 'html5lib')
table = unit_search_page.find(lambda tag: tag.name=='fieldset') 
rows = table.findAll(lambda tag: tag.name=='tr')

unit_data = []
for i in range(1, len(rows)):
    row_data = {}
    row_text = [data for data in rows[i].text.replace('\n', '  ').split('  ') if data not in ['', ' ']]
    row_data['unit_code'] = row_text[0]
    row_data['unit_title'] = row_text[1]
    href = rows[i].a['href']
    row_data['unit_link'] = unit_url.format(href=href)
    unit_data.append(row_data)
    
# Get unit content
for i in range(len(unit_data)):
    unit_link = unit_data[i]['unit_link']
    r = requests.get(unit_link)
    unit_page = soup(r.content, 'html5lib')
    
    content = ""
    for heading in unit_page.find_all("h3"):
        if heading.text not in ['Content', 'Learning outcomes']:
            break
        for sibling in heading.find_next_siblings():
            if sibling.name == "h3":
                break
            content = content + sibling.text
    content = ' '.join(content.split())
    unit_data[i]['unit_content'] = content
    
# Save the data to txt
txt = ''
for unit in unit_data:
    txt += f"Unit code: {unit['unit_code']}\n"
    txt += f"Unit title: {unit['unit_title']}\n"
    txt += f"Unit content: {unit['unit_content']}\n"
    txt += f"Unit link: {unit['unit_link']}\n\n"

with open('unit_data.txt', 'w') as file:
    file.write(txt)
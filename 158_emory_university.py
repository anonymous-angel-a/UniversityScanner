import requests
import urllib.request
import time
import urllib
import re
import csv
import sys
from bs4 import BeautifulSoup
import requests
from os.path  import basename
import pytesseract
from PIL import Image

def emory_university():
    url = "https://www.cs.emory.edu/people/faculty/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    r = requests.get(url, headers=headers)

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html5lib")
    # print(soup.prettify)

    # file initialization to write
    file_name = sys.argv[0]
    # file_name = file_name[4:]

    txt_file = file_name.replace(".py", ".txt")
    f = open(txt_file, "w")

    csv_file = file_name.replace(".py", ".csv")
    f2 = open(csv_file, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "Emory University"
    country = "USA"

    grabage_emails = []

    var = [f, csvwriter, csvwriter2, u_name, country, grabage_emails]

    # d gives the array of all profs on the dept homepage
    dd = soup.find('div', {'class':"span9"})
    d = dd.find_all('tr')
    # print(len(d))

    #iterating for every prof
    for i in d:
        td = i.find('td')
        if td == None:
            continue
        a = td.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        name = " ".join(name.split())
        link = "https://www.cs.emory.edu/people/faculty/"+a.get('href')

        # print(name, link)
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link, headers=headers)   
        except:
            continue

        email = "Not Found"

        print(name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)



    f.close()
    f2.close()
    f3.close()
    print("Finished")

def GET_Email_FROM_PIC(site):
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    tag1 = soup.find('b',string="Email")
    tag2= tag1.find_next('img')
    image_url = tag2.get("src")
    r=requests.get(site+image_url)
    data = image_url
    response = urllib.request.urlopen(data)
    with open('image.jpg', 'wb') as f:
        f.write(response.file.read())

    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image_path = r"image.jpg"
    
    # Opening the image & storing it in an image object
    img = Image.open(image_path)

    # Providing the tesseract executable
    # location to pytesseract library
    pytesseract.tesseract_cmd = path_to_tesseract
    
    # Passing the image object to image_to_string() function
    # This function will extract the text from the image
    text = pytesseract.image_to_string(img)
  
# Displaying the extracted text
    return text[:-1]

def filterandgetEmail(var, grabage_emails, name, link, email, prof_resp):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    keyword_list = ['Computer Architecture','hardware and system architecture', 'hardware and architecture', 'Computerarchitectuur', 'embedded system', 'computer organization','VLSI Design', 'Computer and System',
                    'multiprocessor architecture']
    flag = 1
    prof_soup = BeautifulSoup(prof_resp.text, "html.parser")
    # print(prof_soup)
    research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern, research_text, re.IGNORECASE):
            flag = 0
            if email != 'Not Found':
                f.write(link + '\n' + name + "\t"+ email + "\n")
                csvwriter.writerow([u_name, country, name, email, link])
                csvwriter2.writerow([u_name, country, name, email, link])
            else:
                new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
                for eemail in grabage_emails:
                    if eemail in new_emails:
                        new_emails.remove(eemail)
                if len(new_emails) == 0:
                    email =GET_Email_FROM_PIC(link) 
                    f.write(link + '\n' + name + "\t"+ email + "\n")
                    csvwriter.writerow([u_name, country, name, email, link])
                    csvwriter2.writerow([u_name, country, name, email, link])
                else:
                    # f.write(link + '\n' + name)
                    for email in new_emails:
                        f.write(link + '\n' + name + '\t\t' + email + '\n')
                        csvwriter.writerow([u_name, country, name, email, link])
                        csvwriter2.writerow([u_name, country, name, email, link])
                    # f.write("\n") 
 

            f.write(pattern)
            f.write('\n\n')
            break

if __name__ == '__main__':
    emory_university()
     
import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def gadjahmada():
    url = "http://dcse.fmipa.ugm.ac.id/site/en/profil-pengajar/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    #print(r.text)
    #print(soup.get_text())
    
    # file initialization to write
    filename = "gadjah.txt"
    f = open(filename, "w", encoding='utf-8')

    excel_filename = "gadjah.csv"
    f2 = open(excel_filename, "w", encoding='utf-8')
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a", encoding='utf-8')
    csvwriter2 = csv.writer(f3)
    
    u_name = "Universitas Gadjah Mada"
    country = "Indonesia"
    garbage_emails = []
    var = [f, csvwriter, csvwriter2, u_name, country]

    
    d = soup.find_all('table')
    d=d[0].find_all('a')
    
    #print(d)
    b=0
    for i in d:
        
        #print(z)
        #print(a,z)
        if(i.get_text()=='Google Scholar Profile'):
            continue
        link = i.get('href')                # extracting prof page link
        #print(a.find('a'))
        name = i.get_text()                 # extracting prof name
        #print(link)
        #print(name)
        try:
            prof_resp = requests.get(link)      # requesting prof homepgae
        except:
            continue
        email = "Not Found"
        b=b+1
        
        print(name, email, link)
        filterandgetEmail(var, garbage_emails, name, link, email, prof_resp)


def filterandgetEmail(var, garbage_emails, name, link, email, prof_resp):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    keyword_list = ['Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded System','Computer Organization','VLSI', 'Computer and System','Distributed System', 'distributed system', 'Distributed system' ]
    #keyword_list = ['computer architecture', 'Computer architecture', 'Embedded System', 'Embedded system', 'embedded system']   # 'Computer Architecture',
    flag = 1
    prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
    research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern,research_text):
            flag = 0
            if email != 'Not Found':
                f.write(link + '\n' + name + "\t"+ email + "\n")
                csvwriter.writerow([u_name, country, name, email, link])
                csvwriter2.writerow([u_name, country, name, email, link])
            else:
                new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
                #print(new_emails)
                for eemail in garbage_emails:
                    if eemail in new_emails:
                        new_emails.remove(eemail)
                if len(new_emails) == 0:
                    email = "Email Not Found"
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
    #print("aa")
    gadjahmada()
    print("finish")
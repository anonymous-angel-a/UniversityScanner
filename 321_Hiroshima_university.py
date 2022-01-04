import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def oxford():
    url = "https://www.hiroshima-u.ac.jp/en/eng/research_and_staff"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    filename = "hiroshima.txt"
    f = open(filename, "w")

    excel_filename = "hiroshima.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "Hiroshima University"
    country = "Japan"

    garbage_emails = ['finance@cs.ox.ac.uk', 'enquiries@cs.ox.ac.uk']

    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find_all('table')
    dd = d[3]
    ddd = dd.find_all('tr')
    #dd = d.find_all('div', {'class': 'views-field views-field-title'})
    #print(dd)
    count =1
    #iterating for every prof
    for i in ddd:
        if count==1:
            count=count+1
            continue
        elif count==2:
            print("jdncjnjn")
            name = i.find('td').find_next('td').find_next('td').get_text()
            prof_soup=i.find('td').find_next('td').get_text()
            count =count+1

        else:
            prof_soup= i.find('td').get_text()
            name = i.find('td').find_next('td').get_text()                 # extracting prof name
        name = name.strip()
        a = i.find('a')      
        email=""
        if a!=None:
            email = a.get('href')
        print(name,email)
        filterandgetEmail(var, garbage_emails, name, prof_soup, email)


    f.close()
    f2.close()
    f3.close()
    print("Finished")





def filterandgetEmail(var, garbage_emails, name,prof_soup, email):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    keyword_list = ['Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 
                'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded System','Computer Organization','VLSI', 'Computer and System',
                'Distributed System', 'distributed system', 'Distributed system' ]
    flag = 1
    link="not available"
   # prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
    #research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern,prof_soup):
            print(prof_soup)
            flag = 0
            if email != 'Not Found':
                f.write(link + '\n' + name + "\t"+ email + "\n")
                csvwriter.writerow([u_name, country, name, email, link])
                csvwriter2.writerow([u_name, country, name, email, link])
            else:
                new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
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
    oxford()
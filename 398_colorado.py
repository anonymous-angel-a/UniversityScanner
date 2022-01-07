import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def colorado():
    url = "https://engineering.ucdenver.edu/computer-science-and-engineering/faculty-and-staff"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    filename = "colorado.txt"
    f = open(filename, "w")

    excel_filename = "colorado.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "University of Colorado Denver"
    country = "United States"

    garbage_emails = ['santana@seas.harvard.edu', 'gioia@seas.harvard.edu', 'jsalant@harvard.edu', 'jbourge@seas.harvard.edu']
    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all profs on the dept homepage
    # d = soup.find('a', {'class':"accordian-title"})
    
    dl = soup.find('div' , {'class': 't-list-widget people-list'})
    dd = dl.find_all('div')
    
    #iterating for every prof
    for i in dd:

            
        if i.find('h3', {'class':'people-display-name'})== None:
            continue                    # a contains the name and the homepage of prof
        a = i.find('h3', {'class':'people-display-name'}).get_text()
        a = a.split(",")
        name = a[0]
        email = i.find('a').get_text()
        aa = i.find_all('a')
        link = ''
        for j in aa:
            if j.get_text() == "Profile":
                link = j.get('href')
            if j.find('strong') != None:
                if j.find('strong').get_text() == "Website":
                    link =   j.get('href')
        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        # print(name, link)
        
        print(name,email, link)
        filterandgetEmail(var, garbage_emails, name, link, email, prof_resp)


    f.close()
    f2.close()
    f3.close()
    print("Finished")



def filterandgetEmail(var, garbage_emails, name, link, email, prof_resp):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    keyword_list = ['Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 
                'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded System','Computer Organization', 'Computer and System',
                'distributed system', 'Distributed System', 'Distributed system' ]
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
    colorado()
    

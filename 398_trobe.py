import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def trobe():
    url = "https://www.latrobe.edu.au/computer-science-and-information-technology/staff"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    filename = "trobe.txt"
    f = open(filename, "w")

    excel_filename = "trobe.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "La Trobe University"
    country = "Australia"

    garbage_emails = ['santana@seas.harvard.edu', 'gioia@seas.harvard.edu', 'jsalant@harvard.edu', 'jbourge@seas.harvard.edu']
    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all profs on the dept homepage
    # d = soup.find('a', {'class':"accordian-title"})
    
    d = soup.find('div',{'class':'row'})
    da = d.find_all('a')
    dl = []
    dd = []
    for i in da:
        if i.get_text().isdigit():
            dl.append(i.get('href'))
            #print(i.get('href'))
    
    for i in dl:
        r1 = requests.get(i)
        soup2 = BeautifulSoup(r1.text, "html.parser")
        d = soup2.find_all('div',{'class':'row'})
        for i in d:
            d1 = i.find_all('tr')
            dd.extend(d1)
    
    
    
    
	
    #iterating for every prof
    for i in dd:
        if i.find('a') == None:
            continue
        a = i.find('a')                     # a contains the name and the homepage of prof
        
        link = a.get('href')                # extracting prof page link
        name = a.get_text()                 # extracting prof name
        l = name.split()
        if len(l) == 3:
            name = l[1] + " " + l[2]
        td = i.find_all('td')
        email = td[3].get_text()
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
    trobe()
    

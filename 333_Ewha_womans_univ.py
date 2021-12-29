import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def ewha():
    url = "http://cms.ewha.ac.kr/user/indexSub.action?codyMenuSeq=2172651&siteId=cseeng&menuUIType=sub"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    filename = "EWHA.txt"
    f = open(filename, "w")

    excel_filename = "EWHA.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "Ewha Womans University"
    country = "South korea"

    garbage_emails = []

    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find('div', {'class':'htmlOuter'})
    dd = d.find_all('tbody')
   # print(dd)

    #iterating for every prof
    for i in dd:
        name1 = i.find('td')
        name = name1.find('p').get_text()
        #print(name)
        a = i.find('a') 
        email_1 = a.get_text()
        link = a.find_next('a').get('href')
       # print(email_1)
       # print(link)

       # email_1 =  a.get('href')                # a contains the name and the homepage of prof
       # link=  i.findnext('a')              # extracting prof page link
       # name = i.find('td')  
       # name = name_1.findnext('p')               # extracting prof name
        print(name, "\t", link)
       

        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(name, link)
        filterandgetEmail(var, garbage_emails, name, link, email, prof_resp,email_1)


    f.close()
    f2.close()
    f3.close()
    print("Finished")





def filterandgetEmail(var, garbage_emails, name, link, email, prof_resp,email_1):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    keyword_list = ['Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 
                'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded System','Computer Organization','VLSI', 'Computer and System',
                'Distributed System', 'distributed system', 'Distributed system' ]
    flag = 1
    prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
    research_text = prof_soup.text
    for pattern in keyword_list:
        if re.search(pattern,research_text):
            flag = 0
            if email != 'Not Found':
                f.write(link + '\n' + name + "\t"+ email_1+ "\n")
                csvwriter.writerow([u_name, country, name, email_1, link])
                csvwriter2.writerow([u_name, country, name, email_1, link])
            else:
                new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
                for eemail in garbage_emails:
                    if eemail in new_emails:
                        new_emails.remove(eemail)
                if len(new_emails) == 0:
                    email = "Email Not Found"
                    f.write(link + '\n' + name + "\t"+ email_1 + "\n")
                    csvwriter.writerow([u_name, country, name, email_1, link])
                    csvwriter2.writerow([u_name, country, name, email_1, link])
                else:
                    # f.write(link + '\n' + name)
                    for email in new_emails:
                        f.write(link + '\n' + name + '\t\t' + email_1 + '\n')
                        csvwriter.writerow([u_name, country, name, email_1, link])
                        csvwriter2.writerow([u_name, country, name, email_1, link])
                    # f.write("\n") 
 

            f.write(pattern)
            f.write('\n\n')
            break

if __name__ == '__main__':
    ewha()
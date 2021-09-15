import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def lund_university():
    url = "https://www.lunduniversity.lu.se/lucat/group/v1000234"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify)

    # file initialization to write
    filename = "lund_university.txt"
    f = open(filename, "w")

    excel_filename = "lund_university.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "Lund University"
    country = "Sweden"

    grabage_emails = ['expedition@cs.lth.se']

    var = [f, csvwriter, csvwriter2, u_name, country, grabage_emails]

    # d gives the array of all profs on the dept homepage
    # d = soup.find('a', {'class':"accordian-title"})
    dd = soup.find('div', {'class':'lucat-user-list mt-7 mb-7'})
    d = dd.find_all('li', {'class':'border-bottom mb-3 pb-3'})

    #iterating for every prof
    for i in d:
        h4 = i.find('h4')
        a = h4.find('a')
        if a == None:
            continue
        name = (a.get_text()).strip()
        link = 'https://www.lunduniversity.lu.se' +a.get('href')
        # check if link is valid on Not
        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        prof_soup = BeautifulSoup(prof_resp.text, "html.parser")

        #getting prof personal homepage from desc page
        prof_span = prof_soup.find('span', text=' Personal website:')
        if prof_span == None:
            continue
        a_prof = prof_span.find_next('a') 
        link = a_prof.get('href')

        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(name, link)
        filterandgetEmail(var, grabage_emails, name, link, email, prof_resp)

    f.close()
    f2.close()
    f3.close()
    print("Finished")





def filterandgetEmail(var, grabage_emails, name, link, email, prof_resp):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    keyword_list = ['Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 
                'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded system','Computer Organization','VLSI Design', 'Computer and System']
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
                for eemail in grabage_emails:
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
    lund_university()
    
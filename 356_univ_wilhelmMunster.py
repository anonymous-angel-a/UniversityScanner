import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def Munster():
    url = "https://www.uni-muenster.de/FB10/Service/listinst.shtml#top"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    filename = "munster.txt"
    f = open(filename, "w")

    excel_filename = "munster.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "Westfälische Wilhelms-Universität Münster"
    country = "Germany"

    garbage_emails = ['santana@seas.harvard.edu', 'gioia@seas.harvard.edu', 'jsalant@harvard.edu', 'jbourge@seas.harvard.edu']
    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all profs on the dept homepage
    # d = soup.find('a', {'class':"accordian-title"})
    d1 = soup.find_all('div' , {'class' : 'module-content'})
    dd = []
    for i in d1:
        d = i.find_all('tr')
        dd.extend(d)      

	
    #iterating for every prof
    for i in dd:
        if i.find('a') == None:
            continue        
        a = i.find_all('a')                     # a contains the name and the homepage of prof
        name = a[0].get_text()
        email = a[1].get_text()
        link = a[0].get('href')               # extracting prof page link
        
	
        # check if link is valid on not
        try:    
            p = requests.get(link)        
        except:
            continue
        soup2 = BeautifulSoup(p.text, "html.parser")
        a = soup2.find_all('a')
        prof_link = ""
        for i in a:
            if i.get('href') == i.get_text():
                prof_link = i.get_text()
        if prof_link == "":
            continue
        else:
            prof_resp = requests.get(prof_link)
            print(name, email,  prof_link)
            filterandgetEmail(var, garbage_emails, name, prof_link, email, prof_resp)


        # print(name, link)
        


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
    Munster()
    

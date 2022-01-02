import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def grifith():
    url = "https://www.griffith.edu.au/griffith-sciences/school-information-communication-technology/our-staff"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    filename = "griffith.txt"
    f = open(filename, "w")

    excel_filename = "griffith.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "Grifith University"
    country = "Australia"
    garbage_emails = []

    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all prof on the dept homepage
    d = soup.find('div',{"class":"slab puff primary trim-top"})
    dd=d.find_all('li')
   # print(d)
    
   ## print(d)
    #iterating for every prof
    for i in dd:
        a = i.find('a')  
        if a!=None:                   # a contains the name and the homepage of prof
            link =  a.get('href')                # extracting prof page link
            name = a.get_text()                 # extracting prof name
            name = name.strip()
        #print(name,link)

        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(name, link)
        filterandgetEmail(var, garbage_emails, name, link, email, prof_resp)

    f.write("https://experts.griffith.edu.au/9484-sven-venema"+'\n'+"Dr Sven Venema"+"\t"+"s.venema@griffith.edu.au"+"\n")
    csvwriter.writerow([u_name, country,"Dr Sven Venema", "s.venema@griffith.edu.au", "https://experts.griffith.edu.au/9484-sven-venema"]) 
    csvwriter2.writerow([u_name, country, "Dr Sven Venema","s.venema@griffith.edu.au","https://experts.griffith.edu.au/9484-sven-venema"])
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
                'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded System','Computer Organization','VLSI', 'Computer and System',
                'Distributed System', 'distributed system', 'Distributed system' ]
    flag = 1
    prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
    research_text = prof_soup.text
    #print(research_text)
    for pattern in keyword_list:
        ##print(pattern)
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
    grifith()
    #print("Griffith University-Access to read Web pages of Proffesors now given")
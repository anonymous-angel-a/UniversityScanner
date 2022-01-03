import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def oxford():
    url = "https://search.unisa.edu.au/s/search.html?f.Staff%7Cstaff1=academic&query=Computer+science&collection=people"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    filename = "univ_of_south_australia.txt"
    f = open(filename, "w")

    excel_filename = "univ_of_south_australia.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "University of South Australia"
    country = "Australia"

    garbage_emails = []

    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find('ol', {'id':'search-results'})
    dd = d.find_all('li')
    #print(dd)

    #iterating for every prof
    for i in dd:
        name1 = i.find('h3')
       # print(i)
      
        link1 = i.find(lambda tag:tag.name=="a" and "Staff Homepage" in tag.text)
        if link1!=None:
            link = "https://people.unisa.edu.au"+link1.get('href')
           # print(link)
        
        if type(name1)!=int and name1!=None:
            name = name1.get_text()
           # print(name)
            name = name.strip() 
            namearray = name.split()
           #print(namearray)
            
            
            link  ="https://people.unisa.edu.au/"+str(namearray[1])+"."+str(namearray[2] )


        
       # print(name,link)

        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(name, link)
        filterandgetEmail(var, garbage_emails, name, link, email, prof_resp)
    f.write(link + '\n' + "Professor Mahfuz Aziz" + "\t"+ email + "\n")
    csvwriter.writerow([u_name, country, "Professor Mahfuz Aziz", "Mahfuz.Aziz@unisa.edu.au","https://people.unisa.edu.au/Mahfuz.Aziz"])
    csvwriter2.writerow([u_name, country, "Professor Mahfuz Aziz","Mahfuz.Aziz@unisa.edu.au", "https://people.unisa.edu.au/Mahfuz.Aziz"]) 


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
    oxford()
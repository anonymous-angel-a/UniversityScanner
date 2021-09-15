import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup, element

def univ_tokyo():
   
    url = " https://sites.google.com/view/casys/"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    filename = "univ_tokyo.txt"
    f = open(filename, "w")

    excel_filename = "univ_tokyo.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "University of Tokyo"
    country = "Japan"

    garbage_emails = []
    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all profs on the dept homepage
    # d = soup.find('a', {'class':"accordian-title"})
    d = soup.find('section', {'id':"h.45c1229e9bb0144a_24"})
    dd = d.find_all('a')

    #print(d.text)
    #print("jcnj")

    #iterating for every prof
    for i in d:
        if i.find('a') == None:
            continue        
        a = i.find('a',{'class':"XqQF9c"})                     # a contains the name and the homepage of prof
        link = a.get('href')                # extracting prof page link
        name = a.get_text()   

        print(name, link)              # extracting prof name

        # check if link is valid on not
        try:    
            prof_resp = requests.get(link)    
        except:
            continue

        #print(name, link)
        email = "Not Found" 
        OnlygetEmail(var, garbage_emails, name, link, email, prof_resp)


    f.close()
    f2.close()
    f3.close()
    print("Finished")
def get_ac_type_email(site):
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    tag1 = soup.findAll('li',id ="h.p_3zDKFR19-4Tx") 
   # print(tag1[0])
    text = tag1[0].text
   # text =tag1.__str__
   # print(text)
    words = text.split()
    #print(words)
    return words[1]
   # return tag1.text



def OnlygetEmail(var, garbage_emails, name, link, email, prof_resp):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 
    element = prof_soup.find('meta',attrs={'http-equiv': 'refresh'})
    refresh_content = element['content']
    link= refresh_content.partition('=')[2]
    ##print(url)
    if email != 'Not Found':
        email = get_ac_type_email(link)
        print(email)
        f.write(link + '\n' + name + "\t"+ email + "\n")
        csvwriter.writerow([u_name, country, name, email, link])
        csvwriter2.writerow([u_name, country, name, email, link])
    else:
        new_emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", prof_resp.text))
        for eemail in garbage_emails:
            if eemail in new_emails:
                new_emails.remove(eemail)
        if len(new_emails) == 0:
            email = get_ac_type_email(link)
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


    f.write('\n\n')

if __name__ == '__main__':
    univ_tokyo()
    

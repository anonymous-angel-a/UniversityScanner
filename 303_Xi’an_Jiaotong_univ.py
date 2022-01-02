import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def Xian_Jiaotong_Univ():
    url = "https://www.researchgate.net/institution/Xian_Jiaotong_University/department/Institute_of_Computer_Architecture_and_Network/members"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    filename = "xian.txt"
    f = open(filename, "w")

    excel_filename = "xian.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "Xi’an_Jiaotong"
    country = "China"

    garbage_emails = []

    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all profs on the dept homepage
    d = soup.find('div', {'class':'nova-legacy-o-stack nova-legacy-o-stack--gutter-xl nova-legacy-o-stack--spacing-none nova-legacy-o-stack--show-divider nova-legacy-o-stack--no-gutter-outside'})
    dd = d.find_all('div', {'class': 'nova-legacy-v-person-list-item__align'})
   # print(d)
    #iterating for every prof
    for i in d:
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = "https://www.researchgate.net/" + a.get('href')                # extracting prof page link
        name = a.find_next('a').get_text()  
       # print(a)               # extracting prof name
        #print(name, "\t", link)
        name = name.strip()

        try:    
            prof_resp = requests.get(link)        
        except:
            continue

        email = "Not Found"
        print(name, link)
        OnlygetEmail(var, garbage_emails, name, link, email, prof_resp)


    f.close()
    f2.close()
    f3.close()
    print("Finished")





def OnlygetEmail(var, garbage_emails, name, link, email, prof_resp):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    prof_soup = BeautifulSoup(prof_resp.text, "html.parser") 

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


    f.write('\n\n')
if __name__ == '__main__':
    Xian_Jiaotong_Univ()
import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def harvard():
    #url1 = "https://www.rug.nl/about-ug/how-to-find-us/find-an-expert"   # homepage url
    #r1 = requests.get(url1)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    #soup1 = BeautifulSoup(r1.text, "html.parser")
    #d1 = soup1.find('a' , text = "Computer Science, Hardware & Architecture")  #get link to computer architecture
    #print(d1)
    #url = "https://www.rug.nl" + d1.get('href')
    url1 = "https://www.rug.nl/about-us/how-to-find-us/find-an-expert?discipline=Computer+Science%2C+Hardware+%26+Architecture"

    r1 = requests.get(url1)
    soup = BeautifulSoup(r1.text, "html.parser")


    # file initialization to write
    filename = "grogingen.txt"
    f = open(filename, "w")

    excel_filename = "grogingen.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "Grogingen"
    country = "Netherlands"

    garbage_emails = ['ppo@rug.nl']
    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all profs on the dept homepage
    # d = soup.find('a', {'class':"accordian-title"})
    #d1 = soup.find('a', text="computer science, hardware & architecture")
    dd = soup.find_all('div', {'class': 'rug-h3'})



    #iterating for every prof
    for i in dd:
        if i.find('a') == None:
            continue
        a = i.find('a')                     # a contains the name and the homepage of prof
        link = "https://www.rug.nl"+ a.get('href')                # extracting prof page link
        #name = a.get_text()                 # extracting prof name

        # check if link is valid on not
        try:
            prof_resp = requests.get(link)
        except:
            continue

        # print(name, link)
        prof_soup = BeautifulSoup(prof_resp.text, "html.parser")
        dn = prof_soup.find('h1', {'class': 'rug-mb-0'})
        #print(dn)
        #name = 'hi'
        name = dn.text
        print(name, link)
        femail = ''    #final email
        de  = prof_soup.find_all('span', {'class' : 'js--decode'})   #these contains all emails
        #print(de)
        for dde in de:
            email = dde.text
            email = email.replace(' ', '@')
            if email not in garbage_emails:
                #print(email)
                femail = email

        #print(femail)

        #email = new_emails[0]
        #print(name, link)
        OnlygetEmail(var, garbage_emails, name, link, femail, prof_resp)


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
    harvard()

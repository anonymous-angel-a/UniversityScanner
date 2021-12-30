#!/usr/bin/env python
# coding: utf-8

# In[15]:


import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def brunelluni():
    url = "https://www.brunel.ac.uk/people/cedps/computer"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    #print(r.text)
    #print(soup.get_text())
    
    # file initialization to write
    filename = "brunelluni.txt"
    f = open(filename, "w", encoding='utf-8')

    excel_filename = "brunelluni.csv"
    f2 = open(excel_filename, "w", encoding='utf-8')
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a", encoding='utf-8')
    csvwriter2 = csv.writer(f3)
    
    u_name = "Brunel University London"
    country = "United Kingdom"
    garbage_emails = ['contact@massey.ac.nz']
    var = [f, csvwriter, csvwriter2, u_name, country]

    #print(soup)
    d = soup.find('tbody')
    d = d.find_all('tr')
    #print(d)
    #d = d.find_all('tr')
    #print(d)
    #d = d.find_all('p')
    
    #print(d)
    #print(len(e))
    #d = d.find_all('a')
    #print(len(d))
    #print(d)
    
    #print(type(d))
    #print(a)
    #print(type(c))
    #print(len(d))
    
    b=0
    for i in d:
        try:
            link1 = i.find('a')
        except:
            continue
        name = link1.find('img').get('alt')
        #print(name)
        link1 = 'https://www.brunel.ac.uk'+link1.get('href')
        email = i.find('div',{'class':'hidden-lg-up'}).get_text()
        #print(name)
        #print(link)
        
        #print(link)
        #print(name)
        #print(link1)
        #print(name.get_text())
        #print(i)
        #email = link[1].get_text()
        #link1 = 'https://www.ucc.ie/'+link[2].get('href')
        
        #name = i.get_text()
        #print(link1)
        #print(email)
        #print(link1)
        #print(link1)
        #link1 = requests.get(link1)
        #print(type(link1))
        #if link1 == ""
        #soup = BeautifulSoup(link1.text, "html.parser")
        #print(soup)
        #name1 = soup.find_all('td',{'class':'mask vkpadding'})
        #name = i.get_text()
        #j=0
        #email = None
                #print(name)
        
        #print(email)
        #print(link1)
        #break
        
        
        #print(link1)
        #print(name)
        #name = name.get_text()
        if link1 == None :
            continue
        #name=name.strip()                             # extracting prof page link
        
        b=b+1
        
        #print(b)
        #print(name)
        #print(link)
        try:
            prof_resp = requests.get(link1)      # requesting prof homepgae
        except:
            continue
        
        #print(name,email)
        #link = link.get('href')
        #if link ==None:
        #    link =link1
        #try:
        #    prof_resp = requests.get(link)      # requesting prof homepgae
        #except:
        #    continue
        
        #email = i.find('p',{'class':'pf_short_email'})
        #e = email.get_text()
        #print(e)
        #print(email)
        #email = email.find('script')
        #print(email)
        #email = email.get_text()
        #print(email)
        #email='Not Found'
        #b=b+1
        #print(b)
        print(name, email, link1)
        filterandgetEmail(var, garbage_emails, name, link1, email, prof_resp)
        #b = b+1


def filterandgetEmail(var, garbage_emails, name, link, email, prof_resp):
    f = var[0]
    csvwriter = var[1]
    csvwriter2 = var[2]

    u_name = var[3]
    country = var[4]

    #keyword_list = ['Parallel Systems','parallel systems','parallel system','Parallel System','Computer architecture','computer architecture','Computer Architecture', 'Hardware And System Architecture', 'hardware and system architecture', 'Hardware and Architecture', 'hardware and architecture', 'embedded system', 'Embedded System','Computer Organization','VLSI', 'Computer and System','Distributed System', 'distributed system', 'Distributed system' ]
    keyword_list = ['Computer Organization','Computer organization','computer Organization','computer organization','computer architecture', 'Computer architecture', 'Embedded System', 'Embedded system', 'embedded system']   # 'Computer Architecture',
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
                #print(new_emails)
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
    #print("aa")
    brunelluni()
    print("finish")


# In[ ]:





# In[ ]:





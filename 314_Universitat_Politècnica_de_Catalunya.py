import requests
import urllib.request
import time
import urllib
import re
import csv
from bs4 import BeautifulSoup

def Universitat_Politècnica_de_Catalunya():
    url = "https://www.ac.upc.edu/ca/personal"   # homepage url
    r = requests.get(url)                                        # request to url

    # getting the soup by parsing the html parsel to text to request r
    soup = BeautifulSoup(r.text, "html.parser")

    # file initialization to write
    filename = "Universitat_Politècnica_de_Catalunya.txt"
    f = open(filename, "w")

    excel_filename = "Universitat_Politècnica_de_Catalunya.csv"
    f2 = open(excel_filename, "w")
    csvwriter = csv.writer(f2)

    overall_file = "all_emails.csv"
    f3 = open(overall_file, "a")
    csvwriter2 = csv.writer(f3)

    u_name = "Universitat Politècnica de Catalunya"
    country = "Spain"

    garbage_emails = []
    var = [f, csvwriter, csvwriter2, u_name, country]

    # d gives the array of all profs on the dept homepage
    # d = soup.find('a', {'class':"accordian-title"})
    print(soup)
    d = soup.find('tbody')
    #dd = d.find('tr',{'class':'ng-scope'})
     
   

    #print(dd)
    #iterating for every prof
    #print(d)
    f.write("https://personals.ac.upc.edu/eduard/" + '\n' + "Eduard Ayguade Parra" + "\t"+ "eduard@ac.upc.edu" + "\n")
    csvwriter.writerow([u_name, country,"Eduard Ayguade Parra", "eduard@ac.upc.edu","https://personals.ac.upc.edu/eduard/"])
    csvwriter2.writerow([u_name, country,"Eduard Ayguade Parra" ,"eduard@ac.upc.edu","https://personals.ac.upc.edu/eduard/"]) 

    f.write("Not available" + '\n' + "Jaime M. Delgado Merce" + "\t"+ "jaime@ac.upc.edu" + "\n")
    csvwriter.writerow([u_name, country,"Jaime M. Delgado Merce", "jaime@ac.upc.edu","Not available"])
    csvwriter2.writerow([u_name, country,"Jaime M. Delgado Mercea" ,"jaime@ac.upc.edu","Not available"]) 

    f.write("https://personals.ac.upc.edu/jordid/" + '\n' + "Eduard Ayguade Parra" + "\t"+ "jordi.domingo@ac.upc.edu" + "\n")
    csvwriter.writerow([u_name, country,"Jordi Domingo Pascual", "jordi.domingo@ac.upc.edu","https://personals.ac.upc.edu/jordid/"])
    csvwriter2.writerow([u_name, country,"Jordi Domingo Pascual" ,"jordi.domingo@ac.upc.edu","https://personals.ac.upc.edu/jordid/"])



    f.write("https://personals.ac.upc.edu/jorge/" + '\n' + "Jorge Garcia Vidal" + "\t"+ "jorge.domingo@ac.upc.edu" + "\n")
    csvwriter.writerow([u_name, country,"Jorge Garcia Vidal", "jorge.domingo@ac.upc.edu","https://personals.ac.upc.edu/jorge/"])
    csvwriter2.writerow([u_name, country,"Jorge Garcia Vidal" ,"jorge.domingo@ac.upc.edu","https://personals.ac.upc.edu/jorge/"])


    f.write("https://personals.ac.upc.edu/antonio/" + '\n' + "Antonio Maria Gonzalez Colas" + "\t"+ "antonio@ac.upc.edu" + "\n")
    csvwriter.writerow([u_name, country,"Antonio Maria Gonzalez Colas", "antonio@ac.upc.edu","https://personals.ac.upc.edu/antonio/"])
    csvwriter2.writerow([u_name, country,"Antonio Maria Gonzalez Colas" ,"antonio@ac.upc.edu","https://personals.ac.upc.edu/antonio/"])



    f.write("https://personals.ac.upc.edu/jesus/" + '\n' + "Jesus Jose Labarta Mancho" + "\t"+ "jesus.labarta@ac.upc.edu" + "\n")
    csvwriter.writerow([u_name, country,"JJesus Jose Labarta Mancho", "jesus.labarta@ac.upc.edu","https://personals.ac.upc.edu/jesus/"])
    csvwriter2.writerow([u_name, country,"Jesus Jose Labarta Mancho" ,"jesus.labartab3666tv                                                                                                                                                                                                                                                                                                                                                                                                                     @ac.upc.edu","https://personals.ac.upc.edu/jesus/"])
     



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
    Universitat_Politècnica_de_Catalunya()
    

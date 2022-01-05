import csv
filename = "soas.txt"
f = open(filename, "w")

excel_filename = "soas.csv"
f2 = open(excel_filename, "w")
csvwriter = csv.writer(f2)

overall_file = "all_emails.csv"
f3 = open(overall_file, "a")
csvwriter2 = csv.writer(f3)

u_name = "SOAS University of London"
country = "Us"
print("SOAS University of London - No Computer Science department")
f.write("SOAS University of London - No Computer Science department")
csvwriter.writerow([u_name, country, "SOAS University of London - No Computer Science department"])
csvwriter2.writerow([u_name, country, "SOAS University of London - No Computer Science department"])
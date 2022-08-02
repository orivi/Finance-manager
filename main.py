import csv
import gspread
from time import sleep


def hsbcVO(filename):
    salaries = ["důchod", "066", "web", "STŘED"]
    investments = ["revolutie", "Trading 212", "Revolut"]
    coffeeShops = ["KAFEJNICA", "Pivovaru", "CAFE",
                   "COFFEE", "OBYVAK", "ZA PECI S.R.O."]
    education = ["Udemy", "KOH-I-NOOR", "ENVATO"]
    clothes = ["Nike"]
    transport = ["www.cd.cz"]
    fta = ["LAGUNA", "FITNESS"]
    food = ["GYMBEAM.CZ","KEBAB", "tousty", "VEIKALS", "Restorans", "BAR", "DELIKOMAT", "PIZZA", "SUSHI", "Boulevard", "kaufland",
            "ALBERT", "Penny", "GLOBAL", "POTRAVIN", "VECERKA", "Billa", "KFC", "PIZZERIA"]
    cosmetics = ["parfemy.cz", "TETA", "ROSSMANN",
                 "Happy End Lounge", "MEDICAMEN", "LEKARNA", "DentSmile"]
    accessories = ["*TVRZENASKLA.EU", "KRYTEO", "applemix.cz", "MALL", "ALZA"]
    subscriptions = ["APPLE.COM/BILL"]

    sa = gspread.service_account()
    sh = sa.open("Personal Finances")

    transactions = []

    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        next(csv_reader)
        for row in csv_reader:
            date = row[1]
            ammount = float(row[2].replace(",", "."))
            
            months = ["january", "february", "march", "april", "may", "june",
"july", "august", "september", "october", "november", "december"]
            month = ""
            for index in range(len(months)):
                if str(index) == date[4] and date[3] == "0":
                    month = months[index-1]
                if date[3] != "0":
                    month = months[int(date[3:5])-1]
                    
            category = ""
            if row[13] == "Karetní transakce" or row[13] == "Okamžitá příchozí platba" or row[13] == "Bezhotovostní příjem" or row[13] == "Platba převodem uvnitř banky":
                if row[12] != "":
                    name = row[12]
                if "Výběr z bankomatu" in row[12]:
                    category = "withdrawal"
                if row[12] == "":
                    name = f"Instant incoming payment: {row[5]}"
                
            if row[13] == "Vklad v hotovosti":
                name = "cash deposit"
                category = "cash deposit"
                
            if row[13] == "Okamžitá odchozí platba":
                name = "Instant outgoing payment"

            for item in salaries:
                if item.lower() in name.lower() or item.lower() in row[5].lower():
                    category = "salary"
                    break

            for item in investments:
                if item.lower() in name.lower():
                    category = "investment"
                    break

            for item in coffeeShops:
                if item.lower() in name.lower():
                    category = "coffee shop"
                    break

            for item in education:
                if item.lower() in name.lower():
                    category = "education"
                    break

            for item in clothes:
                if item.lower() in name.lower():
                    category = "clothes"
                    break

            for item in transport:
                if item.lower() in name.lower():
                    category = "transport"
                    break

            for item in fta:
                if item.lower() in name.lower():
                    category = "free time activities"
                    break

            for item in food:
                if item.lower() in name.lower():
                    category = "food"
                    break

            for item in cosmetics:
                if item.lower() in name.lower():
                    category = "cosmetics"
                    break

            for item in accessories:
                if item.lower() in name.lower():
                    category = "accessories"
                    break

            for item in subscriptions:
                if item.lower() in name.lower():
                    category = "subscriptions"
                    break

            if category == "":
                category = "other"

            transaction = (date, ammount, category, name)
            wks = sh.worksheet(f"{month}")
            wks.insert_row(transaction, 7)
            sleep(2)
            transactions.append(transaction)


hsbcVO("hsbc.csv")

import lxml
import pymongo
import re
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup


def connect_db():
    client = pymongo.MongoClient("localhost", 27017)
    return client.soup

def insert_mortgage(db, **itm):
    db.mortgage.insert({
        'company': itm['company'],
        'category': itm['category'],
        'rate': itm['rate'],
        'apr': itm['apr'],
        'points': itm['points'],
        'payment': itm['payment'],
        'created_at': datetime.today()
    })

def get_safecu_mortgage_rates(db):
    url = "https://www.safecu.org/mortgage-rates.xml"
    site = urlopen(url).read()
    soup = BeautifulSoup(site, "lxml-xml")

    interested_rates = [
        {'F30-1': '30-Year Fixed'},
        {'F30-2': ''},
        {'F30-3': ''},
        {'F30J-1': '30-Year Fixed Jumbo'},
        {'F30J-2': ''},
        {'F30J-3': ''},
        {'F30NOMI-1': '30-Year Fixed - No mortgage insurance'},
        {'F30NOMI-2': ''},
        {'F30NOMI-3': ''},
        {'F30JMI-1': '30-Year Fixed Jumbo - No mortgage insurance'},
        {'F30JMI-2': ''},
        {'F30JMI-3': ''}
    ]

    print()
    print("Date: {}".format(datetime.strftime(datetime.today().date(),
                                              "%b %d, %Y")))
    print()
    company_name = "Safe Credit Union Mortgage Rates"
    print(len(company_name) * "=")
    print(company_name)
    print(len(company_name) * "=")

    i = 1
    for int_rate in interested_rates:
        key = list(int_rate.keys())
        value = list(int_rate.values())

        if value[0]:
            print("\n{}".format(value[0]))
            print(len(value[0]) * "-")

        rate = round(float(soup.MORTGAGERATES.find(int_rate).RATE.string), 3)

        points = "{}".format(
            round(float(soup.MORTGAGERATES.find(int_rate).POINTS30.string), 3)
        )

        apr = "{}".format(round(float(soup.MORTGAGERATES.find(int_rate).
                                       APR.string) * 100, 3))

        payment = "{}".format(
            round(float(soup.MORTGAGERATES.find(int_rate).PAYMENT.string), 2)
        )

        item = {}
        item['company'] = 'safecu'
        item['category'] = key[0]
        item['rate'] = float(rate)
        item['apr'] = float(apr)
        item['points'] = float(points)
        item['payment'] = float(payment)

        insert_mortgage(db, **item)

        main_str = "{}. Rate: {}, Point: {}, APR: {}%, Payment: ${}".\
            format(i, rate, points, apr, payment)

        print(main_str)

        i += 1

    print()

def get_wells_fargo_mortgage_rates(db):
    url = "https://www.wellsfargo.com/mortgage/rates/"
    site = urlopen(url).read()
    soup = BeautifulSoup(site, "lxml")

    company_name = "Wells Fargo Mortgage Rates"
    print(len(company_name) * "=")
    print(company_name)
    print(len(company_name) * "=")

    html_headers = soup.find(id='PurchaseRatesTable').tbody.find_all(
        attrs={
            "id": "productName",
            "scope": "row",
            "headers": "product confirmFHA"
        }
    )

    headers = []
    for x in html_headers:
        headers.append(x.a.string)

    html_jumbo_headers = soup.find(id='PurchaseRatesTable').tbody.find_all(
        attrs={
            "id": "productName",
            "scope": "row",
            "headers": "product jumboLoan"
        }
    )

    for x1 in html_jumbo_headers:
        headers.append(x1.a.string)

    html_int_rates = soup.find(id='PurchaseRatesTable').tbody.find_all(
        attrs={
            "headers": "productName confirmFHA intRate"
        }
    )

    rates = []
    for y in html_int_rates:
        rates.append(y.string)

    html_jumbo_int_rates = soup.find(id='PurchaseRatesTable').tbody.find_all(
        attrs={
            "headers": "productName jumboLoan intRate"
        }
    )

    for y1 in html_jumbo_int_rates:
        rates.append(y1.string)

    html_aprs = soup.find(id='PurchaseRatesTable').tbody.find_all(
        attrs={
            "headers": "productName confirmFHA apr"
        }
    )

    aprs = []
    for z in html_aprs:
        aprs.append(z.string)

    html_jumbo_aprs = soup.find(id='PurchaseRatesTable').tbody.find_all(
        attrs={
            "headers": "productName jumboLoan apr"
        }
    )

    for z1 in html_jumbo_aprs:
        aprs.append(z1.string)

    i = 1
    for index in range(0, len(headers), 1):
        if headers[index] == '30-Year Fixed Rate' or \
           headers[index] == '30-Year Fixed-Rate FHA' or \
           headers[index] == '30-Year Fixed-Rate Jumbo' or \
           headers[index] == '':

            if headers[index] == '30-Year Fixed Rate':
                category = 'F30-1'
            elif headers[index] == '30-Year Fixed-Rate FHA':
                category = 'F30FHA-1'
            else:
                category = 'F30J-1'

            rate = re.findall("\d+\.\d+", rates[index])
            apr = re.findall("\d+\.\d+", aprs[index])

            print()
            print(headers[index])
            print(len(headers[index]) * "-")
            print("{}. Interest Rate: {}, APR: {}%".format(
                i, float(rate[0]), float(apr[0])
            ))

            item = {}
            item['company'] = 'wellsfargo'
            item['category'] = category
            item['rate'] = float(rate[0])
            item['apr'] = float(apr[0])
            item['points'] = 0
            item['payment'] = 0

            insert_mortgage(db, **item)

            i += 1

    print()

def get_quicken_loans_mortgage_rates(db):
    url = "https://www.quickenloans.com/mortgage-rates"
    site = urlopen(url).read()
    soup = BeautifulSoup(site, "lxml")

    company_name = "Quicken Loans Mortgage Rates"
    print(len(company_name) * "=")
    print(company_name)
    print(len(company_name) * "=")

    html_product_names = soup.find_all(
        attrs={
            "class": "rateTable__product__name"
        }
    )

    names = []
    for x in html_product_names:
        names.append(x.a.text)

    html_product_rates = soup.find_all(
        attrs={
            "class": "rateTable__product__rate"
        }
    )

    rates = []
    for y in html_product_rates:
        rates.append(str(y.string).strip())

    html_aprs = soup.find_all(
        attrs={
            "class": "rateTable__product__apr"
        }
    )

    aprs = []
    for z in html_aprs:
        aprs.append(str(z.string).replace("(", "").\
                    replace(")", "").replace(" APR", ""))

    i = 1
    for index in range(0, len(names), 1):
        if names[index] == '30-Year Fixed':
            category = 'F30-1'
            rate = re.findall("\d+\.\d+", rates[index])
            apr = re.findall("\d+\.\d+", aprs[index])

            item = {}
            item['company'] = 'quickenloans'
            item['category'] = category
            item['rate'] = float(rate[0])
            item['apr'] = float(apr[0])
            item['points'] = 0
            item['payment'] = 0

            insert_mortgage(db, **item)

            print()
            print(names[index])
            print(len(names[index]) * "-")
            print("{}. Rate: {}, APR: {}%".format(
                i, float(rate[0]), float(apr[0])
            ))

            i += 1

    print()

if __name__ == '__main__':
    db = connect_db()
    get_safecu_mortgage_rates(db)
    get_wells_fargo_mortgage_rates(db)
    get_quicken_loans_mortgage_rates(db)
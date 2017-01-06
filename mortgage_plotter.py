from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from mapping import category, company
from bson.code import Code
import pymongo
import sys

pic_dir = "/Users/yamin/Programming/Python/soup/images"
# pic_dir = "/home/osmc/Pictures/Mortgage Charts"

def connect_db():
    client = pymongo.MongoClient("localhost", 27017)
    return client.soup


def plot_me(**param):
    plt.margins(x=0.1, y=0.1)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.minorticks_on()
    plt.plot(
        param['x'],
        param['y'],
        param['line_color'],
        label=param['line_label']
    )
    plt.plot(
        param['x'],
        param['y'],
        param['scatter_color']
    )
    # plt.xlabel('Dates')
    plt.ylabel('Rates %')

    try:
        legend = param['legend']
    except KeyError:
        legend = False

    if legend:
        plt.legend(loc='best', bbox_to_anchor=(param['offset'], -0.15), ncol=3)

    try:
        title = param['title']
    except KeyError:
        title = None

    if title:
        plt.title('{} - {}'.format(param['company'], title))

    plt.gcf().autofmt_xdate()
    plt.grid(True)
    plt.savefig(param['output'])


def get_mortgage_by_comp_cat(db, comp, cat):
    reducer = Code("""
        function(curr, result) {
        }
    """)
    frequency = sys.argv[1]

    date_query = {}
    if frequency == "monthly":
        date_query = {
            "created_at": {
                "$gte": datetime.today() - timedelta(days=30)
            }
        }
    else:
        date_query = {
            "created_at": {
                "$gte": datetime.today() - timedelta(days=7)
            }
        }


    return db.mortgage.group(
        key={
            "company": 1,
            "category": 1,
            "rate": 1,
            "apr": 1,
            "created_at": 1
        },
        reduce=reducer,
        initial={},
        condition={
            "company": comp,
            "category": cat,
            "created_at": date_query['created_at']
        }
    )

def prepare_plot_data(**data):
    dates = []
    rates = []

    for result in data['results']:
        dates.append(
            result['created_at'].strftime("%Y-%m-%d")
        )

        rates.append(result['rate'])

    x = [datetime.strptime(d, '%Y-%m-%d').date() for d in dates]
    y = rates

    param = {}
    param['output'] = "{}/{}".format(pic_dir, data['png'])
    param['x'] = x
    param['y'] = y
    param['company'] = data['company']
    param['category'] = data['category']

    return param


def plot_safecu(db):
    frequency = sys.argv[1]

    plt.figure(1)
    # Safecu - 30 Year Fixed Rate - 1
    f30_1_results = get_mortgage_by_comp_cat(db, "safecu", "F30-1")
    data = {
        "results": f30_1_results,
        "company": company.safecu.value,
        "category": "{}-1".format(category.F30_1.value),
        "png": "{}_safecu_f30.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xb"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 1"

    if os.path.exists(param['output']):
        os.remove(param['output'])

    plot_me(**param)

    # Safecu - 30 Year Fixed Rate - 2
    f30_2_results = get_mortgage_by_comp_cat(db, "safecu", "F30-2")
    data = {
        "results": f30_2_results,
        "company": company.safecu.value,
        "category": "{}-2".format(category.F30_2.value),
        "png": "{}_safecu_f30.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xg"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 2"
    plot_me(**param)

    # Safecu - 30 Year Fixed Rate - 3
    f30_3_results = get_mortgage_by_comp_cat(db, "safecu", "F30-3")
    data = {
        "results": f30_3_results,
        "company": company.safecu.value,
        "category": "{}-3".format(category.F30_3.value),
        "png": "{}_safecu_f30.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xy"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 3"
    param['title'] = category.F30_3.value
    param['legend'] = True
    param['offset'] = 0.90
    plot_me(**param)

    plt.figure(2)
    # Safecu - 30 Year Fixed Jumbo Rate - 1
    F30J_1_results = get_mortgage_by_comp_cat(db, "safecu", "F30J-1")
    data = {
        "results": F30J_1_results,
        "company": company.safecu.value,
        "category": "{}-1".format(category.F30J_1.value),
        "png": "{}_safecu_f30j.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xb"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 1"

    if os.path.exists(param['output']):
        os.remove(param['output'])

    plot_me(**param)

    # Safecu - 30 Year Fixed Jumbo Rate - 2
    F30J_2_results = get_mortgage_by_comp_cat(db, "safecu", "F30J-2")
    data = {
        "results": F30J_2_results,
        "company": company.safecu.value,
        "category": "{}-2".format(category.F30J_2.value),
        "png": "{}_safecu_f30j.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xg"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 2"
    plot_me(**param)

    # Safecu - 30 Year Fixed Jumbo Rate - 3
    F30J_3_results = get_mortgage_by_comp_cat(db, "safecu", "F30J-3")
    data = {
        "results": F30J_3_results,
        "company": company.safecu.value,
        "category": "{}-3".format(category.F30J_3.value),
        "png": "{}_safecu_f30j.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xy"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 3"
    param['title'] = category.F30J_3.value
    param['legend'] = True
    param['offset'] = 0.90
    plot_me(**param)

    plt.figure(3)
    # Safecu - 30-Year Fixed - No mortgage insurance - 1
    F30NOMI_1_results = get_mortgage_by_comp_cat(db, "safecu", "F30NOMI-1")
    data = {
        "results": F30NOMI_1_results,
        "company": company.safecu.value,
        "category": "{}-1".format(category.F30NOMI_1.value),
        "png": "{}_safecu_f30nomi.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xb"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 1"

    if os.path.exists(param['output']):
        os.remove(param['output'])

    plot_me(**param)

    # Safecu - 30-Year Fixed - No mortgage insurance - 2
    F30NOMI_2_results = get_mortgage_by_comp_cat(db, "safecu", "F30NOMI-2")
    data = {
        "results": F30NOMI_2_results,
        "company": company.safecu.value,
        "category": "{}-2".format(category.F30NOMI_2.value),
        "png": "{}_safecu_f30nomi.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xg"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 2"
    plot_me(**param)

    # Safecu - 30-Year Fixed - No mortgage insurance - 3
    F30NOMI_3_results = get_mortgage_by_comp_cat(db, "safecu", "F30NOMI-3")
    data = {
        "results": F30NOMI_3_results,
        "company": company.safecu.value,
        "category": "{}-3".format(category.F30NOMI_3.value),
        "png": "{}_safecu_f30nomi.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xy"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 3"
    param['title'] = category.F30NOMI_3.value
    param['legend'] = True
    param['offset'] = 0.90
    plot_me(**param)

    plt.figure(4)
    # Safecu - 30-Year Fixed Jumbo - No mortgage insurance - 1
    F30JMI_1_results = get_mortgage_by_comp_cat(db, "safecu", "F30JMI-1")
    data = {
        "results": F30JMI_1_results,
        "company": company.safecu.value,
        "category": "{}-1".format(category.F30JMI_1.value),
        "png": "{}_safecu_f30jmi.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xb"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 1"

    if os.path.exists(param['output']):
        os.remove(param['output'])

    plot_me(**param)

    # Safecu - 30-Year Fixed Jumbo - No mortgage insurance - 2
    F30JMI_2_results = get_mortgage_by_comp_cat(db, "safecu", "F30JMI-2")
    data = {
        "results": F30JMI_2_results,
        "company": company.safecu.value,
        "category": "{}-2".format(category.F30JMI_2.value),
        "png": "{}_safecu_f30jmi.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xg"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 2"
    plot_me(**param)

    # Safecu - 30-Year Fixed Jumbo - No mortgage insurance - 3
    F30JMI_3_results = get_mortgage_by_comp_cat(db, "safecu", "F30JMI-3")
    data = {
        "results": F30JMI_3_results,
        "company": company.safecu.value,
        "category": "{}-3".format(category.F30JMI_3.value),
        "png": "{}_safecu_f30jmi.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xy"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 3"
    param['title'] = category.F30JMI_3.value
    param['legend'] = True
    param['offset'] = 0.90
    plot_me(**param)


def plot_wellsfargo(db):
    frequency = sys.argv[1]

    plt.figure(5)
    # Wells Fargo - 30-Year Fixed Rate - 1
    F30_1_results = get_mortgage_by_comp_cat(db, "wellsfargo", "F30-1")
    data = {
        "results": F30_1_results,
        "company": company.wellsfargo.value,
        "category": "{}-1".format(category.F30_1.value),
        "png": "{}_wellsfargo_f30.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xb"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 1"
    param['title'] = category.F30_1.value
    param['offset'] = 0.60
    param['legend'] = True

    if os.path.exists(param['output']):
        os.remove(param['output'])

    plot_me(**param)

    plt.figure(6)
    # Wells Fargo - 30-Year Fixed-Rate FHA - 1
    F30FHA_1_results = get_mortgage_by_comp_cat(db, "wellsfargo", "F30FHA-1")
    data = {
        "results": F30FHA_1_results,
        "company": company.wellsfargo.value,
        "category": "{}-1".format(category.F30FHA_1.value),
        "png": "{}_wellsfargo_f30fha.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xb"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 1"
    param['title'] = category.F30FHA_1.value
    param['offset'] = 0.60
    param['legend'] = True

    if os.path.exists(param['output']):
        os.remove(param['output'])

    plot_me(**param)

    plt.figure(7)
    # Wells Fargo - 30-Year Fixed-Rate Jumbo - 1
    F30J_1_results = get_mortgage_by_comp_cat(db, "wellsfargo", "F30J-1")
    data = {
        "results": F30J_1_results,
        "company": company.wellsfargo.value,
        "category": "{}-1".format(category.F30J_1.value),
        "png": "{}_wellsfargo_f30j.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xb"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 1"
    param['title'] = category.F30J_1.value
    param['offset'] = 0.60
    param['legend'] = True

    if os.path.exists(param['output']):
        os.remove(param['output'])

    plot_me(**param)


def plot_quickenloans(db):
    frequency = sys.argv[1]

    plt.figure(8)
    # Quicken Loans - 30-Year Fixed - 1
    F30_1_results = get_mortgage_by_comp_cat(db, "quickenloans", "F30-1")
    data = {
        "results": F30_1_results,
        "company": company.quickenloans.value,
        "category": "{}-1".format(category.F30_1.value),
        "png": "{}_quickenloans_f30.png".format(frequency)
    }
    param = prepare_plot_data(**data)
    param['line_color'] = "-xb"
    param['scatter_color'] = "ro"
    param['line_label'] = "Series 1"
    param['title'] = category.F30_1.value
    param['offset'] = 0.60
    param['legend'] = True

    if os.path.exists(param['output']):
        os.remove(param['output'])

    plot_me(**param)

if __name__ == '__main__':
    db = connect_db()
    plot_safecu(db)
    plot_wellsfargo(db)
    plot_quickenloans(db)
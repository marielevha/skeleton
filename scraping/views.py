import csv
import smtplib
import ssl
import email
import threading
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import redirect

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from .models import Announce
from .models import City
from utils import constants as const
from .run import launch_scraping
from django_pandas.io import read_frame
import pandas as pd
import numpy as np


def index(request):
    # r = threading.Thread(target=launch_scraping)
    # r.start()
    """run = RunScraper()
    lr = run.get_last_ma_ad_from_db()
    if lr is not None:
        lr = model_to_dict(lr)
    run.scrape_ma(last_record=lr)
    run.save_data_to_db()"""
    announces = Announce.objects.all()

    pagination = Paginator(announces, 10)
    page = request.GET.get('page')
    announces = pagination.get_page(page)
    return render(request, 'index.html', {
        "announces": announces,
    })


def export_to_csv(request):
    data = Announce.objects.all().values_list(
        'title', 'price', 'date',
        'city', 'source'
    )
    response = HttpResponse(content_type='text/csv')
    try:
        writer = csv.writer(response)
        writer.writerow(const.CSV_HEADER)
        for el in data:
            writer.writerow(el)
        response['Content-Disposition'] = 'attachment; filename="data_announces.csv"'
        return response
    except:
        response['Content-Disposition'] = 'attachment; filename="nothing_announces.csv"'
        return response


def send_email(request):
    cities = Announce.objects.all().values_list('city', flat=True).distinct()
    return render(request, 'send-mail.html', {
        'cities': cities
    })


def send_data_by_email(request):
    # Read form inputs
    to = request.POST['email']
    city = request.POST['city']
    start_price = float(request.POST['start_price'])
    end_price = float(request.POST['end_price'])
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']

    # Find from db with filter
    announces = Announce.objects.filter(
        city=city,
        date__range=[start_date, end_date],
        price__range=[start_price, end_price]
    )

    # Build & Send email
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = const.SMTP_FROM
    message["To"] = to
    message["Subject"] = const.SMTP_SUBJECT
    # message["Bcc"] = receiver_email

    # Add body to email
    message.attach(MIMEText(const.SMTP_BODY, "plain"))
    filename = "scraping/data.csv"

    # Write CSV file
    data = announces.values_list(
        'title', 'price', 'date',
        'city', 'source'
    )
    with open(filename, 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        # write the header
        writer.writerow(const.CSV_HEADER)

        # write the data
        for el in data:
            writer.writerow(el)

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP(const.SMTP_HOST, const.SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(const.SMTP_FROM, const.SMTP_PASSWORD)
        server.sendmail(const.SMTP_FROM, const.SMTP_TO, text)

    # print(f"ANNOUNCES LENGTH: {len(announces)}")
    # print(f"EMAIL : {to}")
    # print(f"CITY : {city}")
    # print(f"START PRICE : {start_price}")
    # print(f"END PRICE : {end_price}")
    # print(f"START DATE : {start_date}")
    # print(f"END DATE : {end_date}")
    response = redirect('/sendEmail')
    return response


def pivot_table(request):
    items = Announce.objects.all().values()
    df = pd.DataFrame(items)
    cols = ['price']
    value = ['A', 'D']
    # df[cols] = df[cols].astype(float)
    # pt = pd.pivot_table(df, index=['price'])
    # pt = pd.pivot_table(df, index=["type", "city"], values=["price"], aggfunc=np.sum)
    pt = pd.pivot_table(df, index=["type", "city"], values=["price"], aggfunc=np.average)
    print(pt)
    myDict = {
        # "df": df.to_html(
        #     classes='table table-striped table-bordered text-capitalize',
        #     columns=['title', 'price', 'city', 'type', 'date'],
        #     justify='justify',
        # ),
        "pt": pt.to_html(
            classes='table table-striped table-bordered text-capitalize',
            header=True,
            justify='justify',
            float_format='{:10.2f} DH'.format
        ),
    }
    # qs = Announce.objects.all().values()
    # df = read_frame(qs)
    return render(request, 'pivot-table.html', context=myDict)


def scrape(request):
    r = threading.Thread(target=launch_scraping)
    r.start()
    response = redirect('/')
    return response


def test(request):
    data = Announce.objects.all()
    for el in data:
        if el.price > float(20000):
            print(el.price)
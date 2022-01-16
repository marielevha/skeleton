import csv
import datetime
import re
import dateparser
import smtplib
import ssl
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
from scraping.utils import constants as const
from .runner import launch_scraping
import pandas as pd
import numpy as np


def index(request):
    announces = Announce.objects.all().order_by('-date')
    pagination = Paginator(announces, 20)
    page = request.GET.get('page')
    announces = pagination.get_page(page)
    return render(request, 'index.html', {
        "announces": announces,
    })


def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="announces.csv"'

    writer = csv.writer(response)
    writer.writerow(const.CSV_HEADER)

    data = Announce.objects.all().values_list(
        'title', 'price', 'date',
        'city', 'source'
    )
    for el in data:
        writer.writerow(el)

    return response


def send_email(request):
    cities = Announce.objects.all().values_list('city', flat=True).order_by('city').distinct()
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

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
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
        server.sendmail(const.SMTP_FROM, to, text)

    return redirect('send_email')


def pivot_table(request):
    items = Announce.objects.all().values()
    dataFrame = pd.DataFrame(items)
    pt = pd.pivot_table(dataFrame, index=["type", "city"], values=["price"], aggfunc=np.average)
    data = {
        "table": pt.to_html(
            classes='table table-striped table-bordered text-capitalize',
            header=True,
            justify='justify',
            float_format='{:10.2f} DH'.format
        ),
    }
    return render(request, 'pivot-table.html', context=data)


def scrape(request):
    r = threading.Thread(target=launch_scraping)
    r.start()
    return redirect('index')


def test(request):
    data = Announce.objects.all().order_by('-date')
    for el in data:
        el.city = el.city.lower()
        el.save()
    print(len(data))
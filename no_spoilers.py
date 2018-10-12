#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from urllib.parse import quote_plus
from pprint import pprint
import datetime
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.message

import pymysql

def mysqlconnect(shows, email_id):
    try:
        no_spoilers_db = pymysql.connect(
            host="localhost",
            user="NSuser",
            passwd="NSpass",
            database="no_spoilers_database"
        )
    except:
        print("Can't connect to database") 
        return 0

    mycursor = no_spoilers_db.cursor()

    sql = "CREATE TABLE IF NOT EXISTS viewers (id INT AUTO_INCREMENT PRIMARY KEY, emailId VARCHAR(255), tvSeries VARCHAR(1023))"
    mycursor.execute(sql)

    sql = "INSERT INTO viewers(emailId, tvSeries) VALUES (%s, %s)"
    val = (email_id, shows)
    print(val)
    mycursor.execute(sql, val)
    no_spoilers_db.commit()
    no_spoilers_db.close()

MY_ADDRESS = 'nospoilers.demo@gmail.com'
PASSWORD = 'N0sp0ilers'

def main():
    while True :
        email_id = input('Email Address:')
        shows = input('TV Series:')
        mysqlconnect(shows, email_id)

        shows = shows.split(',')
        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(MY_ADDRESS, PASSWORD)

        msg = email.message.Message()
        msg['From'] = MY_ADDRESS
        msg['To'] = email_id
        msg['Subject'] = 'REMINDER: Upcoming TV Series'
        msg.add_header('Content-Type', 'text/html')

        email_content = \
            """
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">

        </head>

        <body>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td>
            <table width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff" style="border: 1px solid #cfcece;">
                <tr>
                    <td>
                        <table cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9">
                        <tr>
                            <td width="50%" align="center" bgcolor="#f0b4b5"><h1 align="right" style="color: #d11c24;">No</h1></td>
                            <td width="50%" align="center" bgcolor="#f0b4b5"><h1 align="left" style="color: ##313131;">Spoilers!</h1></td>
                        </tr>
                        <tr>
                            <td width="100%" align="right" bgcolor="#df5e61"><pstyle="color: #3d3f49">Updated on: {}</p></td>
                        </tr>
                        </table>
                    </td>
                </tr>

        """.format(datetime.datetime.now())

        for show in shows:
            url = 'http://api.tvmaze.com/search/shows?q=' \
                + quote_plus(show)
            r = requests.get(url)
            switch = 0
            if r.ok:
                j = r.json()

                if not j:
                    res_str = '<b>Tv series name:</b> {} <br><b>Status:</b> Series not found.'.format(
                        show)
                    email_content += \
                        """
                    <hr style="color: #f34343; border-width: 5px;">
                    <tr>
                        <td>
                            <table cellpadding="0" cellspacing="0" align="center">
                            <tr>
                                <td width="500" align="center" bgcolor="d0d0d0" style="padding:5px;"><span><p>{}</p></span></td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    """.format(res_str)
                    exit(0)
                    
                found = j[0]['show']
                status = found['status']
                show_name = found['name']
                # show_id = found['id']
                image = found['image']['medium']
                imdb_id = found['externals']['imdb']
                imdb_link = "http://www.imdb.com/title/" + imdb_id
                try:
                    airtime_start = found['schedule']['time']
                    airtime_start = airtime_start[0:2] + airtime_start[3:5]
                    runtime = found['runtime']
                    airtime_end = int(airtime_start) + int(runtime)
                    airtime_end = str(airtime_end)
                except:
                    airtime_start = int("0000")
                    airtime_end = int("0060")

                if status == 'Ended':
                    res_str = "<b>Tv series name:</b><a href='{}'> {} </a><br><b>Status:</b> The show has finished streaming all its episodes.".format(
                        imdb_link, show_name)
                    email_content += \
                        """
                    <hr style="color: #feaf0d; border-width: 5px;">
                    <tr>
                        <td>
                            <table cellpadding="0" cellspacing="0" align="center">
                            <tr>
                                <td width="285" valign="top" bgcolor="ffffff" style="padding:5px;">
                                    <img align="center" src="{}" width="200" height="150">
                                </td>
                                <td width="285" valign="top" bgcolor="ffffff" style="padding:5px;">
                                    <span><p>{}</p></span>
                                </td>
                            </tr>
                            </table>
                        </td>
                    </tr>
                    """.format(image,
                            res_str)
                else:

                    try:
                        next_episode_link = found['_links'
                                                ]['nextepisode']['href']
                    except KeyError:
                        switch = 1

                    if not switch:
                        r2 = requests.get(next_episode_link)

                        if r2.ok:
                            next_episode_json = r2.json()
                            name = next_episode_json['name']
                            # season = next_episode_json['season']
                            airdate = next_episode_json['airdate']
                            res_str = \
                                "<b>Tv series name:</b><a href='{}'> {} </a> <br><b>Status:</b> The next episode '{}' airs on {}".format(imdb_link, show_name,
                                                                                                                                        name, airdate)

                            cal_date = airdate[0:4] + airdate[5:7] \
                                + airdate[8:10]
                            calendar_link = \
                                'https://www.google.com/calendar/render?' \
                                + 'action=TEMPLATE' + '&text=' \
                                + show_name.replace(' ', '+') \
                                + '+Streaming' + '&dates=' + cal_date \
                                + 'T' + airtime_start + '00Z/' \
                                + cal_date + 'T' + airtime_end + '00Z' \
                                + '&details=For+details,+link+here:+http://www.imdb.com/title/' \
                                + imdb_id
                            email_content += \
                                """
                            <hr style="color: #0070dd; border-width: 5px;">
                            <tr>
                                <td>
                                    <table cellpadding="0" cellspacing="0" align="center">
                                    <tr>
                                        <td width="285" valign="top" bgcolor="ffffff" style="padding:5px;">
                                            <img align="center" src="{}" width="200" height="150">
                                        </td>
                                        <td width="285" valign="top" bgcolor="ffffff" style="padding:5px;">
                                            <span><p>{}</p>
                                            <p>
                                                <a href='{}' align="right">Add to Calendar!</a>
                                            </p></span>
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                            </tr>
                            """.format(image,
                                    res_str, calendar_link)
                    else:
                        show_self = found['_links']['self']['href']
                        url = show_self
                        r2 = requests.get(url + '?embed=seasons')
                        url = r2.json()['_embedded']['seasons'
                                                    ][-1]['url']
                        r = requests.get(url)
                        start = r.text.find('Premieres')
                        end = r.text[start:].find('</span>')
                        out = r.text[start:start + end].split(' ')[-1]
                        out = int(out)
                        now = datetime.datetime.now()
                        now_year = now.year
                        if out > now_year:
                            res_str = "<b>Tv series name:</b><a href='{}'> {} </a><br><b>Status:</b> The next season begins in {}.".format(imdb_link, show_name,
                                                                                                                                        out)
                        else:
                            res_str = "<b>Tv series name:</b><a href='{}'> {} </a><br><b>Status:</b> No update on next season yet.".format(
                                imdb_link, show_name)
                        email_content += \
                            """
                        <hr style="color: #2da953; border-width: 5px;">
                        <tr>
                            <td>
                                <table cellpadding="0" cellspacing="0" align="center">
                                <tr>
                                    <td width="285" valign="top" bgcolor="ffffff" style="padding:5px;">
                                        <img align="center" src="{}" width="200" height="150">
                                    </td>
                                    <td width="285" valign="top" bgcolor="ffffff" style="padding:5px;">
                                        <span><p>{}</p></span>
                                    </td>
                                </tr>
                                </table>
                            </td>
                        </tr>
                        """.format(image,
                                res_str)

        email_content += \
            """
        </table>
        <table id="bottom" cellpadding="20" cellspacing="0" width="600" align="center">
            <tr>
            <td align="center">
                <p><a href="https://github.com/dhruv-chauhan/no_spoilers">View on Github</a></p>
            </td>
            </tr>
        </table><!-- top message -->
        </td></tr></table><!-- wrapper -->

        </body>
        </html>
        """
        msg.set_payload(email_content)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())

if __name__ == '__main__':
    main()

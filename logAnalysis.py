#!/usr/bin/env python3

# code for retrieving analytical data from news database

import psycopg2

DBNAME = "news"


def get_articles():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    articles_qry = "select * from articles_viewcount;"
    cursor.execute(articles_qry)
    articles = cursor.fetchall()
    db.close()
    return articles


def get_authors():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    authors_qry = "select * from authors_viewcount;"
    cursor.execute(authors_qry)
    authors = cursor.fetchall()
    db.close()
    return authors


def get_errors():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    errors_qry = """select to_char(day, 'MON-DD-YYYY') as day,
                    percentage from error_date where percentage > 1.0;"""
    cursor.execute(errors_qry)
    errors = cursor.fetchall()
    db.close()
    return errors


file = open("logsAnalysis_results.txt", "a+")
file.write("What are the most popular three articles of all time?\n")

for (title, views) in get_articles():
    file = open("logsAnalysis_results.txt", "a+")
    file.write(" \"%s\" -- %s views\n" % (title, views))
    file.close()

file = open("logsAnalysis_results.txt", "a+")
file.write("\n")
file.write("Who are the most popular article authors of all time?\n")


for (name, views) in get_authors():
    file = open("logsAnalysis_results.txt", "a+")
    file.write(" %s -- %s views\n" % (name, views))
    file.close()

file = open("logsAnalysis_results.txt", "a+")
file.write("On which days did more than 1% of requests lead to errors?\n")


for (day, percentage) in get_errors():
    file = open("logsAnalysis_results.txt", "a+")
    file.write(" %s -- %s%% errors\n" % (day, percentage))
    file.close()

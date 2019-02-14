# Logs Analysis Project

This is a program used to query a PostgreSQL database and then print the results to a plain text file.


### 5 Total Views Created:
   - articles_viewcount
   - authors_viewcount
   - total_status
   - error_status
   - error_date
 
### SQL for create views used:
 
    create view articles_viewcount as select title, count(path) as views from articles, log where articles.slug like substr(log.path, 10) group by title order by count(path) desc limit 3;

    create view authors_viewcount as select name, sum(views) as view_count from (select name, title, count(path) as views from articles, authors, log where articles.slug like substr(log.path, 10) AND articles.author = authors.id group by title, name order by count(path) desc limit 10) as authors_count group by name order by view_count desc;

    create view total_status as select time::date as day, count(status) as total_status_count from log group by day;
 
    create view error_status as select time::date as day, status, count(status) as error_count from log where status like '404%' group by day, status order by day;
 
    create view error_date as select error_status.day, (((error_status.error_count*1.0) / total_status.total_status_count) * 100)::numeric(12,2) as percentage from error_status, total_status where error_status.day = total_status.day;

### Design of code:
The program answers these 3 questions:
- What are the most popular three articles of all time?
- Who are the most popular article authors of all time?
- On which days did more than 1% of requests lead to errors?

The logsAnalysis.py file contains 3 different functions to query the news database and return the results specific to each question. Each function connects to the database, executes a SQL query, then fetches the results of the query into a variable. The last step in the functions returns the variable that contains the query results.

After all 3 functions have ran and queried the database and returned the expected results, the program will then move on to opening a file named "logsAnalysis_results.txt", if this file is not present then the program will automatically create this file. Once the file is opened/created the program writes the question that needs to be answered, and then proceeds to write the results of the variables in each function performed specific to each question into the "logsAnalysis_results.txt" file.


### How to execute:
   * First you will need to ensure the "news" database is running on your vagrant machine.
      - You will need to download the newsdata.sql file to your /vagrant shared directory. You can download the data here: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

   * Place the logAnalysis.py file into your shared /vagrant directory
   
   Open a terminal and cd to your /vagrant directory and run the command:

    vagrant ssh
    
   Your terminal will now look like the following:

    vagrant@vagrant:$
   
   Next, cd into the /vagrant directory on vagrant box terminal.
   
    vagrant@vagrant:$ cd /vagrant

   Make sure to setup the news database on your vagrant machine by running the command:
   
    vagrant@vagrant:/vagrant$ psql -d news -f newsdata.sql
    
   Next you will need to connect to the news database and create each of the 5 views provided at the beginning of this README:
   
    vagrant@vagrant:/vagrant$ psql news
    
    news=> [input create view statements here]
       
   After you have created the views in the database, you can execute the program using the following command:
   
    vagrant@vagrant:/vagrant$ python3 logAnalysis.py
    
### Results:
   Once the program finishes running you will now have a logsAnalysis_results.txt file located in your shared /vagrant directory.
   
   This file will contain the output of the logAnalysis.py program.

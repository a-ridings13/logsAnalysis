#Logs Analysis Project

This is a program used to query a PostgreSQL database and then print the results to a plain text file.


4 Total Views Created:
   - articles_viewcount
   - authors_viewcount
   - total_status
   - error_date
 
SQL for create views used:
 
 create view articles_viewcount as select title, count(path) as views from articles, log where articles.slug like substr(log.path, 10) group by title order by count(path) desc limit 3;

 create view authors_viewcount as select name, sum(views) as view_count from (select name, title, count(path) as views from articles, authors, log where articles.slug like substr(log.path, 10) AND articles.author = authors.id group by title, name order by count(path) desc limit 10) as authors_count group by name order by view_count desc;

 create view total_status as select time::date as day, count(status) as total_status_count from log group by day;
 
 create view error_date as select error_status.day, (((error_status.error_count*1.0) / total_status.total_status_count) * 100)::numeric(12,2) as percentage from error_status, total_status where error_status.day = total_status.day;

Design of code:
The design of the Python code follows and adheres to the PEP 8 style guide.

How to execute:
   * First you will need to ensure the "news" database is running on your vagrant machine.
   * Place the logAnalysis.py file into your shared /vagrant directory
   
   Open a terminal and cd to your /vagrant directory and run the command:

    vagrant ssh
    
   Your terminal will now look like the following:

    vagrant@vagrant:$
   
   Next, cd into the /vagrant directory on vagrant box terminal.
   
    vagrant@vagrant:$ cd /vagrant
    
   From here you can execute the program using the following command:
   
    vagrant@vagrant:/vagrant$ python3 logAnalysis.py
    
Results:
   Once the program finishes running you will now have a logsAnalysis_results.txt file located in your shared /vagrant directory.
   
   This file will contain the output of the logAnalysis.py program.

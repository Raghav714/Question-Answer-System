# Question-Answer-System
It was the part of CS200 my 4th Semester Course work. The domain on which the system was trained was freedom fighters biography.
The whole system was divided into 2 parts that is text processor and question processor.

In Text processor the Standford Tools to extract the named entity and relation between those entity was used. The obtanied tuple was stored in PGSQL database. This is the method by which i converted the unstructed data to structed data.

In question processor first the question were classified into o


In this You Need to download the NER and OPENIE tools from standford site given on below link
https://nlp.stanford.edu/software/openie.html and https://nlp.stanford.edu/software/CRF-NER.shtml

# PgSQL
You need to download pgsql in your system and conf it according to your need.
sudo apt-get install postgresql

create the database and table as given in the code.

# how to run it
$ python entry.py

$ python askques.py
# Result
you can see few result of the system in result.txt

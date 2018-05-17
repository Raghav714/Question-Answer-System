from __future__ import print_function
import os
from argparse import ArgumentParser
from subprocess import Popen
from sys import argv
from sys import stderr
import numpy as np
import psycopg2
JAVA_BIN_PATH = 'java'
DOT_BIN_PATH = 'dot'
STANFORD_IE_FOLDER = 'stanford-openie'
tmp_folder = '/tmp/openie/'
Aug0=[]
Rel=[]
Aug1=[]
if not os.path.exists(tmp_folder):
    os.makedirs(tmp_folder)
def arg_parse():
    arg_p = ArgumentParser('Stanford IE Python Wrapper')
    arg_p.add_argument('-f', '--filename', type=str, default=None)
    return arg_p
def process_entity_relations(entity_relations_str):
    # format is ollie.
    entity_relations = list()
    for s in entity_relations_str:
        entity_relations.append(s[s.find("(") + 1:s.find(")")].split(';'))
    return entity_relations
def stanford_ie(input_filename):
    out = tmp_folder + 'out.txt'
    input_filename = input_filename.replace(',', ' ')
    new_filename = ''
    for filename in input_filename.split():
        if filename.startswith('/'):  # absolute path.
            new_filename += '{} '.format(filename)
        else:
            new_filename += '../{} '.format(filename)
    absolute_path_to_script = os.path.dirname(os.path.realpath(__file__)) + '/'
    command = 'cd {};'.format(absolute_path_to_script)
    command += 'cd {}; {} -mx4g -cp "stanford-openie.jar:stanford-openie-models.jar:lib/*" ' \
               'edu.stanford.nlp.naturalli.OpenIE {} -format ollie > {}'. \
        format(STANFORD_IE_FOLDER, JAVA_BIN_PATH, new_filename, out)
    java_process = Popen(command, stdout=stderr, shell=True)
    java_process.wait()
    assert not java_process.returncode, 'ERROR: Call to stanford_ie exited with a non-zero code status.'
    with open(out, 'r') as output_file:
        results_str = output_file.readlines()
    os.remove(out)
    results = process_entity_relations(results_str)
    return results
def main(args):
    arg_p = arg_parse().parse_args(args[1:])
    filename = arg_p.filename
    if filename is None:
        print('please provide a text file containing your input. Program will exit.')
        exit(1)
    entities_relations = stanford_ie(filename)
    X = np.array(entities_relations)
    for p in range(0,len(X)):
    	Aug0.append(X[p][0])
    	Rel.append(X[p][1])
    	Aug1.append(X[p][2])
    print(entities_relations)
    conn = psycopg2.connect(database="project", user = "postgres",password = "root", host = "127.0.0.1", port = "5432")
    print("Opened database successfully")
    cur = conn.cursor()
    for i in range(0,len(Aug0)):
    	cur.execute("select * from mg where aug1 similar to'"+Aug1[i].lstrip().lower()+"'and rel similar to'"+Rel[i].lstrip().lower()+"'or aug0 similar to'"+Aug0[i].lstrip().lower()+"';")
    rows = cur.fetchall()
    for j in range(0,len(rows)):
    	ans=rows[j][0]+" "+rows[j][1]+" "+rows[j][2]
    	print (ans)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    exit(main(argv))

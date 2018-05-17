from nltk.tag import StanfordNERTagger
from itertools import groupby
x = ''
crps = open("maha.txt", "r")
stanford_ner_dir = '/home/raghav/NLP/Project/stanford-ner-2018-02-27/'
eng_model_filename= stanford_ner_dir + 'classifiers/english.muc.7class.distsim.crf.ser.gz'
my_path_to_jar= stanford_ner_dir + 'stanford-ner.jar'
st = StanfordNERTagger(model_filename=eng_model_filename, path_to_jar=my_path_to_jar) 
for line in crps:
	x = str(x) + line
netagged_word=st.tag(x.split())
for tag, chunk in groupby(netagged_word, lambda x:x[1]):
	if (tag != "O"):
		print("%-12s"%tag, " ".join(w for w, t in chunk))

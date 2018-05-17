question = raw_input("Enter the Question:-\n")
question.lower()
qtype=["what","where","when","who","how much"]
atype=["x","pl","d","pe","no"]
for i in range(0,len(qtype)):
	question = question.replace(qtype[i],atype[i])
fh = open("question.txt","w")
fh.write(question)
fh.close()

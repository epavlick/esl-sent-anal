"""Methods for organizing and analyzing control sentences' introduced errors and turkers responses to those errors"""

#Get the raw counts for each type of error
def get_counts(data):
	ret = {'insert' : 0, 'delete' : 0, 'change' : 0}
	for hit in data:
		for sent in data[hit]:
			for error in data[hit][sent]:
				mode = error[' mode'].strip()
				ret[mode] += 1
	print ret
	return ret
	
#Average number of errors per sentence
def avgnumerr(data):
	total = 0
	errs = 0
	for hit in data:
		for sent in data[hit]:
			total += 1
			for error in data[hit][sent]:
				errs += 1
	return float(errs) / total

#Average number of turker-made corrections per sentence
def avgnumcorr(data):
	total = 0
	corr = 0
	for assign in data:
		for sent in data[assign]:
			total += 1
			for error in data[assign][sent]:
				corr += 1
	return float(corr) / total

#get the number of times each sentence was assigned to a worker for editing
def numassign(data):
	sents = {}
	for assign in data:
		for sent in data[assign]:
			if(not(sent in sents)):
				sents[sent] = 1
			else:	
				sents[sent] += 1
	print sents 
	return sents 




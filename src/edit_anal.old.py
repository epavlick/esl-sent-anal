import edit_graph

def agreement(revs):
	average_counts(change_count_by_rev(revs), "change")

#return map of {sent# : rev# : [list of {word#: # of each kind of change}]}
def change_count_by_rev(revs):
	chart = {}
	for n in revs:
		chart[n] = {}
        	for s in revs[n]:
			chart[n][s.id] = {}
			alts = s.get_alterations()
        	        for e in alts:
				chart[n][s.id][e] = {"change" : 0, "insert" : 0, "reorder" : 0, "delete" : 0}
				for ee in alts[e]:
					chart[n][s.id][e][ee.mode.strip()] += 1
					if(chart[n][s.id][e][ee.mode.strip()] > 4):
						print "!!!!!!!!!", n 
	return change_count_by_sent(chart)

#return map of {#revs : {sent# : [list of {word#: # of each kind of change}]}}
def change_count_by_sent(by_rev):
	by_sent = {}
	retmap = {1 : {}, 2 : {}, 3 : {}, 4 : {}}
	for sent in by_rev:
		tot = 0
		by_sent[sent] = {}
		for rev in by_rev[sent]:
			tot += 1
			for word in by_rev[sent][rev]:
				if(not(word in by_sent[sent])):
					by_sent[sent][word] = by_rev[sent][rev][word]				
				else:	
					for mode in by_rev[sent][rev][word]:				
						by_sent[sent][word][mode] += by_rev[sent][rev][word][mode]				
		retmap[tot][sent] = by_sent[sent]
#	for s in retmap:
#		print s, retmap[s]
	return retmap	


def average_counts(tbl, mode):
	#for sentences with n of 1, 2, 3, and 4
	for n in tbl:
		edits = 0
		words = 0
		for sent in tbl[n]:
			words += 1 
			for word in tbl[n][sent]:
				#print tbl[n][sent][word][mode]	
				edits += tbl[n][sent][word][mode]	
		#print n, edits, words

"""
	avgs = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
	tots = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
	for sent in tbl:
		for word in tbl[sent][1]:
			num_edits = tbl[sent][1][word][mode]
			num_views = tbl[sent][0]
			avgs[num_views] += (float(num_edits)/num_views) 
			if(num_edits > 0):
				tots[num_views] += 1

	print avgs
	print tots
def word_change_counts(tbl, m):
	irrs = {}
	totals = {}
	#for each sentence
	for sent in tbl:
		irrs[sent] = [] 
		num_view = 0
		k = tbl[sent].keys()
		word_counts = [0] * len(tbl[sent][k[0]])
		#for each edit of that sentence
		for rev in tbl[sent]:
			num_view += 1
			#for each word in that sentence
			for word in tbl[sent][rev]:
				#count number of times each word was changed
				if(tbl[sent][rev][word][m] > 0):
					word_counts[word] += 1
		print num_view, word_counts	
		#divide by total number of times it was viewed by an editor
		avg_counts = [float(w)/num_view for w in word_counts]
		irrs[sent] = [num_view, avg_counts]
	#return map of {sentence : n , [list of %changes by word]}
#	for i in irrs:
#		print i, irrs[i]
	return irrs

def counts_by_n(change_counts):
	counts = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
	totals = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
	for sent in change_counts:
		for w in change_counts[sent][1]:
		#	print w
			counts[change_counts[sent][0]] += w
			totals[change_counts[sent][0]] += 1 
	print counts
	print totals
#	print {n : [total, float(counts[n])] for n in counts}
				
"""
#given that a word is edited once by mode m, what percent of editors edit it by mode m?
						
					

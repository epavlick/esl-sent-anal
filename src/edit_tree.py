import csv
import sys

#edit object containing information about an atomic change made to a sentence
class Edit:
	def __init__(self):
		self.seq_id= 0
		self.sp_start = 0
		self.sp_end = 0
		self.old_wd = 0
		self.new_wd = 0
		self.mode = 0

#given a row from the data table, return a map of sent_id: edit 
def get_edit(dt_row):
	edit = Edit()
	edit.seq_id = dt_row[' edit_num']
	edit.sp_start = dt_row[' span_start']
	edit.sp_end = dt_row[' span_end']
	edit.old_wd = dt_row[' old_word']
	edit.new_wd = dt_row[' new_word']
	edit.mode = dt_row[' edit_type']
	return {dt_row[' esl_sentence_id'] : edit}



## --- begin main --- ##

if(len(sys.argv) < 2):
	print "usage: provide path to edit_data and sent_ids"
	exit(0)

edit_data = open(sys.argv[1]+"/edit_data")
sent_data = open(sys.argv[1]+"/sent_ids")

raw_edits = csv.DictReader(edit_data)
raw_sents = csv.DictReader(sent_data)

#mapping from assignment: [list of {sentence: [list of edits]}]
all_edits = {}
for e in raw_edits: 
	assign = e[' assignment_id']
	if(not(assign == "")): 
		if(not(assign in all_edits)): 
			all_edits[assign] = {}
	edit = get_edit(e)
	sent = edit.keys()[0]
	if(not(sent == "")):
		if(not(sent in all_edits[assign])):
			all_edits[assign][sent] = [edit[sent]]
		else:
			all_edits[assign][sent].append(edit[sent])
		
for e in all_edits:
	print e + " " + str(all_edits[e])	

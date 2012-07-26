import csv
import sys
import rebuild_sents
import edit_graph

#edit object containing information about an atomic change made to a sentence
class Edit:
	def __init__(self):
		self.seq_id= 0
		self.sp_start = 0
		self.sp_end = 0
		self.old_wd = 0
		self.new_wd = 0
		self.mode = 0
	def __str__(self):
		return "[{id: %s}, {start: %s}, {end: %s}, {old: %s}, {new: %s}, {mode: %s}]" % (self.seq_id, self.sp_start, self.sp_end, self.old_wd, self.new_wd, self.mode)
	def __repr__(self):
		return "[{id: %s}, {start: %s}, {end: %s}, {old: %s}, {new: %s}, {mode: %s}]" % (self.seq_id, self.sp_start, self.sp_end, self.old_wd, self.new_wd, self.mode)
	def __cmp__(self, other):
		return (int(self.seq_id) - int(other.seq_id))	


#given a row from the data table, return a map of sent_id: edit 
def get_edit(dt_row):
	edit = Edit()
	edit.seq_id = dt_row[' edit_num']
	edit.sp_start = dt_row[' span_start']
	edit.sp_end = dt_row[' span_end']
	edit.old_wd = dt_row[' old_word']
	edit.new_wd = dt_row[' new_word']
	edit.mode = dt_row[' edit_type']
	return {dt_row[' esl_sentence_id'].strip() : edit}


def build_edit_map(edit_data, sent_data):
	raw_edits = csv.DictReader(edit_data)
	#mapping from assignment: [list of {sentence: [list of edits]}]
	all_edits = {}
	for e in raw_edits: 
		assign = e[' assignment_id'].strip()
		if(not(assign == "")): 
			if(not(assign in all_edits)): 
				all_edits[assign] = {}
		edit = get_edit(e)
		sent = edit.keys()[0].strip()
		if(not(sent == "")):
			if(not(sent in all_edits[assign])):
				all_edits[assign][sent] = [edit[sent]]
			else:
				all_edits[assign][sent].append(edit[sent])
	return all_edits		

def build_sent_map(sent_data):
	raw_sents = csv.DictReader(sent_data)
	all_sents = {}
	for s in raw_sents:
		all_sents[s['id']] = s[' sentence']	
	return all_sents

	

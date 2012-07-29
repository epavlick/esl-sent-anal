import rebuild_sents
import figures
import sys

#edit object containing information about an atomic change made to a sentence
class Node:
	id_num = 0
	
	@staticmethod
	def print_list(nodes):
		for n in nodes:
			if(isinstance(n, Node)):
				if(n.is_root):
					print str(n),
				else:
					print str(n) + '<-',
			else:
				Node.print_list(n)

	def __init__(self, _pos, _parent, _text, _blank,):
		#id (unique within sentence)
		self.id = Node.id_num
		self.pos = _pos
		#id of parent in previous revision
		assert isinstance(_parent, list)
		self.parent = _parent
		self.children = [] 
		self.alterations = []
		self.is_blank = _blank
		if(_parent == [None]):
			self.is_root = True
		else:
			self.is_root = False
		#word in sentence
		self.text = _text
		Node.id_num +=1
	
	def __str__(self):
		if(self.is_root):
			return '[ Head ]'
		else:
			pid = str(self.parent[0].pos) + '-' + str(self.parent[len(self.parent)-1].pos)
			return '[pos:'+str(self.pos)+' parent:'+ str(pid) +' '+str(self.text)+']'
	
	def add_child(self, node):
		self.children.append(node)
	
	def alter(self, mode):
		self.alterations.append(mode)
		if(not(self.is_root)):
			for p in self.parent:
				p.alter(mode)
	
	def lineage(self):
		l = [self]
		par = self.parent
		if(self.is_root):
			return [self]
		else:
			for p in par:
				l.append(p.lineage())
		return l
	
	def get_fate(self):
		fate = {self : {}}
		if(self.children == []):
			return fate
		else:
			for c in self.children:
				fate[self][c] = c.get_fate()
		return fate

	def get_alterations(self):
		return self.alterations
	
	def has_changed(self, mode):
		for a in self.alterations:
			if(a.mode == mode):
				return True
		return False

class Sentence:
	id_num = 0
	def __init__(self, sent):
		self.id = Sentence.id_num
		self.head = Node(0, [None], "Head", False)
		#list of revisions
		self.revisions = []
		self.latest = 0
		Sentence.id_num += 1
	def revise(self, edit):
#		for r in self.revisions:
#			print str(r),
#		print
		last_revision = self.revisions[self.latest]
		new = last_revision.revise(edit)
		self.revisions.append(new)
		self.latest += 1	
	def clean_print(self):
		print '['+str(self.head.text)+']'
		for r in self.revisions:
			s = ""
			for w in r.words:
				s += '['+w.text+']'
			print s

	def print_sent(self):
		for r in self.revisions:
			print str(r)			
	
	def print_final(self, buf=sys.stdout):
		buf.write("Initial: " + str(self.revisions[0])+'\n')
		buf.write("Final: " + str(self.revisions[self.latest])+'\n')
		buf.write('\n')

	def get_fates(self):
		destiny = []
		for node in self.revisions[0].words:
			destiny.append(node.get_fate())
		return destiny
	
	def get_alterations(self):
		alts = {} 
		for node in self.revisions[0].words:
	#		print node.text, node.get_alterations()
			alts[node.pos] = node.get_alterations()
	#	print alts
		return alts

	def __print_fate(self, dct):
		s = ""
		for key in dct:
			if(dct[key] == {}):
				return key.text #str(key)
			else:
				s += key.text + "->"+self.__print_fate(dct[key])
		return s

	def print_fates(self, buf=sys.stdout):
		for f in self.get_fates():
			buf.write(self.__print_fate(f)+'\n')

	def print_alterations(self, buf=sys.stdout):
		for a in self.get_alterations():
			buf.write(str(a)+'\n')
	
	def print_lineage(self, name):
		figures.draw_revisions(self.revisions, "figures-20120726/"+name) # "figures/sent-"+str(self.id))
	
	
class Revision:
	def __init__(self, _num):
		self.num = _num
		#list of nodes
		self.words = []
		self.edit_num = -1

	def __str__(self):
		s = ""
		for w in self.words:
			s += str(w.text) + " "	
		return "{ "+str(self.num)+" "+str(self.edit_num)+" "+s+" }"

	def revise(self, edit):
		e = edit.mode.strip()
		if(e == "change"):
			return self.change(edit)
		if(e == "insert"):
			return self.insert(edit)
		if(e == "reorder"):
			return self.reorder(edit)
		if(e == "delete"):
			return self.delete(edit)
		else:
			return self

	def change(self, edit):
	        new = Revision(self.num + 1)
		ewords = edit.new_wd.split()
		pos = 0
	        for w in self.words[:(2*(int(edit.sp_start))+1)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			w.add_child(node)
			pos += 1
		parent = []
		for w in self.words[(2*(int(edit.sp_start))+1):(2*(int(edit.sp_end)))]:
			parent.append(w)
		if(len(ewords) == 0):
			node = Node(pos, parent, "", True)
			new.words.append(node)
			for p in parent:
				p.add_child(node)
				p.alter(edit)
			pos += 1
		else:
	      		for w in ewords:
				node = Node(pos, parent, w, False)
	                	new.words.append(node)
				for p in parent:
					p.add_child(node)
					p.alter(edit)
				pos += 1
				if(len(ewords)>1 and w != ewords[len(ewords)-1]):#if adding multiple words, put spaces between them
					n = Node(pos, parent, "", True)
					new.words.append(n)
					for p in parent:
						p.add_child(node)
						p.alter(edit)
					pos += 1
	        for w in self.words[(2*(int(edit.sp_end))): len(self.words)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			w.add_child(node)
			pos += 1
		new.edit_num = edit.seq_id
		return new 

	def insert(self, edit):
        	new = Revision(self.num + 1)
		ewords = edit.new_wd.split()
		pos = 0
		for w in self.words[:(2*(int(edit.sp_start))+1)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			w.add_child(node)
			pos += 1
	        for w in ewords:
			if(2*(int(edit.sp_start)) < len(self.words)):
				parent = self.words[2*(int(edit.sp_start))]
			else:
				parent = self.words[len(self.words) - 1]
			node = Node(pos, [parent], w, False)
	                new.words.append(node)
			parent.add_child(node)
			parent.alter(edit)
			pos += 1
			node = Node(pos, [parent], "", True)
	                new.words.append(node)
			parent.add_child(node)
			parent.alter(edit)
			pos += 1
	        for w in self.words[(2*(int(edit.sp_start))+1): len(self.words)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			w.add_child(node)
			pos += 1
		new.edit_num = edit.seq_id
		return new

	def reorder(self, edit):
		if(int(edit.sp_start) <= int(edit.new_wd)):
                	return self.__move_forward(edit)
        	else:
                	return self.__move_back(edit)

	def __move_back(self, edit):
		new = Revision(self.num + 1)
	        ewords = self.words[(2*(int(edit.sp_start))+1):(2*(int(edit.sp_end))+1)]
		pos = 0
	        for w in self.words[:(2*(int(edit.new_wd))+1)]:
	        	node = Node(pos, [w], w.text, w.is_blank)	
		        new.words.append(node)
			w.add_child(node)
			pos += 1
		onode = 2*(int(edit.sp_start))+1
	        for w in ewords:
	        	node = Node(pos, [self.words[onode]], w.text, w.is_blank)
		        new.words.append(node)
			self.words[onode].add_child(node)
			self.words[onode].alter(edit)
			onode += 1	
			pos += 1
	        for w in self.words[(2*(int(edit.new_wd))+1):(2*(int(edit.sp_start))+1)]:
			node = Node(pos, [w], w.text, w.is_blank)	
		        new.words.append(node)
			w.add_child(node)
			pos += 1
	        for w in self.words[(2*(int(edit.sp_end))+1):]:
	        	node = Node(pos, [w], w.text, w.is_blank)	
		        new.words.append(node)
			w.add_child(node)
			pos += 1
		new.edit_num = edit.seq_id
		return new

	def __move_forward(self, edit):
		new = Revision(self.num + 1)
	        ewords = self.words[(2*(int(edit.sp_start))+1):(2*(int(edit.sp_end))+1)]
	        pos = 0
		for w in self.words[:(2*(int(edit.sp_start))+1)]:
	        	node = Node(pos, [w], w.text, w.is_blank)	
		        new.words.append(node)
			w.add_child(node)
			pos += 1
	        for w in self.words[(2*(int(edit.sp_end))+1):(2*(int(edit.new_wd))+1)]:
			node = Node(pos, [w], w.text, w.is_blank)	
		        new.words.append(node)
			w.add_child(node)
			pos += 1
		onode = 2*(int(edit.sp_start))+1
	        for w in ewords:
	        	node = Node(pos, [self.words[onode]], w.text, w.is_blank)
		        new.words.append(node)
			self.words[onode].add_child(node)
			self.words[onode].alter(edit)
			onode += 1	
			pos += 1
	        for w in self.words[(2*(int(edit.new_wd))+1):]:
			node = Node(pos, [w], w.text, w.is_blank)	
		        new.words.append(node)
			w.add_child(node)
			pos += 1
		new.edit_num = edit.seq_id
		return new

	def delete(self, edit):
        	new = Revision(self.num + 1)
		ewords = edit.new_wd.split()
		pos = 0
		for w in self.words[:(2*(int(edit.sp_start))+1)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			w.add_child(node)
			pos += 1
		for w in self.words[(2*(int(edit.sp_start))+1):(2*(int(edit.sp_end))+1)]:
			w.alter(edit)		
	        for w in self.words[(2*(int(edit.sp_end))+1): len(self.words)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			w.add_child(node)
			pos += 1
		new.edit_num = edit.seq_id
		return new

class EditGraph:
	def __init__(self, graph):
		self.data = graph
	
	def get_edits(self, sentid=None):
		edits = {}
		if(sentid==None):
			for assign in self.data:
				edits[assign] = [] 
				for s in self.data[assign]:
					for edit in self.data[assign][s]:
						edits[assign].append(edit)
		else:
			for assign in self.data:
				edits[assign] = [] 
				if sentid in self.data[assign]:
					for edit in self.data[assign][sentid]:
						edits[assign].append(edit)
		return edits
			 
class RevisionGraph:
	"""Highest level data structure containing map from sentence id to all the revisions on that sentence"""
	def __init__(self, graph):
		self.data = graph
	
	def get_revisions(self, sentid=None):
		revs = []
		if(sentid==None):
			for s in self.data:
				for r in self.data[s]:
					revs.append(r)
		else:
			for r in self.data[sentid]:
				revs.append(r)
		return revs

def initialize_sentence(sent):
	words = sent.split()
	graph = Sentence(sent)
	rev = Revision(0) 
	pos = 0
	n = Node(pos, [graph.head], "", True)
	pos += 1
	rev.words.append(n)
	for w in words:
		n = Node(pos, [graph.head], w, False)
		rev.words.append(n)
		pos += 1
		n = Node(pos, [graph.head], "", True)
		rev.words.append(n)
		pos += 1
	graph.revisions.append(rev)
	return graph

def generate_figures(graph, sentid=None):
   	if(sentid==None):
		for s in graph:
			s.print_lineage(str(s.id))
        else:
		i = 0
	        for s in graph[sentid]:
        	        s.print_lineage(sentid+'.'+str(i))
        	        i += 1
	
def get_graph(all_sents, all_edits):
	graph_by_sent = {}
	edits_by_sent = {}
	for assign in all_edits:
		if(not(assign in edits_by_sent)):
			edits_by_sent[assign] = {}
		for sent in all_edits[assign]:
			if(not(sent in graph_by_sent)):
				graph_by_sent[sent] = []
			if(not(sent in edits_by_sent[assign])):
				edits_by_sent[assign][sent] = []
			if(sent != None):
				start = all_sents[sent].strip()
				start = start.strip('"')
				s = initialize_sentence(start)
				these_edits = all_edits[assign][sent]
				these_edits.sort()
				for edit in these_edits:
				#	if(not(len(start.split())==0)):
					s.revise(edit)
					edits_by_sent[assign][sent].append(edit)
				graph_by_sent[sent].append(s)	
	return [RevisionGraph(graph_by_sent), EditGraph(edits_by_sent)]

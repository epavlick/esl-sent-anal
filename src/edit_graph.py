import rebuild_sents
import figures

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
					print str(n)# + '<-',
			else:
				Node.print_list(n)

	def __init__(self, _pos, _parent, _text, _blank):
		#id (unique within sentence)
		self.id = Node.id_num
		self.pos = _pos
		#id of parent in previous revision
		assert isinstance(_parent, list)
		self.parent = _parent
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
			return '[pos:'+str(self.pos)+' parent:'+ pid +' '+self.text+']'
	
	def lineage(self):
		l = [self]
		par = self.parent
		if(self.is_root):
			return [self]
		else:
			for p in par:
			#	print "p is "+str(p)
				l.append(p.lineage())
		return l

class Sentence:
	def __init__(self, sent):
		self.head = Node(0, [None], "Head", False)
		#list of revisions
		self.revisions = []
		self.latest = 0
	def revise(self, edit):
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
	
	def print_final(self):
		print "Initial: " + str(self.revisions[0])
		print "Final: " + str(self.revisions[self.latest])
	
	def print_lineage(self):
		figures.draw_revisions(self.revisions)
#		for r in self.revisions:
#			print '----' + str(r.num) + '----'
#			for w in r.words:
#				Node.print_list(w.lineage())
#				print
#			print
	
	
class Revision:
	def __init__(self, _num):
		self.num = _num
		#list of nodes
		self.words = []

	def __str__(self):
		s = ""
		for w in self.words:
			s += str(w.text) + " "	
		return "{ "+str(self.num)+" "+s+" }"

	def revise(self, edit):
		if(edit.mode == "change"):
			return self.change(edit)
		if(edit.mode == "insert"):
			return self.insert(edit)
		if(edit.mode == "reorder"):
			return self.reorder(edit)
		if(edit.mode == "delete"):
			return self.delete(edit)

	def change(self, edit):
	        new = Revision(self.num + 1)
		ewords = edit.new_wd.split()
		pos = 0
	        for w in self.words[:(2*(int(edit.sp_start))+1)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			pos += 1
		parent = []
		for w in self.words[(2*(int(edit.sp_start))+1):(2*(int(edit.sp_end))+1)]:
			parent.append(w)
	        for w in ewords:
			node = Node(pos, parent, w, False)
	                new.words.append(node)
			pos += 1
			if(len(ewords)>1 and w != ewords[len(ewords)-1]):#if adding multiple words, put spaces between them
				n = Node(pos, parent, "", True)
				new.words.append(n)
				pos += 1
	        for w in self.words[(2*(int(edit.sp_end))): len(self.words)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			pos += 1
	        return new 

	def insert(self, edit):
        	new = Revision(self.num + 1)
		ewords = edit.new_wd.split()
		pos = 0
		for w in self.words[:(2*(int(edit.sp_start))+1)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			pos += 1
	        for w in ewords:
			parent = self.words[2*(int(edit.sp_start))]
			node = Node(pos, [parent], w, False)
	                new.words.append(node)
			pos += 1
			node = Node(pos, [parent], "", True)
	                new.words.append(node)
			pos += 1
	        for w in self.words[(2*(int(edit.sp_start))+1): len(self.words)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			pos += 1
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
			pos += 1
	        for w in ewords:
			onode = int(edit.sp_start)
	        	node = Node(pos, [self.words[onode]], w.text, w.is_blank)
			onode += 1	
		        new.words.append(node)
			pos += 1
	        for w in self.words[(2*(int(edit.new_wd))+1):(2*(int(edit.sp_start))+1)]:
			node = Node(pos, [w], w.text, w.is_blank)	
		        new.words.append(node)
			pos += 1
	        for w in self.words[(2*(int(edit.sp_end))+1):]:
	        	node = Node(pos, [w], w.text, w.is_blank)	
		        new.words.append(node)
			pos += 1
		return new

	def __move_forward(self, edit):
		new = Revision(self.num + 1)
	        ewords = self.words[(2*(int(edit.sp_start))+1):(2*(int(edit.sp_end))+1)]
	        pos = 0
		for w in self.words[:(2*(int(edit.sp_start))+1)]:
	        	node = Node(pos, [w], w.text, w.is_blank)	
		        new.words.append(node)
			pos += 1
	        for w in self.words[(2*(int(edit.sp_end))+1):(2*(int(edit.new_wd))+1)]:
			node = Node(pos, [w], w.text, w.is_blank)	
		        new.words.append(node)
			pos += 1
	        for w in ewords:
			onode = int(edit.sp_start)
	        	node = Node(pos, [self.words[onode]], w.text, w.is_blank)
			onode += 1	
		        new.words.append(node)
			pos += 1
	        for w in self.words[(2*(int(edit.new_wd))+1):]:
			node = Node(pos, [w], w.text, w.is_blank)	
		        new.words.append(node)
			pos += 1
		return new

	def delete(self, edit):
        	new = Revision(self.num + 1)
		ewords = edit.new_wd.split()
		pos = 0
		for w in self.words[:(2*(int(edit.sp_start))+1)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			pos += 1
	        for w in self.words[(2*(int(edit.sp_end))+1): len(self.words)]:
			node = Node(pos, [w], w.text, w.is_blank)
	                new.words.append(node)
			pos += 1
		return new
			 
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
	
def get_graph(all_sents, all_edits):
#	k = all_sents.keys()
#	initialize_sentence(all_sents[k[0]])
	graph = []
	for assign in all_edits:
		for sent in all_edits[assign]:
			if(sent in all_sents):
				start = all_sents[sent].strip()
				start = start.strip('"')
				s = initialize_sentence(start)
				#s.print_sent()
				these_edits = all_edits[assign][sent]
				these_edits.sort()
				for edit in all_edits[assign][sent]:
					if(not(len(start.split())==0)):
						s.revise(edit)
					#	start = rebuild_sents.do_edit(start, edit)
			#	s.print_final()
				graph.append(s)		
	
	graph[1].print_lineage()	
	#for s in graph:
	#	s.print_lineage()
	

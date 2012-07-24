import rebuild_sents

#edit object containing information about an atomic change made to a sentence
class Node:
	id_num = 0
	def __init__(self, _parent, _text):
		#id (unique within sentence)
		self.id = Node.id_num
		#id of parent in previous revision
		self.parent = _parent
		if(_parent == None):
			self.is_root = True
		#revision number (when this word/change was introduced)
		#self.rev = _rev
		#word in sentence
		self.text = _text
		Node.id_num +=1
	def __str__(self):
		pid = str(self.parent[0].id) + ' - ' + str(self.parent[len(self.parent)-1].id)
		return '[id: '+str(self.id)+', parent: '+ pid +', text: '+self.text+']'

class Sentence:
	def __init__(self, sent):
		self.head = Node([None], "Head")
		#list of revisions
		self.revisions = []
	#	self.revisions.append(Revision(0, sent.split()))
		self.latest = 0
	def revise(self, edit):
		last_revision = self.revisions[self.latest]
#		print "Old: " + str(last_revision)
		new = last_revision.revise(edit)
#		print "New: " + str(new)
		self.revisions.append(new)
		self.latest += 1		
	def print_sent(self):
		for r in self.revisions:
			print str(r)			
	def print_final(self):
		print "Initial: " + str(self.revisions[0])
		print "Final: " + str(self.revisions[self.latest])
	
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
	        for w in self.words[:int(edit.sp_start)]:
			node = Node([w], w.text)
	                new.words.append(node)
		parent = []
		for p in range(int(edit.sp_start), int(edit.sp_end)):
			parent.append(self.words[p])
	        for w in ewords:
	        	node = Node(parent, w)
	                new.words.append(node)
	        for p in range(int(edit.sp_end), len(self.words)):
			node = Node([self.words[p]], self.words[p].text)
	                new.words.append(node)
	        return new 

	def insert(self, edit):
        	new = Revision(self.num + 1)
		ewords = edit.new_wd.split()
		for p in range(0, int(edit.sp_start)):
			node = Node([self.words[p]], self.words[p].text)
	                new.words.append(node)
	        for w in ewords:
			node = Node(None, w)
	                new.words.append(node)
	        for p in range(int(edit.sp_start), len(self.words)):
			node = Node([self.words[p]], self.words[p].text)
	                new.words.append(node)
		return new

	def reorder(self, edit):
		if(int(edit.sp_start) <= int(edit.new_wd)):
                	return self.__move_forward(edit)
        	else:
                	return self.__move_back(edit)

	def __move_back(self, edit):
		new = Revision(self.num + 1)
	        ewords = self.words[int(edit.sp_start):int(edit.sp_end)]
	        for w in self.words[:int(edit.new_wd)]:
	        	node = Node([w], w.text)	
		        new.words.append(node)
	        for w in ewords:
			onode = int(edit.sp_start)
	        	node = Node([self.words[onode]], w.text)
			onode += 1	
		        new.words.append(node)
	        for w in self.words[int(edit.new_wd):int(edit.sp_start)]:
			node = Node([w], w.text)	
		        new.words.append(node)
	        for w in self.words[int(edit.sp_end):]:
	        	node = Node([w], w.text)	
		        new.words.append(node)
		return new

	def __move_forward(self, edit):
		new = Revision(self.num + 1)
	        ewords = self.words[int(edit.sp_start):int(edit.sp_end)]
	        for w in self.words[:int(edit.sp_start)]:
	        	node = Node([w], w.text)	
		        new.words.append(node)
	        for w in self.words[int(edit.sp_end):int(edit.new_wd)]:
			node = Node([w], w.text)	
		        new.words.append(node)
	        for w in ewords:
			onode = int(edit.sp_start)
	        	node = Node([self.words[onode]], w.text)
			onode += 1	
		        new.words.append(node)
	        for w in self.words[int(edit.new_wd):]:
			node = Node([w], w.text)	
		        new.words.append(node)
		return new

	def delete(self, edit):
        	new = Revision(self.num + 1)
		ewords = edit.new_wd.split()
		for p in range(0, int(edit.sp_start)):
			node = Node([self.words[p]], self.words[p].text)
	                new.words.append(node)
	        for p in range(int(edit.sp_end), len(self.words)):
			node = Node([self.words[p]], self.words[p].text)
	                new.words.append(node)
		return new
			 
def initialize_sentence(sent):
	words = sent.split()
	graph = Sentence(sent)
	rev = Revision(0) 
	for w in words:
		n = Node([graph.head], w)
		rev.words.append(n)
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
			s.print_final()
			graph.append(s)		
		

	

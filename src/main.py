import extract_data
import sys
import edit_graph

if(len(sys.argv) < 2):
        print "usage: provide path to edit_data and sent_ids"
        exit(0)

print "reading data from " + sys.argv[1] + "..."

edit_data = open(sys.argv[1]+"/edit_data")
sent_data = open(sys.argv[1]+"/sent_ids")

print "building edit map..."
all_edits = extract_data.build_edit_map(edit_data, sent_data)

print "building sentence map..."
all_sents = extract_data.build_sent_map(sent_data)


print "generating graph data structure..."
graph = edit_graph.get_graph(all_sents, all_edits)

rgraph = graph[0]
egraph = graph[1]

edits = egraph.get_edits('45403')

for a in edits:
	for e in edits[a]:
		print str(a), str(e)

for r in rgraph.get_revisions('45403'):
	r.print_sent()

print "FINISH"

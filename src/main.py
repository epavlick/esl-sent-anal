import extract_data
import sys
import edit_graph
import edit_anal
import figures 

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

#figures.plot_agreements(edit_anal.agreement(rgraph.data), path="figures/agreement")

#figures.plot_modes(edit_anal.by_mode(rgraph.data), path="figures/agreement")
data = edit_anal.by_pos(rgraph.data)[3]
new_data = {}
for m in data:
	new_data[m] = {}
	for p in data[m]:
		if(not(p == 'BLANK')):
			new_data[m][p] = data[m][p]
print new_data
print "generating figures..."
figures.plot_pos(new_data, path="figures/agreement")

"""

print "writing final sentences to log..."
log = open("edits.log", "w")


for r in rgraph.get_revisions():
	#log.write(str(r.id)+" ")
	#r.print_final(log)
	print r.get_alterations(pos=True)
log.close()

#print "generating figures..."
#i = 0
#for s in rgraph.data:
#	if(i%10==0):
#	edit_graph.generate_figures(rgraph.data, s)
#	i += 1	

#edit_graph.generate_figures(rgraph.data, '45480')

for n in rgraph.data:
	log.write("------------"+n+"-----------"+'\n')
	for s in rgraph.data[n]:
		log.write('\n')
		#s.print_fates(log)
		s.print_alterations(log)

log.close()
"""
print "FINISH"

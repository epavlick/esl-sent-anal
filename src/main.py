import extract_data
import sys
import edit_graph
import edit_anal
import figures 
import argparse 
import control_anal

print "Begin main..."

parser = argparse.ArgumentParser()
parser.add_argument('--data', dest='data', help='path to directory containing mturk data dump', action='store', default=False)
parser.add_argument('--controls', dest='controls', help='perform analysis on control data', action='store_true', default=False)
parser.add_argument('--controlsonly', dest='controlsonly', help='perform analysis on control data and not edit data', action='store_true', default=False)

args = parser.parse_args()

if(not(args.data)):
        print "usage: provide path to edit_data and sent_ids"
        exit(0)

print "Reading data from " + args.data + "..."

rgraph = {}
egraph = {}

if(not(args.controlsonly)):
	edit_data = open(args.data+"/edit_data")
	sent_data = open(args.data+"/sent_ids")
	
	all_edits = extract_data.build_edit_map(edit_data, sent_data)

	all_sents = extract_data.build_sent_map(sent_data)

	graph = edit_graph.get_graph(all_sents, all_edits)

	rgraph = graph[0]
	egraph = graph[1]

if(args.controls or args.controlsonly):
	control_data = open(args.data+"/cntrl_data")
	all_controls = extract_data.build_control_map(control_data)
	counts = control_anal.avgnumerr(all_controls)
	print counts
	corrcounts = control_anal.avgnumcorr(egraph.data)
	print corrcounts
	control_anal.numassign(egraph.data)

#Plot the frequency of edit modes, partitioned based on number of redundancies
#figures.plot_modes(edit_anal.by_mode(rgraph.data), path="figures/agreement")

#Plot the agreement between workers, partitioned based on number of redundancies
#figures.plot_agreements(edit_anal.agreement(rgraph.data), path="figures/agreement")
#edit_anal.agreement(rgraph.data)

#print "...edits by pos..."
#data = edit_anal.by_pos(rgraph.data)[3]
###new_data = {}
#for m in data:
#	new_data[m] = {}
#	for p in data[m]:
#		if(not(p == 'BLANK')):
#			new_data[m][p] = data[m][p]
#figures.plot_pos(new_data, path="figures/agreement")

#print "...agreements by pos..."
#figures.plot_agreements_pos(edit_anal.agreement_pos(rgraph.data, n=3), path="figures/agreement")
#edit_anal.agreement_pos(rgraph.data, n=3)

#print "sanity check..."
#edit_anal.sanitycheck()


#print "writing final sentences to log..."
#log = open("edits.log", "w")


#for r in rgraph.get_revisions():
	#log.write(str(r.id)+" ")
#	r.print_final(log)
#	print r.get_alterations(pos=True)
#log.close()

#print "generating figures..."
#i = 0
#for s in rgraph.data:
#	edit_graph.generate_figures(rgraph.data, s)
#	i += 1	

#edit_graph.generate_figures(rgraph.data, '45480')

#for n in rgraph.data:
#	log.write("------------"+n+"-----------"+'\n')
#	for s in rgraph.data[n]:
#		log.write('\n')
#		#s.print_fates(log)
#		s.print_alterations(log)
#
#log.close()

print "FINISH"

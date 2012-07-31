from pyx import *
import numpy as np
import matplotlib.pyplot as plt
import datetime

NODE_WIDTH = 1 
NODE_HEIGHT = 0.5 

def undo_csv_format(string):
    string = string.strip()
    string = string.replace("&amp;", '&')
    string = string.replace("&#44;", ',')
    string = string.replace("&gt;", '>')
    string = string.replace("&lt;", '<')
    string = string.replace("&quot;", '"')
    string = string.replace("&#39;", "'")
    return string

def draw_revisions(revs, name):
	c = canvas.canvas()
	y = len(revs)	
	for r in revs:
		print r
		x = 0
		for w in r.words:
			changed = False
			if(w.is_blank):
				if(not(r == revs[0]) and (len(w.parent) > 1 or w.text != w.parent[0].text)):
				#	changed = True
					c.stroke(path.circle(x + (0.5*NODE_WIDTH), y + (0.5*NODE_HEIGHT), 0.25* NODE_WIDTH))
					c.fill(path.circle(x + (0.5*NODE_WIDTH), y + (0.5*NODE_HEIGHT), 0.25* NODE_WIDTH), [color.rgb.blue])
				else:
					c.stroke(path.circle(x + (0.5*NODE_WIDTH), y + (0.5*NODE_HEIGHT), 0.25* NODE_WIDTH))
			else:
				if(not(r == revs[0]) and (len(w.parent) > 1 or w.text != w.parent[0].text)):
				#	changed = True
					c.stroke(path.rect(x, y, NODE_WIDTH, NODE_HEIGHT))
					c.fill(path.rect(x, y, NODE_WIDTH, NODE_HEIGHT), [color.rgb.blue])
				else:
					c.stroke(path.rect(x, y, NODE_WIDTH, NODE_HEIGHT))

			c.text(x+(0.5*NODE_WIDTH), y+(0.5*NODE_HEIGHT), undo_csv_format(w.text), [text.halign.boxcenter, text.valign.middle])
			if(y < len(revs)): #not the original sentence
				for p in w.parent:
					px = NODE_WIDTH*(p.pos) + (0.5 * NODE_WIDTH)
					py = y + 4*NODE_HEIGHT
					c.stroke(path.line(px, py, x + (0.5 * NODE_WIDTH), y + NODE_HEIGHT))
				#	if(changed):
				#		if p.is_blank:
				#			c.fill(path.circle(px + (0.5*NODE_WIDTH), py + (0.5*NODE_HEIGHT), 0.25* NODE_WIDTH), [color.rgb.blue])
				#		else:	
				#			c.fill(path.rect(px, py, NODE_WIDTH, NODE_HEIGHT), [color.rgb.blue])
			x += 1
		y -= 4*NODE_HEIGHT
	c.writePDFfile(name)

def plot_agreements(data, n=0, path=None):
	fig = plotbyn(data, n, path)
	plt.suptitle("Annotator agreement across edit modes")
	if(not(path==None)):
		dt = datetime.datetime.now()
		name = dt.strftime("agr-%Y-%m-%d-%H:%m:%S")
		plt.savefig(path+"/"+name)
	plt.show()

def plot_pos(data, n=0, path=None):
        fig = plotbypos(data, path)
        plt.suptitle("Parts of speech edited across edit modes")
        if(not(path==None)):
                dt = datetime.datetime.now()
                name = dt.strftime("pos-%Y-%m-%d-%H:%m:%S")
                plt.savefig(path+"/"+name)
        plt.show()
	
def plot_modes(data, n=0, path=None):
	fig = plotbyn(data, n, path)
	plt.suptitle("Number of edits by edit mode")
	if(not(path==None)):
		dt = datetime.datetime.now()
		name = dt.strftime("mod-%Y-%m-%d-%H:%m:%S")
		plt.savefig(path+"/"+name)
	plt.show()
	

def __plotone(data, n, path):
	fig = plt.figure()
	lbls = data[n].keys()
	yax = [data[n][k] for k in lbls]
	xax = range(len(yax)) 
	fig1 = fig.add_subplot(111)
	fig1.bar(xax, yax, align="center")
	fig1.set_xticks(xax)
	fig1.set_xticklabels(lbls)
	fig1.set_title(str(n)+" x redundant")
#	if(not(path==None)):
#		dt = datetime.datetime.now()
#		name = dt.strftime("%Y-%m-%d-%H:%m:%S")
#		plt.savefig(path+"/"+name)
	return fig
	#plt.show()

def plotbypos(data, path=None):
	locs = {'change' : 221, 'insert' : 222, 'delete' : 223, 'reorder' : 224}
        fig = plt.figure()
	for nn in data: 
		lbls = data[nn].keys()
		yax = [data[nn][k] for k in lbls] 
		xax = range(len(yax))
		fig1 = fig.add_subplot(locs[nn]) 
		fig1.bar(xax, yax)#, align="center") 
		fig1.set_xticks(xax) 
		fig1.set_xticklabels(lbls) 
		fig1.set_title(nn)
		plt.setp(fig1.get_xticklabels(), fontsize=8)
		plt.tight_layout()
       # fig.autofmt_xdate()
	return fig

def plotbyn(data, n=0, path=None):
	if(n == 0):
		locs = {1 : 221, 2 : 222, 3 : 223, 4 : 224}
		fig = plt.figure()
		for nn in data:
			lbls = data[nn].keys()
			yax = [data[nn][k] for k in lbls]
			xax = range(len(yax)) 
			fig1 = fig.add_subplot(locs[nn])
			fig1.bar(xax, yax, align="center")
			fig1.set_xticks(xax)
			fig1.set_xticklabels(lbls)
			fig1.set_title(str(nn)+" x redundant")
		return fig
	else:
		__plotone(data, n, path)

	



	

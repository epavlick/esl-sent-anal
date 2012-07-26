from pyx import *

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


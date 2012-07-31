

def byn(data):
	retmap = {1 : {}, 2 : {}, 3 : {}, 4 : {}}
	for sentnum in data:
		count = 0
		for sent in data[sentnum]:
			count += 1
		retmap[count][sentnum] = data[sentnum]
	return retmap


def by_mode(_data):
	data = byn(_data)
	retmap = {1 : {}, 2 : {}, 3 : {}, 4 : {}}
	for n in retmap:
		submap = {"change" : 0, "delete" : 0, "reorder" : 0, "insert" : 0}
		for sentnum in data[n]:
			for sent in data[n][sentnum]:
				alts = sent.get_alterations()
				for a in alts:
					for e in alts[a]:
						submap[e.mode.strip()] += 1
		retmap[n] = submap
	return retmap

def count_words(data, mode, n):
	retmap = {}
	for sentnum in data:
		corrs = {}
		for sent in data[sentnum]:
			alts = sent.get_alterations()
			for a in alts:
				for e in alts[a]:
					if(e.mode.strip() == mode):
						if(not(a in corrs)):
							corrs[a] = 0
						else:
							corrs[a] += 1
						continue
		if(n==1):
			retmap[sentnum] = [float(corrs[idx]) / n for idx in corrs]
		else:	
			retmap[sentnum] = [float(corrs[idx]) / (n - 1) for idx in corrs]
	return retmap
	return retmap

def __agreement(_data, mode, n):
	data = byn(_data)
	chdata = count_words(data[n], mode, n)	
	cntsum = 0
	total = 0
	for num in chdata:
		for c in chdata[num]:
			cntsum += c
			total += 1
	return float(cntsum) / total

	
def agreement(data, mode=None, n=0):
	ns = []
	modes = []
	retmap = {1 : {}, 2 : {}, 3 : {}, 4 : {}}
	if(n == 0):
		ns = [1, 2, 3, 4]
	else:
		ns = [n]
	if(mode == None):
		modes = ["change", "insert", "delete", "reorder"]
	else:
		modes = [mode]			
		
	for nn in ns:
		submap = {"change" : 0, "delete" : 0, "reorder" : 0, "insert" : 0}
		for m in modes:
			submap[m] = __agreement(data, m, nn)
		retmap[nn] = submap
	return retmap
















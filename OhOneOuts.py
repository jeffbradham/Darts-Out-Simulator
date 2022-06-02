import sys

points_dict = {
	"T20":60, "T19":57, "T18":54, "T17":51, "T16":48, "T15":45, "T14":42, "T13":39, "T12":36, "T11":33, "T10":30, "T9":27, "T8":24, "T7":21, "T6":18, "T5":15, "T4":12, "T3":9, "T2":6, "T1":3,
	"D20":40, "D19":38, "D18":36, "D17":34, "D16":32, "D15":30, "D14":28, "D13":26, "D12":24, "D11":22, "D10":20, "D9":18, "D8":16, "D7":14, "D6":12, "D5":10, "D4":8, "D3":6, "D2":4, "D1":2,
	"S20":20, "S19":19, "S18":18, "S17":17, "S16":16, "S15":15, "S14":14, "S13":13, "S12":12, "S11":11, "S10":10, "S9":9, "S8":8, "S7":7, "S6":6, "S5":5, "S4":4, "S3":3, "S2":2, "S1":1
}

throws = {}
counts = {}


def add_throw(p, darts):
	if p in throws.keys():
		throws[p] = throws[p] +", "+ darts
		counts[p] = counts[p] + 1
	else:
		throws[p] = darts
		counts[p] = 1

def howdy():
	print("Hello World\n")
	x = dict(points_dict)	
	y = dict(points_dict)	
	z = dict(points_dict)	

	for t1 in x:
		p = points_dict[t1]
		if t1.startswith("D"):
			add_throw(p, t1)
		for t2 in y:
			p = points_dict[t1] + points_dict[t2]
			if t2.startswith("D"):
				add_throw(p, t1 +" "+ t2)
			for t3 in z:
				p = points_dict[t1] + points_dict[t2] + points_dict[t3]
				if t3.startswith("D"):
					add_throw(p, t1 +" "+ t2 +" "+ t3)

	orig_stdout = sys.stdout
	with open('outs.txt', 'w') as f:
		sys.stdout = f

		for k in throws:
			print("%s, %d, %s" % (k, counts[k], throws[k]))

	sys.sdtdout = orig_stdout




if __name__ == '__main__':
	howdy()
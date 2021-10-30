import xml.dom.minidom
import collections
import graphviz
import argparse

# NOTE TO SERGI: OUR SOLUTION DID ALWAYS WROTE THE REPORT IN THIS DIRECTORY SO HERE TC1 OUTPUT IS ACTUALLY TC2 OUTPUT :D
SOLUTIONPATH = "testcases/Small/TC1/Output/"
FILEPATH = "testcases/Small/TC2/Input/"

BASE = ""


class Architecture:
    ## This dictionary contains objects.
    graph = collections.defaultdict(list)
    edges = {}
    
    def __init__(self, edges):

        for e in edges:
            self.graph[e.src].append(e.dest)
            #self.graph[e.dest].append(e.src)
            

    def __str__(self):
        return str(self.graph)


class Edge:
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.srcQueue = {
			'q0': [],
			'q1': [],
			'q2': []
		}
		self.destQueue = {
			'q0': [],
			'q1': [],
			'q2': []
		}

class Link:
	def __init__(self, Source, Destination, QNumber):
		super(Link, self).__init__()
		self.src = Source
		self.dest = Destination
		self.q_number = QNumber



	def __str__(self):
		return f"SOURCE: {self.src} DESTINATION: {self.dest} QNUMBER: {self.q_number} "



class Message:
	def __init__(self, links, name, maxE2E):
		super(Message, self).__init__()

		self.links = links
		self.name = name
		self.maxE2E = maxE2E

		path = []
		qnums = []

		for l in links:
			path.append(l.src)
			qnums.append(int(l.q_number))
		path.append(links[len(links)-1].dest)

		self.path = path
		self.qnums = qnums


	def __str__(self):

		linkstr=""
		for l in self.links:
			linkstr += str(l)

		return f"LINKS: {linkstr} Name: {self.name} maxE2E: {self.maxE2E}"

def extract_link(l):
	return Link(l.getAttribute("Source"), l.getAttribute("Destination"), 
		l.getAttribute("Qnumber"))

def extract_message_data(m):
	

	links = [extract_link(l) for l in m.getElementsByTagName("Link")]
	name = m.getAttribute("Name")
	maxE2E = m.getAttribute("maxE2E")


	return Message(links, name, maxE2E)

def extract_edge_data(edge):

 
    source = edge.getAttribute("Source")
    destination = edge.getAttribute("Destination")

    return Edge(source, destination)

def extract_report_data(conf):



	messages = [extract_message_data(m) for m in conf.getElementsByTagName("Message")]
	

	return messages


def extract_config_data(conf):

	edges = [extract_edge_data(e) for e in conf.getElementsByTagName("Edge")]


	return edges


def qString(q, m):

	if q == '0':
		print('1s')
		return f"{{ q0 {m.name} | q1 | q2 }}"
	elif q == '1':
		print('2s')
		return f"{{ q0 | q1 {m.name} | q2}}"
	elif q =='2':
		print('3s')
		return f"{{ q0 | q1 | q2 {m.name}}}"

def illustrate_message(dot, graph, message):

	print(graph)

	dot.engine = 'dot'

	linkq = {}
	for link in message.links:
		linkq[link.src+link.dest] = link.q_number
		linkq[link.dest+link.src] = link.q_number

	
	for key, value in graph.items():
		if key in message.path: 
			dot.node(key, color = 'blue')
		else:
			dot.node(key)
		for v in value:

			if v in message.path:
				dot.node(v, color = 'blue')
				if 'SW' in v and 'SW' in key:
					if key in message.path:
						dot.node(v+key, shape='record', label=qString(linkq[key+v],message), color = 'blue')
					else:
						dot.node(v+key, shape='record', label="{ q1 | q2 | q3 }")
					dot.node(v+key+'1', shape='record', label="{ q1 | q2 | q3 }")
					dot.edge(key, v+key, arrowhead = 'none')
					dot.edge(v+key, v+key+'1', arrowhead = 'none')
					dot.edge(v+key+'1', v, arrowhead = 'none')
				else:
					if key in message.path:
						dot.node(v+key, shape='record', label=qString(linkq[key+v],message), color = 'blue')
					else:
						dot.node(v+key, shape='record', label="{ q1 | q2 | q3 }")
					dot.edge(key, v+key, arrowhead = 'none')
					dot.edge(v+key, v, arrowhead = 'none')
			else:
				dot.node(v+key, shape='record', label="{ q1 | q2 | q3 }")
				dot.node(v+key+'1', shape='record', label="{ q1 | q2 | q3 }")
				dot.edge(key, v+key, arrowhead = 'none')
				dot.edge(v+key, v+key+'1', arrowhead = 'none')
				dot.edge(v+key+'1', v, arrowhead = 'none')



			
				


			

				
			
			
			
			


	dot.render('test-output/topology.gv', view=True)
  
	


def main(message_name):

	if not message_name:
		print('ADD MESSAGE NAME AS AN ARGUMENT')
		return

	num = message_name[1:]
	
	
	

	doc_config = xml.dom.minidom.parse(FILEPATH + "Config.xml")
	doc_report = xml.dom.minidom.parse(SOLUTIONPATH + "Report.xml")



	config_doc = doc_config.getElementsByTagName("Architecture")[0]
	report_doc = doc_report.getElementsByTagName("Report")[0]

	

	edges = extract_config_data(config_doc)
	messages = extract_report_data(report_doc)



	
	

	arch = Architecture(edges)

	dot = graphviz.Graph(comment='Network Topology')

	
	message = messages[int(num)-1]

	print(message.qnums)
	print(message.path)

	illustrate_message(dot, arch.graph, message)








if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('message', metavar='message', type=str, nargs='?',
						help='message name')
	args = parser.parse_args()
	main(args.message)

import xml.dom.minidom
import collections


SOLUTIONPATH = "Report.xml"

BASE = ""

class Vertex:
	def __init__(self, name):
			self.name = name
			self.edges = {}

	def __repr__(self) -> str:
			return f"({self.name}): {self.connections}"

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

def extract_data(conf):

	return [extract_message_data(m) for m in conf.getElementsByTagName("Message")]

def process_messages(messages):
	#vertices = collections.defaultdict(Vertex)
	vertices = {}
	vertex_links = []
	edges = {}
	for message in messages:
		# Source add to message
		for link in message.links:

			if not link.src in vertices:
				vertices[link.src] = Vertex(link.src)
			#vertices[link.src].connections.append((message.name, link.q_number))
			
			edge = (link.src, link.dest)
			if not edge in edges:
				edges[edge] = Edge(link.src, link.dest)
			#edges[edge]
            
            # TODO, store the edges and the information of the messages in the respective queues
            
			
			#vertex_connection = (link.src, link.dest)
			#if not vertex_connection in vertex_links:
			#	vertex_links.append(vertex_connection)


	print("Vertices", vertices)



def getSwitchesString(messages):

	print()

def getConnectionsString(messages):

	print()


def create_output(messages):
	pass
'''
	output = f'graph G {
    style=filled;
    color=lightgrey;
    rankdir = "LR"
    
    node [
        style=filled,
        shape=record,
        fontsize = "16",
    ];
    edge [
    ];
    
    // Switches
   	{getSwitchesString(messages)}
    
    // Connections
    {getConnectionsString(messages)}

    }'
'''

def main():

	doc_app = xml.dom.minidom.parse(SOLUTIONPATH)
	elem_doc = doc_app.getElementsByTagName("Report")[0] 

	messages = extract_data(elem_doc)
	process_messages(messages)






if __name__ == "__main__":

    main()

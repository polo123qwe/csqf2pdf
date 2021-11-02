import xml.dom.minidom
import collections
import argparse
import graphviz

BASE = ""
EMTPY_QUEUE_STR = "{ Q1 | Q2 | Q3 } | { || }"


class Architecture:
    # This dictionary contains objects.
    graph = collections.defaultdict(list)
    edges = {}

    def __init__(self, edges):

        for e in edges:
            self.graph[e.src].append(e.dest)
            # self.graph[e.dest].append(e.src)

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

    def __repr__(self):
        return f"{self.src} => {self.dest} (Q{self.q_number})"


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

        return f"({self.name}) E2E:{self.maxE2E} LINKS: {self.links}"


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
    messages = {}
    for m in conf.getElementsByTagName("Message"):
        message = extract_message_data(m)
        messages[message.name] = message

    return messages


def extract_config_data(conf):

    edges = [extract_edge_data(e) for e in conf.getElementsByTagName("Edge")]

    return edges


def qString(q, m):
    # print(q)

    if q == '0':
        return f"{{ Q1 | Q2 | Q3 }} | {{ {m.name}|| }}"
    elif q == '1':
        return f"{{ Q1 | Q2 | Q3 }} | {{ |{m.name}| }}"
    elif q == '2':
        return f"{{ Q1 | Q2 | Q3 }} | {{ ||{m.name} }}"


def create_topology_with_message(dot, graph, message, output_path):

    dot.engine = 'dot'

    linkq = {}
    for link in message.links:
        linkq[link.src+link.dest] = link.q_number
        linkq[link.dest+link.src] = link.q_number

    #print("Items to iterate", graph)
    #print("Message path", message)
    #print("Edges", linkq)

    for key, value in graph.items():
        if key in message.path:
            dot.node(key, color='blue', style='bold')
        else:
            dot.node(key)
        for v in value:

            if v in message.path:
                dot.node(v, color='blue', style='bold')
                if 'SW' in v and 'SW' in key:
                    if key in message.path:
                        dot.node(v+key, shape='record',
                                 label=qString(linkq[key+v], message), color='blue', style='bold')

                        dot.edge(key, v+key, arrowhead='none',
                                 color='blue', style='bold')
                        dot.edge(v+key, v+key+'1', arrowhead='none',
                                 color='blue', style='bold')
                        dot.edge(v+key+'1', v, arrowhead='none',
                                 color='blue', style='bold')
                    else:
                        dot.node(v+key, shape='record', label=EMTPY_QUEUE_STR)
                        dot.edge(key, v+key, arrowhead='none')
                        dot.edge(v+key, v+key+'1', arrowhead='none')
                        dot.edge(v+key+'1', v, arrowhead='none')
                    dot.node(v+key+'1', shape='record', label=EMTPY_QUEUE_STR)

                else:
                    if key in message.path:
                        dot.node(v+key, shape='record',
                                 label=qString(linkq[key+v], message), color='blue', style='bold')

                        dot.edge(key, v+key, arrowhead='none',
                                 color='blue', style='bold')
                        dot.edge(v+key, v, arrowhead='none',
                                 color='blue', style='bold')
                    else:
                        dot.node(v+key, shape='record', label=EMTPY_QUEUE_STR)

                        dot.edge(key, v+key, arrowhead='none')
                        dot.edge(v+key, v, arrowhead='none')
            else:
                dot.node(v+key, shape='record', label=EMTPY_QUEUE_STR)
                dot.node(v+key+'1', shape='record', label=EMTPY_QUEUE_STR)

                dot.edge(key, v+key, arrowhead='none')
                dot.edge(v+key, v+key+'1', arrowhead='none')
                dot.edge(v+key+'1', v, arrowhead='none')

    try:
        dot.render(f'{output_path}/output.gv', view=True)
    except:
        with open(f'{output_path}/output.gv', 'w') as file:
            file.write(str(dot))

def create_topology(dot, graph, output_path):

    dot.engine = 'dot'

    print("Items to iterate", graph)

    for key, value in graph.items():
        dot.node(key)
        for v in value:
            if 'SW' in v and 'SW' in key:
                dot.node(v+key, shape='record', label=EMTPY_QUEUE_STR)
                dot.edge(key, v+key, arrowhead='none')
                dot.edge(v+key, v+key+'1', arrowhead='none')
                dot.edge(v+key+'1', v, arrowhead='none')
                dot.node(v+key+'1', shape='record', label=EMTPY_QUEUE_STR)
            else:
                dot.node(v+key, shape='record', label=EMTPY_QUEUE_STR)
                dot.node(v+key+'1', shape='record', label=EMTPY_QUEUE_STR)

                dot.edge(key, v+key, arrowhead='none')
                dot.edge(v+key, v+key+'1', arrowhead='none')
                dot.edge(v+key+'1', v, arrowhead='none')

    try:
        dot.render(f'{output_path}/output.gv', view=True)
    except:
        with open(f'{output_path}/output.gv', 'w') as file:
            file.write(str(dot))

def main(message_name, topology_path, report_path, output_path):
    if not message_name:
        print('Creating empty topology')
        empty_topology(topology_path, output_path)
    else:
        topology_with_message(message_name, topology_path, report_path, output_path)

def empty_topology(topology_path, output_path):

    doc_config = xml.dom.minidom.parse(topology_path)

    config_doc = doc_config.getElementsByTagName("Architecture")[0]

    edges = extract_config_data(config_doc)
    
    arch = Architecture(edges)

    dot = graphviz.Digraph(comment='Network Topology')
    
    create_topology(dot, arch.graph, output_path)

def topology_with_message(message_name, topology_path, report_path, output_path):
    doc_config = xml.dom.minidom.parse(topology_path)
    doc_report = xml.dom.minidom.parse(report_path)

    config_doc = doc_config.getElementsByTagName("Architecture")[0]
    report_doc = doc_report.getElementsByTagName("Report")[0]

    edges = extract_config_data(config_doc)
    messages = extract_report_data(report_doc)

    arch = Architecture(edges)

    dot = graphviz.Digraph(comment='Network Topology')

    if (message_name not in messages):
        print('Invalid message!')
        return

    message = messages[message_name]

    create_topology_with_message(dot, arch.graph, message, output_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--message', metavar='message', type=str, nargs='?',
                        default='', help='Message name (eg. F1)')
    parser.add_argument('-t', '--topology', metavar='topology', type=str, nargs='?',
                        default='Config.xml', help='Topology file location')
    parser.add_argument('-r', '--report', metavar='report', type=str, nargs='?',
                        default='Report.xml', help='Report file location')
    parser.add_argument('-o', '--output', metavar='output', type=str, nargs='?',
                        default='.', help='Output directory')

    args = parser.parse_args()
    main(args.message, args.topology, args.report, args.output)

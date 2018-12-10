import pandas,numpy
import os,sys
import networkx as nx
import scipy.stats

#from brainnetworks.utils import mk_random_graph

# read the data from Wormatlas.org: see section 2.1 of http://www.wormatlas.org/neuronalwiring.html for details

celegans_connectome=pandas.read_excel('NeuronConnect.xls')

# set up the graph
G = nx.DiGraph()
for i in celegans_connectome.index:
		G.add_edge(celegans_connectome.loc[i]['Neuron 1'],celegans_connectome.loc[i]['Neuron 2'])

# the graph has two connected components, so we will just keep the giant component
G = nx.DiGraph(G)  # Un-freeze the graph
G.remove_node('NMJ')  # Remove neuromuscular junction "node"
components=sorted(nx.weakly_connected_components(G), key=len, reverse=True)
G = nx.DiGraph(G.subgraph(components[0]))


with open('cycles.txt','a') as f:
	f.write('cycles = [\n')
	i = 0
	for c in nx.simple_cycles(G):
		line = '{},'.format(repr(c).replace(' ',''))
		f.write(line)
		i += 1
		if i % 1e5 == 0:
			print('Found {} cycles'.format(i))
	f.write(']\n\n\n')

print('Finished, found {} cycles'.format(i))
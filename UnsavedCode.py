

# Community Subgraphs
I now counted cycles within each cluster subgraph.  This was particularly fascinating, as the huge clusters had the smallest numbers of cycles, and some middle-sized graphs had the largest number of cycles.  Finally, the nearly-fully-connected smallest cluster had an astounding 6140 cycles amongst just 10 nodes.

### Cycle Count Normalization
To normalize cycle counts against possible counts, I needed to compute the total number of cycles possible in each group.  I considered many formulas on [this StackExchange question](https://math.stackexchange.com/questions/1363963/number-of-cycles-in-complete-graph), but they were all for undirected graphs and several undercounted possible cycles in a directed graph.  I took inspiration from the method described by B2C's equation, which assumes the graphis complete and then counts every subset of 2 or more nodes.  However, this equation only accounts for undirected cycles, which is presumably why cluster 8 has far more cycles than what this equation yields.  I could not find a formula for the total number of cycles in a directed graph.

$C_{total} = \sum_{i=2}^k \binom{k}{i} $ where $k=$ the number of nodes.

This revealed an interesting observation, which is that iterations in the middle of the range yielded many more cycles of medium length than cycles of small and large length (the binomial function returns its largest values when $i$ is near the middle of its range, and tails out such that $\binom{k}{0}=1$ and $\binom{k}{k}=1$).  This might explain the shape of cycle length histograms in each subgraph.



from math import factorial
def max_cycles(k):
    sumval = 0
    for i in range(2,k+1):
        sumval += factorial(k) // (factorial(k-i) * factorial(i))
    return sumval

cycle_utilization = []
for sub in range(len(cycle_counts)):
    cycle_utilization.append( float(cycle_counts[sub]) / max_cycles(len(cluster_subgraphs[sub])) )
print(cycle_utilization)







def plot_adjmtx(G, bin=False, node_order=None, lines=None):
    # Build dataframe
    A = nx.to_numpy_array(G, nodelist=node_order, weight='weight')
    maxval = np.amax(A)
    Am = np.ma.masked_where(A == 0, A)
    A = pd.DataFrame(A,columns=list(G.nodes),index=list(G.nodes))
    # Start plotting
    plt.figure(figsize=(16,16))
    plt.imshow(Am)
    palette = copy(plt.cm.viridis)
    palette.set_under('b', 1.0)
    plt.pcolor(Am, norm=matplotlib.colors.LogNorm(vmin=0.9, vmax=maxval), cmap=palette)
    plt.colorbar()
    # set the axes to use name labels rather than numbers
    ax=plt.gca()
    node_list=list(G.nodes) 
    ax.set_yticks(np.arange(len(node_list)))
    ax.set_xticks(np.arange(len(node_list)))
    ax.set_xticklabels(node_list)
    ax.set_yticklabels(node_list)
    # Plot cluster lines
    if lines is None:
        return
    graph_size = A.shape[0]-1
    for line in lines:
        plt.plot([0,graph_size],[line,line],color='w',linewidth=0.5)
        plt.plot([line,line],[0,graph_size],color='w',linewidth=0.5)










# Utility Functions

def get_weight_histogram(graph):
    ''' Build a histogram of weights from a weighted graph '''
    return dict(Counter([graph[e[0]][e[1]]['weight'] for e in list(graph.edges)]))

def get_cycle_length_histogram(cycles):
    return dict(Counter([c['ct'] for c in cycles]))

def get_node_cluster_map(cluster_nodes):
    ''' Invert a cluster_node set to map node names to cluster index '''
    node_cluster_map = {}
    for cluster in range(len(cluster_nodes)):
        for node in cluster_nodes[cluster]:
            node_cluster_map[node] = cluster
    return node_cluster_map

def count_cycles(graph, cutoff=1e7):
    i = 0
    for c in nx.simple_cycles(graph):
        i += 1
        if i > cutoff:
            return '> {}'.format(cutoff)
    return str(i)

# Courtesy Russ Poldrack
def plot_adjmtx(G,bin=False):
    A = nx.to_numpy_array(G,weight='weight')
    if bin:
        A = (A>0).astype('int')
        cmap='gray'
    else:
        cmap='viridis'
    A = pd.DataFrame(A,columns=list(G.nodes),index=list(G.nodes))
    
    plt.imshow(A,cmap=cmap)
    if not bin:
        plt.colorbar()
    # set the axes to use name labels rather than numbers
    ax=plt.gca()
    node_list=list(G.nodes) 
    ax.set_yticks(np.arange(len(node_list)))
    ax.set_xticks(np.arange(len(node_list)))
    ax.set_xticklabels(node_list)
    ax.set_yticklabels(node_list)
    # add grid lines
#     for i in range(len(node_list)):
#         ax.axvline(x=i-0.5,color='b')
#         ax.axhline(y=i-0.5,color='b')









def analyze_subgraph(g):
    cycles = []
    for c in nx.simple_cycles(g):
        x = {
            'nodes':c,
            'ct':len(c),
        }
        cycles.append(x)
        print(x)
    len_hist = get_cycle_length_histogram(cycles)
    width = 1.0     
    plt.bar(len_hist.keys(), len_hist.values(), width, color='g')
    plt.xlabel('Count of collapsed connections (directionally independent)')
    plt.ylabel('Number of edges in cluster graph')
    plt.show()

analyze_subgraph(comgs[3])



















































'''
Custom extensions the mapper package
'''
import seaborn
import math

def custom_d3js_fdgraph(mapper_output, df_data, feature=None):
    '''
    Build a graph data structure to be injected into a D3 force-directed graph viz.
    This function operates on the mapper.mapper_output class. Vertices in the graph
    are optionally assigned a color, depending on the mean value of a specified
    feature (or binary label) in the original data (provided in a pandas dataframe).
    '''

    # initialize the graph data
    G = {}

    # assign vertices:
    # index - enumerating the nodes from the mapper_output, starting with 0.
    # members - list out the specific data points belonging to a node
    # attribute - if feature provided, take the mean value of that feature for the
    #   points belonging to the node; else, take the default value computed by mapper.
    G['vertices'] = [{'index': i,
                      'members': list(n.points),
                      'attribute': n.attribute if feature is None else df_data.ix[df_data.index[n.points],feature].mean()
                     } for (i,n) in enumerate(mapper_output.nodes)
                    ]

    # assign edges:
    # source/target - are node indices on either side of an edge.
    # weight - use value from mapper, which uses the number of points shared between
    #   the nodes of an edge.
    G['edges']    = [{'source': e[0],
                      'target': e[1],
                      'weight': mapper_output.simplices[1][e]
                     } for e in mapper_output.simplices[1].keys()
                    ]

    # attach a sequential color palete scaled on vertice attribute values
    ncolors   = 50
    color_map = seaborn.color_palette('Spectral',50)
    min_attr  = None
    max_attr  = None
    for v in G['vertices']:
        min_attr = v['attribute'] if min_attr is None else min(v['attribute'],min_attr)
        max_attr = v['attribute'] if max_attr is None else max(v['attribute'],max_attr)
    for v in G['vertices']:
        color_idx = math.floor((ncolors - 1) * (v['attribute'] - min_attr) / (max_attr - min_attr))
        v['color'] = "#{0:02x}{1:02x}{2:02x}".format(*[math.floor(c*255) for c in color_map[color_idx]])

    return G

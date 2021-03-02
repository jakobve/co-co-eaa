# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import igraph as ig
import leidenalg as la
import re

from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.objects.log.util import sorting
from pm4py.util import xes_constants as xes
from pm4py.objects.log.importer.xes import importer as xes_importer
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import fowlkes_mallows_score as fms
from sklearn.metrics.cluster import normalized_mutual_info_score as nmi
from pm4py.objects.log.exporter.xes import exporter as xes_exporter


# Event log methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Imports event log in XES data format
def import_log_xes(path):
    """
    Imports an event log in the xes data format from the file directory and parses it.

    :param path: String representing path in the file directory
    :return: Event log object
    """
    log = xes_importer.apply(path)
    log = sorting.sort_timestamp(log)
    return log


# Exports the event log to a given directory in IEEE XES format
def export_log_xes(log, path):
    """
    Exports the event log to a given directory in IEEE XES format.

    :param log: Event log object
    :param path: string - path to directory
    """
    xes_exporter.apply(log, path)


# Returns a list of event attributes from the event log
# Was used during the project for determining, which attribute should be used for ground truth partitioning
def get_event_attributes_from_log(log):
    """
    Returns a list of all event attributes contained in the event log.

    :param log: Event log object
    :return: List of all different attributes in the event log
    """
    all_attributes = set()
    for trace in log:
        for event in trace:
            all_attributes = all_attributes.union(set(event.keys()))
    if xes.DEFAULT_TRANSITION_KEY in all_attributes:
        all_attributes.remove(xes.DEFAULT_TRANSITION_KEY)
    return all_attributes


# Returns all attribute values from an event log of a specified attribute
# Was used during the project for determining, which attribute should be used for ground truth partitioning
def get_attribute_values_from_log(log, attribute_name):
    """
    Returns all attribute values from an event log of a specified attribute.

    :param log: Event log object
    :param attribute_name: String - attribute name
    :return: List of values of the respective attribute in the given event log
    """
    attributes = attributes_filter.get_attribute_values(log, attribute_name)
    return attributes


# Identifies the ground truth for each event log and inserts it as event attribute to the respective event log
def identify_ground_truth(log, log_name):
    """
    Identifies the ground truth for each event log and inserts it as event attribute to the respective event log.

    :param log: Event log object
    :param log_name: string - Name of the event log
    :return: Event log object containing the ground truth
    """
    if "BPI2015" in log_name:
        for trace in log:
            for event in trace:
                if "AH_I" in str(event['concept:name']):
                    event['truth'] = 0
                    continue
                elif "AH_II" in str(event['concept:name']):
                    event['truth'] = 1
                    continue
                elif "AP" in str(event['concept:name']):
                    event['truth'] = 2
                    continue
                elif 'AWB' in str(event['concept:name']):
                    event['truth'] = 3
                    continue
                elif 'BB' in str(event['concept:name']):
                    event['truth'] = 4
                    continue
                elif 'BPT' in str(event['concept:name']):
                    event['truth'] = 5
                    continue
                elif 'CRD' in str(event['concept:name']):
                    event['truth'] = 6
                    continue
                elif 'DRZ' in str(event['concept:name']):
                    event['truth'] = 7
                    continue
                elif 'EIND' in str(event['concept:name']):
                    event['truth'] = 8
                    continue
                elif 'GBH' in str(event['concept:name']):
                    event['truth'] = 9
                    continue
                elif 'HOOFD' in str(event['concept:name']):
                    event['truth'] = 10
                    continue
                elif 'LGSD' in str(event['concept:name']):
                    event['truth'] = 11
                    continue
                elif 'LGSV' in str(event['concept:name']):
                    event['truth'] = 12
                    continue
                elif 'NGV' in str(event['concept:name']):
                    event['truth'] = 13
                    continue
                elif 'NOCODE' in str(event['concept:name']):
                    event['truth'] = 14
                    continue
                elif 'OLO' in str(event['concept:name']):
                    event['truth'] = 15
                    continue
                elif 'OPS' in str(event['concept:name']):
                    event['truth'] = 16
                    continue
                elif 'UOV' in str(event['concept:name']):
                    event['truth'] = 17
                    continue
                elif 'VD' in str(event['concept:name']):
                    event['truth'] = 18
                    continue
                elif 'VRIJ' in str(event['concept:name']):
                    event['truth'] = 19
                    continue
                else:
                    print(event['concept:name'])
        return log

    elif "BPI2017" in log_name:
        for trace in log:
            for event in trace:
                if event['EventOrigin'] == 'Application':
                    event['truth'] = 0
                elif event['EventOrigin'] == 'Offer':
                    event['truth'] = 1
                elif event['EventOrigin'] == 'Workflow':
                    event['truth'] = 2
                else:
                    print(event['concept:name'])
        return log

    elif "BPI2018" in log_name:
        for trace in log:
            for event in trace:
                if event['subprocess'] == 'Application':
                    event['truth'] = 0
                elif event['subprocess'] == 'Change':
                    event['truth'] = 1
                elif event['subprocess'] == 'Declared':
                    event['truth'] = 2
                elif event['subprocess'] == 'Main':
                    event['truth'] = 3
                elif event['subprocess'] == 'Objection':
                    event['truth'] = 4
                elif event['subprocess'] == 'On-Site':
                    event['truth'] = 5
                elif event['subprocess'] == 'Remote':
                    event['truth'] = 6
                elif event['subprocess'] == 'Reported':
                    event['truth'] = 7
                else:
                    print(event['subprocess'])
        return log

    elif "BPI2020" in log_name:
        for trace in log:
            for event in trace:
                if event['org:role'] == 'ADMINISTRATION':
                    event['truth'] = 0
                elif event['org:role'] == 'BUDGET OWNER':
                    event['truth'] = 1
                elif event['org:role'] == 'EMPLOYEE':
                    event['truth'] = 2
                elif event['org:role'] == 'PRE_APPROVER':
                    event['truth'] = 3
                elif event['org:role'] == 'MISSING':
                    event['truth'] = 4
                elif event['org:role'] == 'SUPERVISOR':
                    event['truth'] = 5
                elif event['org:role'] == 'UNDEFINED':
                    event['truth'] = 6
                elif event['org:role'] == 'DIRECTOR':
                    event['truth'] = 7
                else:
                    print(event['org:role'])
        return log

    else:
        print("Event log not found")


# Inserts the identified communities into the event log as event attribute ['community']
def insert_communities_to_log(log, partition, graph):
    """
    Inserts the identified communities into the event log as event attribute ['community'].

    :param log: event log object
    :param partition: partition object
    :param graph: iGraph object
    :return: event log object
    """
    it = 0
    communities = dict()

    for part in partition:
        for vertex in part:
            communities[graph.vs[vertex]['name']] = it
        it += 1
    for trace in log:
        for event in trace:
            if event['concept:name'] in communities.keys():
                event['community'] = communities[event['concept:name']]
    return log


# Directly Follows Graph Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Discover directly follows graph from event log
def create_directly_follows_graph(log):
    """
    Creates a directly follows graph from an imported event log.

    :param log: Event log object
    :return: dict - Directly Follows Graph. Edges are the keys. Values are the edge weights.
    """
    dfg = dfg_discovery.apply(log)
    dfg = dict(dfg)
    return dfg


# Possibility for linear filtering the directly follows graph
def filter_log_by_weight(directly_follows_graph, edge_weight):
    """
    Filters put the edges of the dfg, which have a lower edge weight than the specified weight.

    :param directly_follows_graph: dict - Directly Follows Graph
    :param edge_weight: int - Threshold value
    :return: dict - Directly Follows Graph with edges where the weights are bigger
    than the specified value
    """
    edges_filtered = dict()
    for (key, value) in directly_follows_graph.items():
        if value > edge_weight:
            edges_filtered[key] = value
    return edges_filtered


# Filter the BPI challenges 2015s event log for the main process HOOFD
def filter_main_process_bpi15(directly_follows_graph):
    """
    Filters the directly follows graph of the BPI challenge 2015 logs_with_truth for the edges belonging to the main
    process HOOFD.

    :param directly_follows_graph: dict - Directly Follows Graph
    :return: dict - Edges with respective weights that belong to the main process of the BPI
    """
    edges_filtered = dict()
    for (key, value) in directly_follows_graph.items():
        if re.search(r"^\(\'01_HOOFD_.+\,\s\'01_HOOFD_.+\'\)$", str(key)):
            edges_filtered[key] = value
    return edges_filtered


# Due to the format of the directly follows graph you have to source the vertices from the edges of the directly
# follows graph
def get_vertices(edges):
    """
    Returns the vertices contained in the directly follows graph
    indicated in the edges.

    :param edges: list - Edges of the directly follows graph
    :return: list - Vertices of the directly follows graph
    """
    vertices = list()
    for edge in edges:
        # Transform edge to string
        txt = str(edge)
        # Split edge into two parts and store both in an array
        txt = txt.split(',')
        for part in txt:
            # If it is the first part of an edge
            if '(' in part:
                # Remove the first two characters
                part = part[2:]
                # Remove the last character
                part = part[:-1]
            elif ')' in part:
                # Remove the first two characters
                part = part[2:]
                # Remove the last two characters
                part = part[:-2]
            # Store cleaned vertices in an array
            vertices.append(part)
    # Remove duplicates from the list
    vertices = remove_duplicates(vertices)
    vertices.sort()
    return vertices


# Graph Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Creates a directed, weighted graph from a list of vertices, edges and weights and
# Returns an iGraph object
def create_igraph(dfg):
    """
    Creates a directed, weighted graph from a list of vertices, edges and weights.

    :param dfg: Directly Follows Graph Object
    :return: iGraph object - Directed, weighted graph in form of an iGraph object
    """
    mylist = list()
    for item in dfg.keys():
        t = (item[0], item[1], dfg[item])
        mylist.append(t)

    graph = ig.Graph.TupleList(mylist, weights=True)

    return graph


# Returns a list of the indexes of the indexes of each given vertex in the given graph
def index_vertices(vertexlist, graph):
    """
    Returns the indexes of the given vertices from the given graph.

    :param vertexlist: list -List of vertices
    :param graph: iGraph object
    :return: list - List of indexes of vertices
    """
    return_list = list()
    for vertex in vertexlist:
        return_list.append(graph.vs.find(name=vertex).index)
    return return_list


# Returns the predecessors of a given vertex in a given graph
def get_predecessors(vertex, graph):
    """
    Returns the predecessors of a given vertex in a given graph.

    :param vertex: int - Vertex in the graph
    :param graph: iGraph object
    :return: list - List of all predecessors of the given node
    """
    predecessors = list()
    predecessors.extend(graph.predecessors(vertex))
    return predecessors


# Returns successors of the given vertex in the given graph
def get_successors(vertex, graph):
    """
    Returns successors of the given vertex in the given graph.

    :param vertex: int - Vertex in the graph
    :param graph: iGraph object
    :return: list - List of all successors of the given node
    """
    successors = list()
    successors.extend(graph.successors(vertex))
    return successors


# Returns predecessors of the given vertex in the given graph without duplicates
def get_unique_predecessors(vertex, graph):
    """
    Returns predecessors of the given vertex in the given graph without duplicates.

    :param vertex: int - Vertex in the graph
    :param graph: iGraph object
    :return: list - Duplicate free list of the predecessors of the given node
    """
    pre_nodes_in_stage_i = get_predecessors(vertex, graph)
    return remove_duplicates(pre_nodes_in_stage_i)


# Returns successors of the given vertex in the given graph without duplicates
def get_unique_successors(vertex, graph):
    """
    Returns successors of the given vertex in the given graph without duplicates.

    :param vertex: int - Vertex in the graph
    :param graph: iGraph object
    :return: list - Duplicate free list of the successors of the given node
    """
    suc_nudes_in_stage_i = get_successors(vertex, graph)
    return remove_duplicates(suc_nudes_in_stage_i)


# Get predecessors and successors of the given vertex
def get_predecessors_successors(vertex, graph):
    """
    Calculates all predecessors and successors of a given vertex in a given graph.

    :param vertex: int - Vertex in the graph
    :param graph: iGraph object
    :return: list - List of predecessors and successors
    """
    overlaps = list()
    pre = get_unique_predecessors(vertex, graph)
    suc = get_unique_successors(vertex, graph)
    overlaps.extend(pre)
    overlaps.extend(suc)
    return overlaps


# Returns the predecessors and successors of a single vertex without duplicates
def get_unique_predecessors_successors(vertex, graph):
    """
    Calculates the predecessors and successors of a given vertex in a given graph.

    :param vertex: int - Vertex in the graph
    :param graph: iGraph object
    :return: list - List of predecessors and successors without duplicate values
    """
    overlaps = get_predecessors_successors(vertex, graph)
    ov_unique = remove_duplicates(overlaps)
    return ov_unique


# Returns number of predecessors without duplicates of a list of vertices
def get_number_of_unique_predecessors(partition, graph):
    """
    Returns number of predecessors without duplicates of a list of vertices.

    :param partition: list - List of vertices
    :param graph: iGraph object
    :return: list - List of predecessors without duplicates
    """
    pre_unique = get_unique_predecessors(partition, graph)
    return len(pre_unique)


# Returns number of successors without duplicates of a list of vertices
def get_number_of_unique_successors(partition, graph):
    """
    Returns number of successors without duplicates of a list of vertices.

    :param partition: list - List of vertices
    :param graph: iGraph object
    :return: list - List of successors without duplicates
    """
    suc_unique = get_unique_successors(partition, graph)
    return len(suc_unique)


# Returns the ground truth which was previously stored in the event log in form of a list
def get_ground_truth(vertices, graph, log):
    """
    Returns the ground truth which was previously stored in the event log in form of a list.

    :param vertices: list - List of vertices
    :param graph: iGraph object
    :param log: event log object - Event log
    :return: list - List with membership of each given vertex in its respective ground truth cluster.
    """
    vertices = index_vertices(vertices, graph)
    vertices.sort()
    cluster = 0
    ground_truth = list()
    for vertex in vertices:
        v_name = graph.vs[vertex]['name']
        for trace in log:
            for event in trace:
                if v_name == event['concept:name']:
                    cluster = event['truth']
        ground_truth.append(cluster)
    return ground_truth


# Run the Leiden algorithm
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Creates a partition of the directed, weighted graph (iGraph Object)
# The method uses the Leiden algorithm in form of the
def run_leiden(graph):
    """
    Creates a partition of the graph with help of the leiden algorithm.

    :param graph: iGraph object - Directed, weighted iGraph object
    :return: Partition object - High modular partition having a high cohesion and loose coupling
    """
    partition = la.find_partition(graph, la.ModularityVertexPartition, seed=0, weights='weight')
    return partition


# Supporting methods for calculating the cohesion-coupling process ratio, Fowlkes-mallows index,
# adjusted rand index, normalized mutual information, graph density
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Duplicate Methods
# ----------------------------------------------------------------------------------------------------------------------

# Removes all duplicates from a given list
def remove_duplicates(input_list):
    """
    Removes all duplicate values from a given list.

    :param input_list: list - List of values to remove duplicates from
    :return: list - List without duplicates
    """
    return list(dict.fromkeys(input_list))


# Returns all duplicates from a given list
def get_duplicates(input_list):
    """
    Returns all duplicates from a given list.

    :param input_list: list - List of values containing duplicates
    :return: list - List with duplicates from the given list
    """
    size = len(input_list)
    duplicates = list()
    for i in range(size):
        k = i + 1
        for j in range(k, size):
            if input_list[i] == input_list[j] and input_list[i] not in duplicates:
                duplicates.append(input_list[i])
    return duplicates


# Returns the number of duplicates contained in a list
def get_number_of_duplicates(input_list):
    """
    Calculates the number of duplicates in a list.

    :param input_list: list - List of values
    :return: int - Number of duplicates
    """
    return len(get_duplicates(input_list))


# Partition Methods
# Methods that are carried out on the partitions to support other methods
# ----------------------------------------------------------------------------------------------------------------------

# Returns the position of a given vertex in a given partition
def get_position(vertex, partition):
    """
    Returns the position of a given vertex in a given partition.

    :param vertex: int - Single vertex
    :param partition: Partition Object - Partition object returned by the leiden algorithm
    :return: int - Integer containing the subpart of the partition the vertex is in
    """
    index = 0
    for part in partition:
        if vertex in part:
            break
        index = index + 1
    return index


# Transforms the partition object to a one dimensional array
# The array contains the position of each event class in the partition
def get_list(vertices, partition):
    """
    Transforms the partition object to a one dimensional array. The array contains the position of each event class in
    the partition.

    :param vertices: list - List of vertices you want the position in the partition object from
    :param partition: Partition Object - Partition object returned by the leiden algorithm
    :return: list - List with the position of each given node in the partition
    """
    vertices.sort()
    return_array = list()
    for vertex in vertices:
        position = get_position(vertex, partition)
        return_array.append(position)
    return return_array


# Converts the by the Leiden algorithm identified partition to a x-dimensional list
def convert_partitions_to_list(partition):
    """
    Converts the by the Leiden algorithm identified partition to a x-dimensional list.

    :param partition: Partition Object - Partition object returned by the leiden algorithm
    :return: list - x-dimensional list containing the different communities of the partition
    """
    parts = list()
    for part in partition:
        parts.append(part)
    return parts


# Returns the number of overlaps of all nodes of a list of vertices
# If a vertex shares a successor or a predecessor with an other vertex
# This is referred to as overlap
def get_number_of_overlaps(partition, graph):
    """
    Returns the number of overlaps of all nodes of a list of vertices. If a vertex shares a successor or a predecessor
    with an other vertex. This is referred to as overlap.

    :param partition: list - List of vertices
    :param graph: iGraph object
    :return: int - Number of overlaps of the respective vertices in the partition
    """
    n_overlaps = 0
    for vertex in partition:
        vertex_pre_suc = get_unique_predecessors_successors(vertex, graph)
        for v in partition:
            if not v == vertex:
                v_pre_suc = get_unique_predecessors_successors(v, graph)
                overlap = set(vertex_pre_suc).intersection(v_pre_suc)
                if not len(overlap) == 0:
                    n_overlaps = n_overlaps + 1
                    overlap.clear()
    return n_overlaps


# Calculate the process cohesion-coupling ratio
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Calculate Process Coupling
# ----------------------------------------------------------------------------------------------------------------------

# Calculate average process coupling. The number of communities that have a connection between,
# separated by the number of communities
def calc_avg_process_coupling(partition, graph):
    """
    Calculates the average process coupling. The number of communities that have a connection between.

    :param partition: Partition Object - Partition object returned by the Leiden algorithm
    :param graph: iGraph object
    :return: float - Average process coupling metric
    """
    n_coupled = 0
    for part in partition:
        for p in partition:
            if not part == p:
                edges = graph.es.select(_between=(part, p))
                if len(edges) > 0:
                    n_coupled = n_coupled + 1
    if len(partition) > 0:
        avg_process_coupling = (n_coupled * 2) / len(partition)
    else:
        avg_process_coupling = 0
    return avg_process_coupling


# Calculate total process coupling by dividing the average process coupling with the number of partitions
def calc_process_coupling(partitions, graph):
    """
    Calculate total process coupling by dividing the average process coupling with the number of partitions.

    :param partitions: Partition Object - Partition object returned by the Leiden algorithm
    :param graph: iGraph object
    :return: float - The total process coupling
    """
    avg_pc = calc_avg_process_coupling(partitions, graph)
    if not (len(partitions) or avg_pc) == 0:
        pc = avg_pc / len(partitions)
    else:
        pc = 0
    return pc


# Calculate Process cohesion
# ----------------------------------------------------------------------------------------------------------------------

# Calculate process cohesion of all partitions
def calc_process_cohesion(partitions, graph):
    """
    Calculate the process cohesion of all given partitions in the given graph. This is done by calculating the
    community relation cohesion and divide it with the community information cohesion.

    :param partitions: Partition Object - Partition object returned by the Leiden algorithm
    :param graph: iGraph
    :return: float - Calculated process cohesion
    """
    ch = 0
    for part in partitions:
        crc = calc_community_relation_cohesion(part, graph)
        cic = calc_community_information_cohesion(part, graph)
        ch = ch + (crc * cic)
    ch = ch / len(partitions)
    return ch


# Calculate community relation cohesion
# ......................................................................................................................

# Determines for each event of the given community with how many other events it overlaps by sharing an input or output
def calc_community_relation_cohesion(partition, graph):
    """
    Determines for each event of the given community with how many other events it overlaps by sharing an input or
    output.

    :param partition: Partition Object - Partition object returned by the Leiden algorithm
    :param graph: iGraph
    :return: float - Calculated community relation cohesion
    """
    n_overlaps = get_number_of_overlaps(partition, graph)
    if n_overlaps > 0 and len(partition) > 1:
        avg_ov = ((n_overlaps * 2) / len(partition))
        crc = avg_ov / (len(partition) * len(partition) - 1)
    elif n_overlaps == 0:
        crc = 0
    elif len(partition) == 1:
        crc = n_overlaps
    else:
        crc = 0
    return crc


# Calculate community information cohesion
# ......................................................................................................................

# Calculates the community information cohesion of a given community
def calc_community_information_cohesion(partition, graph):
    """
    Calculates the community information cohesion of a given community. This is done by dividing the number of
    duplicates of all predecessors and successors by the number of vertices in the partition.

    :param partition: list - List of vertices in a community
    :param graph: iGraph object
    :return: float - Calculated community information cohesion
    """
    pre_suc = list()
    for vertex in partition:
        pre_suc.extend(get_unique_predecessors_successors(vertex, graph))
    pre_suc = get_duplicates(pre_suc)
    if len(pre_suc) == 0:
        cic = 0
    else:
        cic = len(pre_suc) / len(partition)
    return cic


# Calculate process coupling cohesion ratio
# ----------------------------------------------------------------------------------------------------------------------
def calc_process_coupling_cohesion_ratio(partitions, graph):
    """
    Calculate the process cohesion coupling ratio of the whole process.

    :param partitions: Partition Object - Partition object returned by the Leiden algorithm
    :param graph: iGraph object
    :return: float - Calculated process cohesion-coupling-ratio
    """
    cp = calc_process_coupling(partitions, graph)
    ch = calc_process_cohesion(partitions, graph)
    if cp == 0 or ch == 0:
        pccr = 0
    else:
        pccr = cp / ch
    return pccr


# Evaluation Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Calculate the modularity Q of the given partition
def get_modularity(partition):
    """
    Calculate the modularity of the given partition.

    :param partition: Partition Object - Partition object created by the Leiden algorithm
    :return: float - Modularity value for the given partition
    """
    q1 = partition.quality()
    return q1


# Calculates the adjusted Rand index
def calc_adjusted_rand_index(ground_truth, communities_detected):
    """
    Calculates the adjusted Rand index.

    :param ground_truth: list - List containing the ground truth of the given dataset
    :param communities_detected: list - List containing the community membership of each vertex
    :return: float - Calculated adjusted Rand index
    """
    ars = adjusted_rand_score(ground_truth, communities_detected)
    return ars


# Calculates the Fowlkes-Mallows Score
def calc_fms(ground_truth, communities_detected):
    """
    Calculates the adjusted Rand index.

    :param ground_truth: list - List containing the ground truth of the given dataset
    :param communities_detected: list - List containing the community membership of each vertex
    :return: float - Calculated Fowlkes-Mallows Score
    """
    fmi = fms(ground_truth, communities_detected)
    return fmi


# Calculates the normalized mutual information
def calc_nmi(ground_truth, communities_detected):
    """
    Calculates the normalized mutual information.

    :param ground_truth: list - List containing the ground truth of the given dataset
    :param communities_detected: list - List containing the community membership of each vertex
    :return: float - Calculated Normalized mutual information
    """
    calculated_nmi = nmi(ground_truth, communities_detected)
    return calculated_nmi

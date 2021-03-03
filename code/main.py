# Imports
import csv
import functions
import gc
import os

from streamlit import caching

# The BPI2015 all and main are the same event logs. I needed to modify the name to BPI2015_main to analyze the main
# process in the iterative manner shown below.

logs = [
    "BPI2015_all_1.xes",
    "BPI2015_all_2.xes",
    "BPI2015_all_3.xes",
    "BPI2015_all_4.xes",
    "BPI2015_all_5.xes",
    "BPI2015_main_1.xes",
    "BPI2015_main_2.xes",
    "BPI2015_main_3.xes",
    "BPI2015_main_4.xes",
    "BPI2015_main_5.xes",
    "BPI2017.xes",
    "BPI2020_DomesticDeclarations.xes",
    "BPI2020_InternationalDeclarations.xes",
    "BPI2020_PermitLog.xes",
    "BPI2020_PrepaidTravelCost.xes",
    "BPI2020_RequestForPayment.xes"
]


def main():
    gc.enable()

    # Create csv file to store evaluation results in
    with open(f"evaluation_results/evaluation_results.csv", 'w', newline='') as csvfile:
        mywriter = csv.writer(csvfile, delimiter=';')
        # write header
        mywriter.writerow(["Log", "Identified communities", "Ground_truth_clusters", "PCCR", "Q", "ARI", "FMS", "NMI"])

    for log_name in logs:

        # Row to store evaluation results of the respective event log
        myrow = list()
        myrow.append(log_name)

        # Due to runtime optimization I already stored the intermediate results for identifying the ground truth in
        # event logs and skipped this step. For completeness I included the steps below, that identify the ground
        # truth and export the event log to the data/logs_with_truth folder.

        # Specify the path
        log_file = f"data/input_logs/{log_name}"

        if os.path.exists(log_file):

            print("\nLoad event log:", log_name)

            # Import, parse and sort the event log
            log = functions.import_log_xes(log_file)

            # Identify the ground truth
            log = functions.identify_ground_truth(log, log_name)

            # Specify the directory to which the event log containing the ground truth needs to be exported
            path = f"data/logs_with_truth/{log_name}"

            # Export the event log to the given directory
            functions.export_log_xes(log, path)

        else:
            print("File path does not exist: ", log_file)

        # Specify the import directory
        log_file = f"data/logs_with_truth/{log_name}"

        if os.path.exists(log_file):
            print("\nLoad event log: ", log_name)

            # Import, parse and sort the event log
            log = functions.import_log_xes(log_file)

            # Create directly follows graph
            dfg = functions.create_directly_follows_graph(log)

            # If the BPI Log is named BPI15M filter the main edges out of the event log
            if "BPI2015_main" in log_name:
                # Source edges from directly follows graph
                edges = functions.filter_main_process_bpi15(dfg)

                # Source vertices from directly follows graph
                vertices = functions.get_vertices(edges)

                # Remove duplicates from the list
                vertices = functions.remove_duplicates(vertices)

                # Initialize list
                ground_truth_partition = list()

                for vertex in vertices:
                    if vertex[9] == "0":
                        ground_truth_partition.append(0)
                    elif vertex[9] == "1":
                        ground_truth_partition.append(1)
                    elif vertex[9] == "2":
                        ground_truth_partition.append(2)
                    elif vertex[9] == "3":
                        ground_truth_partition.append(3)
                    elif vertex[9] == "4":
                        ground_truth_partition.append(3)
                    elif vertex[9] == "5":
                        ground_truth_partition.append(5)
                    elif vertex[9] == "6":
                        ground_truth_partition.append(6)
                    elif vertex[9] == "7":
                        ground_truth_partition.append(7)
                    elif vertex[9] == "8":
                        ground_truth_partition.append(8)

                # Create a directed weighted graph
                graph = functions.create_igraph(edges)

                # Run the Leiden algorithm on the graph and receive the partitions
                partition = functions.run_leiden(graph)

                # Insert the identified communities in the event log
                functions.insert_communities_to_log(log, partition, graph)

                # Convert the discovered communities into an x dimensional array
                partition_list = functions.convert_partitions_to_list(partition)
                myrow.append(len(partition_list))

                # Ground truth is always 10 in BPI 2015 Main
                myrow.append(9)

                # Calculate Process-Cohesion-Coupling Ratio
                pccr = functions.calc_process_coupling_cohesion_ratio(partition_list, graph)
                print("Process-cohesion-coupling-ratio:", pccr)
                myrow.append(pccr)

                # Index the vertices according to the graphs internal vertices, for later evaluation
                vertices = functions.index_vertices(vertices, graph)

                # Transform the partition to a list
                communities_identified = functions.get_list(vertices, partition_list)

                # Calculate modularity Q for partition
                q = functions.get_modularity(partition)
                print("Modularity: ", q)
                myrow.append(q)

                # Calculate adjusted Rand index for respective event log
                ari = functions.calc_adjusted_rand_index(ground_truth_partition, communities_identified)
                print("Adjusted Rand Index: ", ari)
                myrow.append(ari)

                # Calculate Fowlkes-Mallows Score
                fms = functions.calc_fms(ground_truth_partition, communities_identified)
                print("Fowlkes-Mallows Score:", fms)
                myrow.append(fms)

                # Calculate normalized mutual information
                nmi = functions.calc_nmi(ground_truth_partition, communities_identified)
                print("Normalized Mutual Information", nmi)
                myrow.append(nmi)

                # Insert the identified communities into the event log as event attribute
                log = functions.insert_communities_to_log(log, partition, graph)

                # Specify the directory for the export
                path = f"data/output_logs/{log_name}"

                # Export the event log to the specified directory
                functions.export_log_xes(log, path)

            else:
                # Source vertices from directly follows graph
                vertices = functions.get_vertices(dfg)

                # Remove duplicates from the list
                vertices = functions.remove_duplicates(vertices)

                # Create a directed weighted graph
                graph = functions.create_igraph(dfg)

                # Run the Leiden algorithm on the graph and receive the partitions
                partition = functions.run_leiden(graph)

                # Insert the identified communities in the event log
                functions.insert_communities_to_log(log, partition, graph)

                # Convert the discovered communities into an x dimensional array
                partition_list = functions.convert_partitions_to_list(partition)
                myrow.append(len(partition_list))

                # Calculate Process-Cohesion-Coupling Ratio
                pccr = functions.calc_process_coupling_cohesion_ratio(partition_list, graph)
                print("Process-cohesion-coupling-ratio:", pccr)

                # Sort vertices
                vertices.sort()

                # Get the ground truth from the event log
                ground_truth_partition = functions.get_ground_truth(vertices, graph, log)
                myrow.append(len(functions.remove_duplicates(ground_truth_partition)))

                # Append the pccr in the right order to the csv
                myrow.append(pccr)

                # Index the vertices according to the graphs internal vertices, for later evaluation
                vertices = functions.index_vertices(vertices, graph)

                # Transform the partition to list
                communities_identified = functions.get_list(vertices, partition_list)

                # Calculate modularity Q for partition
                q = functions.get_modularity(partition)
                print("Modularity: ", q)
                myrow.append(q)

                # Calculate adjusted Rand index for respective event log
                ari = functions.calc_adjusted_rand_index(ground_truth_partition, communities_identified)
                print("Adjusted Rand Index: ", ari)
                myrow.append(ari)

                # Calculate Fowlkes-Mallows Score
                fms = functions.calc_fms(ground_truth_partition, communities_identified)
                print("Fowlkes-Mallows Score:", fms)
                myrow.append(fms)

                # Calculate normalized mutual information
                nmi = functions.calc_nmi(ground_truth_partition, communities_identified)
                print("Normalized Mutual Information", nmi)
                myrow.append(nmi)

                # Insert the identified communities into the event log as event attribute
                log = functions.insert_communities_to_log(log, partition, graph)

                # Specify the directory for the export
                path = f"data/output_logs/{log_name}"

                # Export the event log to the specified directory
                functions.export_log_xes(log, path)

        else:
            print("File path does not exist: ", log_file)

        # Append evaluation results into the csv file
        with open(f"evaluation_results/evaluation_results.csv", 'a', newline='') as csvfile:
            mywriter = csv.writer(csvfile, delimiter=';')
            mywriter.writerow(myrow)

        caching.clear_cache()

    print("\nDone")


if __name__ == '__main__':
    main()

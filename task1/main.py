import pandas as pd
import json
from graph import Graph

def create_edges(graph, json_data):
    parent = json_data["LabelName"]
    if json_data.get("Subcategory") != None:
        for category in json_data["Subcategory"]:
            child = category["LabelName"]
            graph.add_edge(parent, child)
            create_edges(graph,category)

def convert_label_name_to_encoded_name(dataframe, node_name):
    return dataframe[dataframe.DisplayName == node_name].index[0]

def convert_encoded_name_to_label_name(dataframe, encoded_name):
    try:
        return dataframe.loc[encoded_name].DisplayName
    except:
        return "Unknown"

def  main():
    dataframe = pd.read_csv("oidv6-class-descriptions.csv", index_col=["LabelName"])
    with open("bbox_labels_600_hierarchy.json") as file:
        json_data = json.load(file)
    
    graph = Graph()
    create_edges(graph, json_data)


    node_name = "Doll"
    encoded_node_name = convert_label_name_to_encoded_name(dataframe, node_name)
    # find sibilings
    siblings = graph.find_all_siblings(encoded_node_name)
    siblings_name = [convert_encoded_name_to_label_name(dataframe, sibling) for sibling in siblings]
    print("siblings name: ", siblings_name)
    
    # find ancestors
    ancestors = graph.find_ancesters(encoded_node_name)
    ancenstors_name = [convert_encoded_name_to_label_name(dataframe, ancestor) for ancestor in ancestors][:-1]
    print("ancestor name: ", ancenstors_name)
    
    # find parent class
    print("Parent class name: ", ancenstors_name[-1])
    
    # find both class belongs to same ancestor
    node_name_2 = "Teddy bear"
    encoded_node_name_2 = convert_label_name_to_encoded_name(dataframe, node_name)
    ancestors_2 = graph.find_ancesters(encoded_node_name_2)
    ancenstors_name_2 = [convert_encoded_name_to_label_name(dataframe, ancestor) for ancestor in ancestors_2][:-1]
    if ancenstors_name == ancenstors_name_2:
        print("same ancestors")
    else:
        print("not same ancestors")

if __name__ == '__main__':
    main()
    
from pyvis.network import Network
from typing import Set, Tuple
import  networkx as nx
import os

class BuildGraph():

    graph=nx.DiGraph()
    def __init__(self,edges):

        self.edges:Set[Tuple[str,str]]=edges 

    def build_graph(self)-> None:
        if self.edges is not None:
            for caller,calls in self.edges : 
                BuildGraph.graph.add_edge(caller,calls)

    def get_graph(self)-> nx.DiGraph:
        return BuildGraph.graph
    

    def visualize_graph(self)-> None:
        try : 
            nn=Network(height="100vh",width="100%",directed=True)

            for node in BuildGraph.graph.nodes :
                node_label:str=node.split(':')[-1]
                color="blue"
                if node_label=="main":
                    color="red"
                nn.add_node(node,label=node_label, title=node,color=color,size=20)
            for source,target in BuildGraph.graph.edges: 
                nn.add_edge(source=source,to=target,arrowStrikethrough=True,width=1)

            nn.save_graph("graph.html")
        except Exception as e : 
            
            print('Error : '+e)
  
    def delete_temp_file(self):
        try :
            os.remove("graph.html")
            os.system("rm -rf lib")
        except Exception as e :
            print('Error : '+e)




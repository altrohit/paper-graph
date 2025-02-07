import os
from typing import Dict
import networkx as nx
import matplotlib.pyplot as plt

class PaperGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, paper_data: Dict):
        """
        Build a comprehensive network graph from paper data
        
        Args:
            paper_data (Dict): Paper metadata with related papers
        """
        # Add main paper as central node
        main_title = paper_data.get("title", "Unknown Paper")
        self.graph.add_node(main_title, type="main")

        # Add cited papers (papers this paper cites)
        cited_papers = paper_data.get("cited_papers", [])
        for cited in cited_papers:
            cited_title = cited.get("title", "Unknown Cited Paper")
            self.graph.add_node(cited_title, type="cited")
            # Blue edges for papers cited by the main paper
            self.graph.add_edge(main_title, cited_title, color='blue', type='cited')

        # Add referencing papers (papers that cite this paper)
        referencing_papers = paper_data.get("related_papers", [])
        for referencing in referencing_papers:
            ref_title = referencing.get("title", "Unknown Referencing Paper")
            self.graph.add_node(ref_title, type="referencing")
            # Red edges for papers referencing the main paper
            self.graph.add_edge(ref_title, main_title, color='red', type='referencing')

    def visualize(self, output_file: str = "paper_network.png"):
        """
        Visualize the comprehensive paper network graph
        
        Args:
            output_file (str, optional): Output image filename. Defaults to "paper_network.png".
        """
        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(self.graph, k=0.5, iterations=50)  # improved layout
        
        # Separate node types
        main_nodes = [n for n, d in self.graph.nodes(data=True) if d['type'] == 'main']
        cited_nodes = [n for n, d in self.graph.nodes(data=True) if d['type'] == 'cited']
        referencing_nodes = [n for n, d in self.graph.nodes(data=True) if d['type'] == 'referencing']

        # Draw nodes with different colors and sizes
        nx.draw_networkx_nodes(self.graph, pos, 
                                nodelist=main_nodes, 
                                node_color='green', 
                                node_size=1000,
                                alpha=0.8)
        nx.draw_networkx_nodes(self.graph, pos, 
                                nodelist=cited_nodes, 
                                node_color='blue', 
                                node_size=500,
                                alpha=0.6)
        nx.draw_networkx_nodes(self.graph, pos, 
                                nodelist=referencing_nodes, 
                                node_color='red', 
                                node_size=500,
                                alpha=0.6)
        
        # Draw edges with different colors
        edges = self.graph.edges(data=True)
        blue_edges = [(u, v) for (u, v, d) in edges if d.get('color') == 'blue']
        red_edges = [(u, v) for (u, v, d) in edges if d.get('color') == 'red']
        
        nx.draw_networkx_edges(self.graph, pos, 
                                edgelist=blue_edges, 
                                edge_color='blue', 
                                arrows=True,
                                connectionstyle='arc3,rad=0.1',
                                alpha=0.6)
        nx.draw_networkx_edges(self.graph, pos, 
                                edgelist=red_edges, 
                                edge_color='red', 
                                arrows=True,
                                connectionstyle='arc3,rad=0.1',
                                alpha=0.6)
        
        # Draw labels
        nx.draw_networkx_labels(self.graph, pos, font_size=8, font_weight='bold')
        
        plt.title("Comprehensive Research Paper Network", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        # Ensure outputs directory exists
        os.makedirs("outputs", exist_ok=True)
        plt.savefig(f"outputs/{output_file}", dpi=300, bbox_inches='tight')
        plt.close()

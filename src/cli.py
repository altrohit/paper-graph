from typing import Dict
from rich.console import Console
from rich.table import Table
from .api_client import PaperAPIClient
from .paper_graph import PaperGraph

class PaperExplorerCLI:
    def __init__(self):
        self.console = Console()
        self.api_client = PaperAPIClient()
        self.paper_graph = PaperGraph()

    def run(self, doi: str):
        """
        Main CLI workflow for paper exploration
        
        Args:
            doi (str): Digital Object Identifier of the paper
        """
        # Fetch paper data
        paper_data = self.api_client.fetch_paper_by_doi(doi)
        
        if not paper_data:
            self.console.print("[red]No paper data found![/red]")
            return

        # Display paper details
        self._display_paper_details(paper_data)

        # Build and visualize graph
        self.paper_graph.build_graph(paper_data)
        self.paper_graph.visualize()

        # Save data to JSON
        self.api_client.save_to_json(paper_data)

    def _display_paper_details(self, paper_data: Dict):
        """
        Display paper details in a rich table
        
        Args:
            paper_data (Dict): Paper metadata
        """
        table = Table(title="Paper Details")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("Title", paper_data.get("title", "N/A"))
        table.add_row("Authors", ", ".join(paper_data.get("authors", [])))
        table.add_row("Year", str(paper_data.get("year", "N/A")))
        table.add_row("Related Papers", str(len(paper_data.get("related_papers", []))))

        self.console.print(table)

        # Display related papers
        related_table = Table(title="Related Papers")
        related_table.add_column("Title", style="green")
        related_table.add_column("Year", style="yellow")
        related_table.add_column("DOI", style="red")

        for paper in paper_data.get("related_papers", []):
            related_table.add_row(
            paper.get("title", "N/A"), 
            str(paper.get("year", "N/A")),
            paper.get("doi", "N/A")
            )

        self.console.print(related_table)

        cited_table = Table(title="Cited Papers")
        cited_table.add_column("Title", style="blue")
        cited_table.add_column("Year", style="yellow")
        cited_table.add_column("DOI", style="red")

        for paper in paper_data.get("cited_papers", []):
            cited_table.add_row(
                paper.get("title", "N/A"), 
                str(paper.get("year", "N/A")),
                paper.get("doi", "N/A")
            )

        self.console.print(cited_table)
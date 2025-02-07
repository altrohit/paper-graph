import re
import requests
import json
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class PaperAPIClient:
    def __init__(self):
        # Configure API clients
        self.semantic_scholar_base_url = "https://api.semanticscholar.org/v1"
        self.crossref_base_url = "https://api.crossref.org/works"

    def fetch_paper_by_doi(self, doi: str) -> Dict:
        """
        Fetch paper details using DOI from Semantic Scholar
        
        Args:
            doi (str): Digital Object Identifier of the paper
        
        Returns:
            Dict: Paper metadata and related papers
        """
        try:
            # Extract DOI from DOI link if necessary
            if doi.startswith("http"):
                doi = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", doi, re.IGNORECASE).group(0)
            
            # Semantic Scholar API call
            ss_url = f"{self.semantic_scholar_base_url}/paper/{doi}"
            response = requests.get(ss_url)
            
            if response.status_code == 200:
                paper_data = response.json()
                
                # Fetch related papers
                related_papers = self._fetch_related_papers(paper_data)
                
                # Fetch cited papers
                cited_papers = self._fetch_cited_papers(paper_data)
                
                return {
                    "title": paper_data.get("title", "Unknown"),
                    "authors": [author.get("name", "Unknown") for author in paper_data.get("authors", [])],
                    "year": paper_data.get("year"),
                    "related_papers": related_papers,
                    "cited_papers": cited_papers
                }
            else:
                raise Exception(f"Failed to fetch paper. Status code: {response.status_code}")

        except Exception as e:
            print(f"Error fetching paper: {e}")
            return {}

    def _fetch_related_papers(self, paper_data: Dict, limit: int = 10) -> List[Dict]:
        """
        Extract related papers from Semantic Scholar response
        
        Args:
            paper_data (Dict): Original paper data
            limit (int, optional): Max number of related papers. Defaults to 10.
        
        Returns:
            List[Dict]: List of related paper details
        """
        related = []
        citations = paper_data.get("citations", [])[:limit]
        
        for citation in citations:
            related.append({
                "title": citation.get("title", "Unknown"),
                "doi": citation.get("doi"),
                "year": citation.get("year")
            })
        
        return related
    
    def _fetch_cited_papers(self, paper_data: Dict, limit: int = 10) -> List[Dict]:
        """
        Extract papers cited by the original paper
        
        Args:
            paper_data (Dict): Original paper data
            limit (int, optional): Max number of cited papers. Defaults to 10.
        
        Returns:
            List[Dict]: List of cited paper details
        """
        cited = []
        references = paper_data.get("references", [])[:limit]
        
        for reference in references:
            cited.append({
                "title": reference.get("title", "Unknown"),
                "doi": reference.get("doi"),
                "year": reference.get("year")
            })
        
        return cited
    
    def save_to_json(self, data: Dict, filename: str = "paper_data.json"):
        """
        Save paper data to a JSON file
        
        Args:
            data (Dict): Paper metadata to save
            filename (str, optional): Output filename. Defaults to "paper_data.json".
        """
        os.makedirs("outputs", exist_ok=True)
        with open(f"outputs/{filename}", "w") as f:
            json.dump(data, f, indent=4)

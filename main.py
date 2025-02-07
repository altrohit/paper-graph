import sys
from src.cli import PaperExplorerCLI
# from app import PaperExplorerApp
from src.app import PaperExplorerApp

def main_cli():
    if len(sys.argv) < 2:
        print("Usage: python main.py <paper_doi>")
        sys.exit(1)

    doi = sys.argv[1]
    cli = PaperExplorerCLI()
    cli.run(doi)


def main():
    app = PaperExplorerApp()
    app.run()

if __name__ == "__main__":
    main_cli()

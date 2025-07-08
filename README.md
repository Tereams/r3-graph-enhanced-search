# R3 Knowledge-Enhanced Search System

A full-stack, graph-powered academic search engine for the **Rice Research Repository (R3)**.  
This system integrates natural language processing, keyword-based knowledge graph construction, and interactive visualizations to provide deeper, more explainable research discovery.

<div align="center">
  <img src="https://repository.rice.edu/assets/rice/images/Rice_Research_Repository_logo_color.png" alt="R3 Logo" width="250" />
</div>

---

## Features

- **Keyphrase Generation** with pretrained T5
- **Knowledge Graph Construction** connecting papers and concepts
- **BM25 + Graph Retrieval** with path explanations
- **Interactive Frontend Visualizations** via Angular + ECharts
- **FastAPI Backend** with `networkx` (no Neo4j dependency!)

---

## Project Structure

```
knowledge\_graph\_builder/        # Keyword extraction & graph building (standalone)
r3-knowledge-search/            # Full-stack application
├── backend/                    # Retrieval API using FastAPI + NetworkX
├── frontend/                   # Angular UI with graph-based search and explanation
```

---

## Technologies

| Layer       | Stack / Tools                       |
| ----------- | ----------------------------------- |
| NLP         | HuggingFace Transformers (T5), BM25 |
| Graph       | NetworkX (GML format, in-memory)    |
| Backend     | FastAPI, Python 3.8+, Uvicorn       |
| Frontend    | Angular 15+, Bootstrap 5, ECharts   |
| Data Format | CSV, JSONL, GML                     |

---

## Module Descriptions

### `knowledge_graph_builder/`

> A standalone preprocessing module to generate a paper–keyword graph.

- Extracts keyphrases from abstracts via T5

- Filters and cleans CSV input

- Constructs a bipartite graph and saves to `.gml`

- Outputs:
  
  - `output.jsonl`, `graph3.gml`, `title_index.json`, `keyword_index.json`
  
📄[View Documentation](knowledge_graph_builder/README.md)

---

### `r3-knowledge-search/backend/`

> FastAPI-based backend with explainable, graph-enhanced search.

- `/search` → BM25 ranking + graph distance aggregation
- `/path/{paper_id}` → Visual explanation of search paths
- Uses NetworkX for graph expansion and reasoning (no Neo4j required)

📄[View Documentation](r3-knowledge-search/backend/README.md)

---

### `r3-knowledge-search/frontend/`

> Interactive Angular frontend with graph display and path explanations.

- Topic evolution and path graphs via ECharts
- Card-style search results with linked metadata
- Pages:
  - `/`: Home + Query input
  - `/search`: Search results + graphs
  - `/graphaccess`: Freeform graph query view

📄 [View Documentation](r3-knowledge-search/frontend/README.md)

---

## ⚠️ Usage Notice

> This project depends on proprietary research data from the **Rice Research Repository (R3)**.  
> The CSV files, keyword lists, and extracted graphs are based on internal datasets that **cannot be made public** due to institutional policy.

- This repository provides the **full application logic and code**, but not the data.
- As a result, this project is **not plug-and-play** and cannot run end-to-end without access to the original dataset.
- If you're a Rice University affiliate and wish to collaborate or reproduce this system, please contact the Fondren Fellows team or repository maintainers.

🔒 _We appreciate your understanding._

---

## ⚡ Quick Start

### Backend

```bash
cd r3-knowledge-search/backend
pip install -r requirements.txt
uvicorn back:app --reload
```

→ Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend

```bash
cd r3-knowledge-search/frontend
npm install
ng serve
```

→ Visit: [http://localhost:4200](http://localhost:4200)

---

## Example Flow

1. User searches for `"climate change"`
2. System uses BM25 to find semantically related keywords
3. Graph expands nearby paper nodes via BFS
4. Scores papers based on distance to keyword triggers
5. Displays results + explanation paths showing **why** they’re relevant*

---

## 🤝 Acknowledgments

Developed as part of the **Fondren Fellows Program** at **Rice University**
In collaboration with the **R3 technical team** and **Fondren Library**.

# Backend: Knowledge-Graph-Enhanced Retrieval API

This FastAPI backend powers a graph-based academic search engine for Rice University's Research Repository (R3). It uses a lightweight in-memory graph built with `networkx`, enabling efficient reasoning over keyword-article relationships without relying on an external Neo4j database.

---

## Architecture Overview

          ┌─────────────┐
          │   Query     │
          └─────┬───────┘
                ↓
       [ BM25 Keyword Matching ]
                ↓
       [ Graph Expansion via BFS on NetworkX ]
                ↓
       [ Scoring & Explanation Path Calculation ]
                ↓
       [ Result + Explanation Graphs ]

---

## Key Components

### `back.py`

- Main FastAPI application
- Handles core routes:
  - `/search`: BM25-based query + graph expansion + scoring
  - `/path/{paper_id}`: Return explanation path(s) for selected result
  - `/neo4j/...`: **Legacy interface for Neo4j**, currently unused in this build
- Uses global cache from `initializer.py`
- Returns both flat result list and graph summaries (key nodes & papers)

---

## Core Modules

### `initializer.py`

- Loads:
  - Filtered CSV data (`filtered_data.csv`)
  - Candidate keyword list (`new_kwds1.txt`)
  - Graph structure (`graph3.gml`) built using `networkx`
- Precomputes tokenized documents and IDF values for BM25

### `bm25.py`

- Implements simple BM25 scoring with query tokenization
- Selects top-10 relevant keywords for a given user query

### `graph_retrieve.py`

- Expands keyword nodes using breadth-first search (BFS) over NetworkX
- Returns nearby paper nodes within a configurable distance

### `apr.py`

- Runs the Apriori algorithm on keyword-paper mappings
- Finds frequent keyword sets to highlight shared themes in results

### `graph_build.py`

- Constructs the `graph3.gml` file from extracted title/keyword JSONL
- Saves both the graph and index mappings to disk

### `module_test.py`

- Standalone module to simulate query processing pipeline
- Useful for debugging BM25 scoring, BFS graph expansion, and path explanations

---

## API Overview

### `/search`

- **Input**: `?query=deep learning`
- **Output**:
  - `list`: Full list of matching papers (with metadata)
  - `freq_graph`: Topic graph showing frequent shared keywords + papers

### `/path/{paper_id}`

- **Input**: Paper node ID
- **Output**: Shortest graph path(s) from query-triggered keyword to paper

---

## Notes

- **No Neo4j required**: this backend uses NetworkX for in-memory graph traversal to simplify deployment and improve debugging.
- All graphs are prebuilt and loaded from `.gml` files to ensure fast API response.
- Keyword and paper node IDs are integer-based, matching entries in the CSV and JSONL.

---

## 🚀 Running the API

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API

```bash
uvicorn back:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔧 Example Project Structure

```
backend/
├── back.py
├── apr.py
├── bm25.py
├── graph_build.py
├── graph_retrieve.py
├── initializer.py
├── module_test.py
├── graph3.gml
├── filtered_data.csv
├── new_kwds1.txt
├── title_index.json
├── keyword_index.json
└── requirements.txt
```

---

## Sample Query Workflow

1. `/search?query=climate`
2. BM25 ranks relevant keywords
3. Keywords matched to nodes in NetworkX graph
4. Paper nodes expanded via BFS
5. Distance-based scoring + path explanation
6. Results + graph returned to frontend

---

## Future Work

* [ ] Cache frequent pattern mining results
* [ ] Parallelize graph expansion
* [ ] Add support for multilingual search
* [ ] Restore full Neo4j support as optional backend

---

## 🤝Acknowledgments

This backend system was developed as part of the R3 knowledge graph enhancement project at Rice University, supported by Fondren Library.

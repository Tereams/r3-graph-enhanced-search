# Knowledge Graph Builder

This module constructs a keyword-based knowledge graph from a collection of academic paper metadata, using a transformer-based keyphrase generator and a Neo4j database. It consists of three main components:

---

## 📁 Module Overview

### 1. `preprocess_csv.py`

**Function:**  
Filters and preprocesses the original CSV file by retaining only columns where more than 80% of values are non-empty. Missing or empty entries are filled with `"not available"`.

**Usage:**

```bash
python preprocess_csv.py
```

By default, the filtered result will be saved as `filtered_data.csv`.

---

### 2. `extract_keywords.py`

**Function:**
Uses a pretrained T5-based keyphrase generation model to extract keywords from paper abstracts.

**Input:** A CSV file with at least `id`, `title`, and `abstract` columns.
**Output:** A JSONL file (`output.jsonl`) containing each paper’s title and a list of extracted keywords.

**Usage:**

```bash
python extract_keywords.py
```

Make sure the model is available at `pretrained/keyphrase-generation-t5-small-inspec`.

---

### 3. `build_graph_neo4j.py`

**Function:**
Creates a keyword-title knowledge graph in a Neo4j database.

* Each paper title is represented as a `Title` node.
* Each extracted keyword is represented as a `Keyword` node.
* A `HAS_KEYWORD` relationship connects each title to its associated keywords.

**Usage:**

```bash
python build_graph_neo4j.py
```

Make sure to configure the Neo4j connection (`uri`, `user`, `password`) in the `main()` function. The script will read `output.jsonl` and push the data to the Neo4j graph.

---

## 🔧 Environment & Requirements

* Python 3.8+
* Transformers
* Pandas
* Neo4j Python Driver
* tqdm

**Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## Data Flow

```text
Original CSV
   │
   ▼
[preprocess_csv.py]
   │
   ▼
Filtered CSV
   │
   ▼
[extract_keywords.py]
   │
   ▼
JSONL with titles + keywords
   │
   ▼
[build_graph_neo4j.py]
   │
   ▼
Graph stored in Neo4j (Title --HAS_KEYWORD--> Keyword)
```

---

## Notes

* Abstracts with missing values are skipped during keyword extraction.
* Neo4j node and relationship creation uses `MERGE` to ensure no duplicates.

---

## 🤝 Acknowledgments

Developed as part of the **Fondren Fellows Program** at **Rice University** In collaboration with the **R3 technical team** and **Fondren Library**.

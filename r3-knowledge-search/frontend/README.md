# Frontend: Knowledge-Enhanced Research Search Interface

This Angular frontend provides a modern, interactive search experience for Rice University's Research Repository (R3), enhanced by graph-based keyword visualization. Users can enter queries, view clustered topics, explore how papers are retrieved via graph paths, and access metadata and full-text links.

---

## Key Components

### `home.component`

- Landing page with introduction to the R3 repository.
- Includes a featured search box and community links.
- **Event emitter** forwards queries to the results page.

### `navbar.component`

- Responsive navigation bar.
- Includes logo, repository links, and a link to the Graph Database Search.
- Dropdown menus for browsing by date, author, subject, etc.

### `footer.component`

- Custom footer with:
  - About and support links
  - Contact details for Fondren Library
- Responsive layout using Bootstrap’s grid system

### `search-box.component`

- Simple input with two-way data binding via `ngModel`.
- Emits user-entered queries to parent components using `@Output`.

### `search-results.component`

- Displays a list of search results with:
  - Title (clickable link)
  - Author(s)
  - Abstract (truncated)
- Integrates two graph views:
  1. **Topic Evolution Graph** – common keywords clustered across retrieved results.
  2. **Explanation Graph** – visual path from query to result, showing relevance even when no keyword is explicitly matched.

### `graph.component`

- Reusable graph visualization container
- Used to render both the topic evolution graph and the explanation graph
- Built on **ECharts** for flexible, interactive display
- Receives graph data via Angular input binding (`[graphData]`)

### `graphaccess.component`

- Provides a dedicated interface for direct graph database querying.
- Allows users to explore nearby nodes and relationships within the knowledge graph.
- Renders a full-page graph visualization.

---

## Technologies Used

- **Angular 15+**
- **Bootstrap 5** for styling and layout
- **ECharts** (via `ngx-echarts`) for graph visualizations
- **RxJS** for reactive bindings (if applicable)
- **Two-way binding** (`[(ngModel)]`) and Angular router

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
npm install
```

### 2. Run the development server

```bash
ng serve
```

Open [http://localhost:4200](http://localhost:4200) to view it in the browser.

### 3. Build for production

```bash
ng build
```

---

## Routes Overview

| Route          | Description                        |
| -------------- | ---------------------------------- |
| `/`            | Home page                          |
| `/search`      | Search results page                |
| `/graphaccess` | Keyword graph database exploration |

---

## UI Preview

> *Optionally insert screenshots of:*
> 
> * Search results page with graphs
> * Graph Database Search
> * Home page with repository intro

---

## Notes

* Graphs are dynamically rendered through the `<app-graph>` component.
* Author names are reformatted from `||`-separated strings to comma-separated lists.
* Footer is modular and can be included globally via layout templates.

---

## 📌 To Do / Future Work

* [ ] Add pagination and loading states
* [ ] Improve responsiveness on smaller screens
* [ ] Add user-uploaded document support for search
* [ ] Integrate graph zoom/pan controls
* [ ] Add dark mode toggle

---

## 🤝 Acknowledgments

This UI is part of the Rice Research Repository Enhancement Project, powered by Fondren Library and the Knowledge Graph Integration Team.

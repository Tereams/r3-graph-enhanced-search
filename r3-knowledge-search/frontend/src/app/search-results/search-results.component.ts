import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { GraphComponent } from '../graph/graph.component';

@Component({
  selector: 'app-search-results',
  imports: [CommonModule,GraphComponent],
  templateUrl: './search-results.component.html',
  styleUrl: './search-results.component.css'
})
export class SearchResultsComponent implements OnInit{
  query: string = '';
  results: any[] = [];
  graphData: any = { nodes: [], links: [] };
  selectedGraphData: any = null;

  constructor(private route: ActivatedRoute, private http: HttpClient) {}

  ngOnInit() {
    this.route.queryParams.subscribe((params) => {
      this.query = params['query'] || '';
      console.log('Received query:', this.query);

      if (this.query) {
        this.fetchResults(this.query);
      }
    });
  }

  fetchResults(query: string) {
    const apiUrl = 'http://127.0.0.1:8000/search?query=' + encodeURIComponent(query);
    
    this.http.get<any>(apiUrl).subscribe({
      next: (data) => {
        this.results = data.list;
        this.generateGraphData(data.freq_graph);
      },
      error: (error) => {
        console.error('Error fetching results:', error);
      }
    });
  }

  generateGraphData(freqGraph: any) {
    const truncate = (s: string) => {
      const maxLines = 3;
      const maxPerLine = 8;
      const maxChars = maxLines * maxPerLine;
    
      if (s.length <= maxChars) {
        // 按每行切分，不足三行也照样切行
        const lines = [];
        for (let i = 0; i < s.length; i += maxPerLine) {
          lines.push(s.slice(i, i + maxPerLine));
        }
        return lines.join('\n');
      } else {
        // 超过最大字符数，取前面部分 + 省略号
        const truncated = s.slice(0, maxChars - 1); // 保留一位给 …
        const lines = [];
        for (let i = 0; i < truncated.length; i += maxPerLine) {
          lines.push(truncated.slice(i, i + maxPerLine));
        }
        // 在最后一行加 …
        lines[lines.length - 1] += '…';
        return lines.join('\n');
      }
    };
  
    const key_nodes = freqGraph.key_nodes;
    const paper_nodes = freqGraph.paper_nodes;
  
    const categoryIndexMap = {
      Keyword: 0,
      Query: 1,
      Paper: 2
    };
  
    const nodes: { id: string; name: string; category: number; value?: any; symbolSize?: number; x?: number; y?: number }[] = [];
    const links: { source: string; target: string; value?: string; symbol?: [string, string]; symbolSize?: number }[] = [];
  
    // 设置关键字节点位置：均匀排在上方
    key_nodes.forEach((n:any, i:any) => {
      nodes.push({
        id: `k${i}`,
        name: n.name,
        category: categoryIndexMap['Keyword'],
        symbolSize: 25,
        x: 400 + i * 250,
        y: 80
      });
    });
  
    // 设置论文节点横向排布 + 时间轴连接
    paper_nodes.forEach((n:any, i:any) => {
      const paperId = `p${i}`;
      nodes.push({
        id: paperId,
        name: `${truncate(n.name)}\n${n.date}`,
        category: categoryIndexMap['Paper'],
        value: n.date,
        symbolSize: 30,
        x: 100 + i * 150,
        y: 300
      });
  
      // 时间线上的箭头连接
      if (i > 0) {
        links.push({
          source: `p${i - 1}`,
          target: paperId,
          symbol: ['none', 'arrow'],
          symbolSize: 10
        });
      }
  
      // 每个 keyword 连向当前 paper
      key_nodes.forEach((_:any, ki:any) => {
        links.push({
          source: `k${ki}`,
          target: paperId
        });
      });
    });
  
    this.graphData = {
      nodes,
      links,
      categories: ['Keyword', 'Query', 'Paper'].map(name => ({ name }))
    };
  }

  convertToGraphData(raw: any): any {
    const truncate = (s: string) => {
      const maxLines = 3;
      const maxPerLine = 8;
      const maxChars = maxLines * maxPerLine;
  
      if (s.length <= maxChars) {
        const lines = [];
        for (let i = 0; i < s.length; i += maxPerLine) {
          lines.push(s.slice(i, i + maxPerLine));
        }
        return lines.join('\n');
      } else {
        const truncated = s.slice(0, maxChars - 1);
        const lines = [];
        for (let i = 0; i < truncated.length; i += maxPerLine) {
          lines.push(truncated.slice(i, i + maxPerLine));
        }
        lines[lines.length - 1] += '…';
        return lines.join('\n');
      }
    };
    
    const graphNodes: any[] = [];
    const graphLinks: any[] = [];
    const nodeMap = new Map<string, any>();

    const categoryNameList = ['Keyword', 'Query', 'Paper'];  // 对应 legend 顺序
    const labelToCategoryIndex: any = {
      keyword: 0,
      center: 1,
      title: 2
    };

    const centerX = 200;
    const centerY = 200;

    // 中心 query 节点
    const coreName = truncate(raw.query_name);
    nodeMap.set(coreName, {
      name: coreName,
      fullName: raw.query_name,
      uri: raw.query_uri,
      category: labelToCategoryIndex['center'],
      x: centerX,
      y: centerY,
      symbolSize: 35
    });

    // 每条路径横向展开，路径内纵向排列
    const pathSpacingX = 180;
    const pathSpacingY = 100;

    raw.paths.forEach((path: any[], pathIdx: number) => {
      let prevName = coreName;
      const offsetX = centerX + (pathIdx - (raw.paths.length - 1) / 2) * pathSpacingX;

      for (let i = path.length - 1; i >= 0; i--) {
        const node = path[i];
        const name = node.label === 'title' ? truncate(node.name) : node.name;

        if (!nodeMap.has(name)) {
          nodeMap.set(name, {
            name,
            fullName: node.name,
            uri: node.uri,
            category: labelToCategoryIndex[node.label],
            x: offsetX,
            y: centerY + (path.length - i) * pathSpacingY,
            symbolSize: node.label === 'title' ? 30 : 25
          });
        }

        graphLinks.push({ source: name, target: prevName });
        prevName = name;
      }
    });

    return {
      nodes: Array.from(nodeMap.values()),
      links: graphLinks,
      categories: categoryNameList.map(name => ({ name }))
    };
  }
  
  // convertToGraphData(raw: any): any {
  //   const truncate = (s: string) => s.length > 6 ? s.slice(0, 6) + '…' : s;
  //   const graphNodes: any[] = [];
  //   const graphLinks: any[] = [];
  //   const nodeMap = new Map<string, any>();
  
  //   const categoryMap: any = {
  //     center: 'Query',
  //     title: 'Paper',
  //     keyword: 'Keyword'
  //   };
  
  //   // 中心节点
  //   const coreName = truncate(raw.query_name);
  //   nodeMap.set(coreName, {
  //     name: coreName,
  //     fullName: raw.query_name,
  //     uri: raw.query_uri,
  //     category: categoryMap['center']
  //   });
  
  //   // 所有路径中的节点
  //   for (const path of raw.paths) {
  //     let prevName = coreName;
  //     for (let i = path.length - 1; i >= 0; i--) {
  //       const node = path[i];
  //       const name = node.label === 'title' ? truncate(node.name) : node.name;
  
  //       if (!nodeMap.has(name)) {
  //         nodeMap.set(name, {
  //           name,
  //           fullName: node.name,
  //           uri: node.uri,
  //           category: categoryMap[node.label] || node.label
  //         });
  //       }
  //       graphLinks.push({ source: name, target: prevName });
  //       prevName = name;
  //     }
  //   }
  
  //   return {
  //     nodes: Array.from(nodeMap.values()),
  //     links: graphLinks,
  //     categories: ['Keyword','Query', 'Paper']
  //   };
  // }

  loadGraphForItem(result: any) {
    // const mockData = {
    //   query_name: "Modular video endoscopy for in vivo cross-polarized and vital-dye fluorescence imaging of Barrett's-associated neoplasia",
    //   query_uri: 'https://hdl.handle.net/1911/70723',
    //   paths: [
    //     [
    //       { name: 'fluorescence', label: 'keyword', uri: null }
    //     ],
    //     [
    //       { name: "barrett's esophagus", label: 'keyword', uri: null },
    //       { name: 'Quantitative evaluation of in vivo vital-dye fluorescence endoscopic imaging for the detection of Barrett’s-associated neoplasia', label: 'title', uri: 'https://hdl.handle.net/1911/80841' },
    //       { name: 'fluorescence imaging', label: 'keyword', uri: null }
    //     ]
    //   ]
    // };
      const paperId = result['id'];  // 或者你想用的唯一标识字段

      const encodedId = encodeURIComponent(paperId);
      const apiUrl = `http://127.0.0.1:8000/path/${encodedId}`;

      this.http.get<any>(apiUrl).subscribe({
        next: (data) => {
          this.selectedGraphData = this.convertToGraphData(data);
        },
        error: (err) => {
          console.error(`Failed to load graph data for paper ID ${paperId}:`, err);
        }
      });
    }
    // this.selectedGraphData = this.convertToGraphData(mockData);
}

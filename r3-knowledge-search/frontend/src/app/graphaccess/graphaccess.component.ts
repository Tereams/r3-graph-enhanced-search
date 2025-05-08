import {
  Component,
  ElementRef,
  AfterViewInit,
  OnChanges,
  SimpleChanges,
  HostListener,
  OnInit
} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as echarts from 'echarts';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-graphaccess',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './graphaccess.component.html',
  styles: ['.graph-container { width: 100%; height: 100%; min-height: 500px; }']
})
export class GraphaccessComponent implements OnInit, AfterViewInit, OnChanges {
  
  graphData: any = null;
  searchQuery: string = '';
  private chart!: echarts.ECharts;

  constructor(private http: HttpClient, private el: ElementRef) {}

  search(): void {
    const trimmed = this.searchQuery.trim();
    if (!trimmed) return;
  
    this.http.get(`http://localhost:8000/neo4j/search?query=${encodeURIComponent(trimmed)}`)
      .subscribe(data => {
        this.graphData = data;
        this.updateChart();
      });
  }

  ngOnInit(): void {
    this.http.get('http://localhost:8000/neo4j/default').subscribe(data => {
      this.graphData = data;
      this.updateChart();
    });
  }

  ngAfterViewInit(): void {
    this.initChart();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['graphData'] && this.chart) {
      this.updateChart();
    }
  }

  private initChart(): void {
    const element = this.el.nativeElement.querySelector('.graph-container');
    if (element) {
      this.chart = echarts.init(element);
      this.updateChart();
      this.resizeChart();
    }
  }

  private updateChart(): void {
    if (!this.graphData || !this.chart) return;

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

    const option = {
      tooltip: {},
      series: [
        {
          type: 'graph',
          layout: 'force',
          roam: true,
          label: {
            show: true,
            position: 'right',
            formatter: (x: any) => x.data.name
          },
          force: {
            repulsion: 300,
            edgeLength: 150
          },
          data: this.graphData.nodes.map((n: any) => {
            const label = n.labels?.[0] || 'Other';
          
            // 设置颜色
            const color = label === 'Keyword'
              ? '#5470C6'   // 蓝色
              : label === 'Title'
                ? '#91CC75' // 绿色
                : '#CCCCCC'; // 默认灰色
            const displayName = label === 'Title' ? truncate(n.name) : n.name;
            return {
              id: n.id.toString(),
              name: displayName,
              category: 0,
              symbolSize: 30,
              itemStyle: { color }
            };
          }),
          links: this.graphData.links.map((l: any) => ({
            source: l.source.toString(),
            target: l.target.toString(),
            label: { show: true, formatter: l.type || '' }
          }))
        }
      ]
    };

    this.chart.setOption(option);
  }

  @HostListener('window:resize')
  resizeChart(): void {
    if (this.chart) {
      this.chart.resize();
    }
  }
}

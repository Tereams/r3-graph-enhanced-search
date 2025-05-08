import { Component, Input, OnChanges, SimpleChanges, ElementRef, AfterViewInit, HostListener } from '@angular/core';
import * as echarts from 'echarts';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-graph',
  standalone: true,
  imports: [CommonModule],
  template: '<div class="graph-container" #chartContainer></div>',
  styles: ['.graph-container { width: 100%; height: 100%; min-height: 300px; }']
})
export class GraphComponent implements AfterViewInit, OnChanges {
  @Input() graphData: any;
  private chart!: echarts.ECharts;

  constructor(private el: ElementRef) {}

  ngAfterViewInit() {
    this.initChart();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['graphData'] && this.chart) {
      this.updateChart();
    }
  }

  private initChart() {
    const element = this.el.nativeElement.querySelector('.graph-container');
    if (element) {
      this.chart = echarts.init(element);
      this.updateChart();
      this.resizeChart();
    }
  }

  private updateChart() {
    if (!this.graphData || !this.graphData.nodes || this.graphData.nodes.length === 0) return;

    const categoryColors: string[] = ['#1f77b4', '#ff7f0e', '#2ca02c']; // Keyword, Query, Paper

    const option = {
      legend: {
        data: this.graphData.categories.map((c: any) => c.name),
        orient: 'vertical',
        left: 'right'
      },
      series: [
        {
          type: 'graph',
          layout: 'none',
          // edgeSymbol: ['none', 'arrow'],  // ✅ 添加箭头
          edgeSymbolSize: 15,
          roam: true,
          categories: this.graphData.categories.map((c: any, i: number) => ({
            name: c.name,
            itemStyle: { color: categoryColors[i] }
          })),
          data: this.graphData.nodes.map((node: any) => ({
            ...node,
            symbolSize: [20, 25, 30][node.category] ?? 20  // category: 0,1,2
          })),
          links: this.graphData.links,
          label: {
            show: true,
            position: 'bottom'
          },
          lineStyle: {
            color: 'source',
            width: 1.5,
            curveness: 0
          }
        }
      ]
    };

    this.chart.setOption(option);

    this.chart.off('click');
    this.chart.on('click', (params: any) => {
      const node = params.data;
      if (node && node.uri) {
        window.open(node.uri, '_blank');
      }
    });
  }

  @HostListener('window:resize')
  resizeChart() {
    if (this.chart) {
      this.chart.resize();
    }
  }
}

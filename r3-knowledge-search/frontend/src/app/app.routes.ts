import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component'; // app-home 对应的组件
import { SearchResultsComponent } from './search-results/search-results.component';
import { GraphaccessComponent } from './graphaccess/graphaccess.component'; // app-searchres 对应的组件

export const appRoutes: Routes = [
  { path: '', component: HomeComponent }, // 默认路由
  { path: 'search', component: SearchResultsComponent }, // 搜索结果页面
  { path: 'graphaccess', component: GraphaccessComponent },
  { path: '**', redirectTo: '', pathMatch: 'full' }, // 未匹配路由重定向到首页
];

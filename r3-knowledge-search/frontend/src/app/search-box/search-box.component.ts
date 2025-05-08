import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-search-box',
  imports: [FormsModule],
  templateUrl: './search-box.component.html',
  styleUrl: './search-box.component.css'
})
export class SearchBoxComponent {
  query: string = '';

  @Output() searchQuery = new EventEmitter<string>();

  onSearch() {
    if (this.query.trim()) {
      this.searchQuery.emit(this.query); // 向父组件传递输入值
    }
  }
}

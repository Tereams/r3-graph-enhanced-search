import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { SearchBoxComponent } from "../search-box/search-box.component";

@Component({
  selector: 'app-home',
  imports: [SearchBoxComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  constructor(private router: Router) {}

  search(query: string) {
    if (query.trim()) {
      this.router.navigate(['/search'], { queryParams: { query } });
    }
  }
}

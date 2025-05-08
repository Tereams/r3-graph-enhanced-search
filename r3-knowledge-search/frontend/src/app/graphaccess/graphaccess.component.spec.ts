import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GraphaccessComponent } from './graphaccess.component';

describe('GraphaccessComponent', () => {
  let component: GraphaccessComponent;
  let fixture: ComponentFixture<GraphaccessComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GraphaccessComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GraphaccessComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

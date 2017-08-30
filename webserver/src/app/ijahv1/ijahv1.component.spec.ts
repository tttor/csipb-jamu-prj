import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Ijahv1Component } from './ijahv1.component';

describe('Ijahv1Component', () => {
  let component: Ijahv1Component;
  let fixture: ComponentFixture<Ijahv1Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Ijahv1Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Ijahv1Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});

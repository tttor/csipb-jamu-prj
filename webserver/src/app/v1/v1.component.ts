import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'v1',
  styles: [`
  `],
  templateUrl: './v1.component.html'
})
export class V1Component implements OnInit {
  private localState;
  constructor(public route: ActivatedRoute) {
    // do nothing
  }

  public ngOnInit() {
    // do nothing
  }
  private asyncDataWithWebpack() {
    // do nothing
  }

}

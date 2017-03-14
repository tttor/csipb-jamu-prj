import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'v1',
  styles: [`
  `],
  templateUrl: './v1.html'
})
export class V1Component { // tslint:disable-line
  private localState;
  constructor(public route: ActivatedRoute) {
    // do nothing
  }

  private ngOnInit() { // tslint:disable-line
    // do nothing
  }
  private asyncDataWithWebpack() {
    // do nothing
  }

}

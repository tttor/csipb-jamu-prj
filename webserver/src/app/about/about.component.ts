import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'about',
  styles: [`
  `],
  templateUrl: './about.template.html'
})
export class About {
  private localState;
  constructor(public route: ActivatedRoute) {
    // do nothing
  }

  private ngOnInit() {
    // do nothing
  }
  private asyncDataWithWebpack() {
    // do nothing
  }

}

import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'help',
  styles: [`
  `],
  templateUrl: './help.template.html'
})
export class HelpComponent { // tslint:disable-line
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

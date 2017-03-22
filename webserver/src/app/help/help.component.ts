import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'help',
  styles: [`
  `],
  templateUrl: './help.component.html'
})
export class HelpComponent implements OnInit {
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

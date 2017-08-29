import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'disclaimer',
  styles: [`
  `],
  templateUrl: './disclaimer.component.html'
})
export class DisclaimerComponent implements OnInit {
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

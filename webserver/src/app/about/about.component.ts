import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'about',
  styles: [`
  `],
  templateUrl: './about.component.html'
})
export class AboutComponent implements OnInit {
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

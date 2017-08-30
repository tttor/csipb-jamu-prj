import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.css']
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

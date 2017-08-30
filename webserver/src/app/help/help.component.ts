import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-help',
  templateUrl: './help.component.html',
  styleUrls: ['./help.component.css']
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

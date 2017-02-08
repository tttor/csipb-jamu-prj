import { Component, ViewEncapsulation} from '@angular/core';

import { AppState } from './app.service';

@Component({
  selector: 'app',
  encapsulation: ViewEncapsulation.None,
  styleUrls: [
    './app.style.css'
  ],
  templateUrl: './app.html'
})
export class App {


  constructor(
    public appState: AppState) {

  }

  ngOnInit() {
  }

}

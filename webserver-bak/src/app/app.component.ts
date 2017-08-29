import {
  Component,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import { AppState } from './app.service';
import { PageScrollConfig } from 'ng2-page-scroll';

@Component({
  selector: 'app',
  encapsulation: ViewEncapsulation.None,
  styleUrls: [
    './app.component.css'
  ],
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {

  constructor(
    public appState: AppState
  ) {
    PageScrollConfig.defaultDuration = 300;
  }

  public ngOnInit() {
    // Do nothing
  }
}

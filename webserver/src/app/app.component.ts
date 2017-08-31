import { Component } from '@angular/core';

import { WebserverConfig } from './config_webserver';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
   private version: string;

   ngOnInit() {
     this.version = WebserverConfig['version'];
   }
}

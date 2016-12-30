import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'download',
  styles: [`
  `],
  templateUrl: './download.template.html'
})
export class Download {
  localState;
  constructor(public route: ActivatedRoute) {

  }

  ngOnInit() {


  }
  asyncDataWithWebpack() {

  }

}

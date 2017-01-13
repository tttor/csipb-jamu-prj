import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'about',
  styles: [`
  `],
  templateUrl: './about.template.html'
})
export class About {
  localState;
  constructor(public route: ActivatedRoute) {

  }

  ngOnInit() {

  }
  asyncDataWithWebpack() {

  }

}

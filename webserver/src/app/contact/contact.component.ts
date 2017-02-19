import { Component, OnInit, Inject, ElementRef, ViewChild
} from '@angular/core';

import { FormControl, FormGroup
} from '@angular/forms';

@Component({
  selector: 'contact',
  templateUrl: './contact.component.html',
  styleUrls: [ './contact.component.css' ]
})
export class Contact implements OnInit {
  public ngOnInit() {
    // Do nothing
  }

  onSubmit(form: any): void {
    console.log('you submitted value:', form);
  }
}

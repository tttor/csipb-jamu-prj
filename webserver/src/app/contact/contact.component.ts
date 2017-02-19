import { Component, OnInit, Inject, ElementRef, ViewChild
} from '@angular/core';

import { FormControl, FormGroup, FormBuilder, Validators
} from '@angular/forms';

import { Http
} from '@angular/http';

import { ActivatedRoute
} from '@angular/router';

@Component({
  selector: 'contact',
  templateUrl: './contact.component.html',
  styleUrls: [ './contact.component.css' ]
})
export class Contact implements OnInit {

  public ngOnInit() {
    // Do nothing
  }

  constructor(public route: ActivatedRoute) {
    // Do nothing
  }

  onSubmit(value: string): void {
    console.log('you submitted value: ', value);
  }

}

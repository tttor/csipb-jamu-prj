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
  private name;
  private email;
  private affiliation;
  private msg;
  private subject;

  constructor(public route: ActivatedRoute) {
    // Do nothing
  }

  public ngOnInit() {
    // Do nothing
  }


  onSubmit(): void {
    let data = JSON.stringify({name: this.name, email: this.email, affiliation: this.affiliation,
                                message: this.msg, subject: this.subject});

    console.log(data);

    this.name = '';
    this.email = '';
    this.affiliation = '';
    this.msg = '';
    this.subject = '';
  }

}

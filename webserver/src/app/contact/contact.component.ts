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

  private baseAPI = 'http://ijah.apps.cs.ipb.ac.id/api/';
  // private baseAPI ='http://localhost/ijah-api/';// Comment this if you run online!

  constructor(public route: ActivatedRoute, private http: Http) {
    // Do nothing
  }

  public ngOnInit() {
    // Do nothing
  }

  private onSubmit(): void {
    // capture data
    let data = {name:this.name, email:this.email, affiliation:this.affiliation,
                message:this.msg, subject:this.subject};
    let dataStr = JSON.stringify(data);
    // console.log(dataStr);

    // Send data to DB
    let contactAPI = this.baseAPI+'contact.php';
    this.http.post(contactAPI,dataStr).map(res=>res.json()).subscribe(reply => {
      // TODO: acknowledgement and thank you
    })

    // clear fields
    this.name = '';
    this.email = '';
    this.affiliation = '';
    this.msg = '';
    this.subject = '';
  }

}

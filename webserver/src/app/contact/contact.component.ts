import {
  Component, OnInit, Inject, ElementRef, ViewChild
} from '@angular/core';

import {
  FormControl, FormGroup, FormBuilder, Validators
} from '@angular/forms';

import { Http } from '@angular/http';
import { ActivatedRoute } from '@angular/router';

import { WebserverConfig } from '../config_webserver';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent implements OnInit {
  public name;
  public email;
  public affiliation;
  public msg;
  public subject;

  public baseAPI = WebserverConfig['api_url'];

  constructor(public route: ActivatedRoute, private http: Http) {
    // do nothing
  }

  public ngOnInit() {
    // do nothing
  }

  public onSubmit(): void {
    // capture data
    let data = {name: this.name, email: this.email, affiliation: this.affiliation,
                message: this.msg, subject: this.subject};
    let dataStr = JSON.stringify(data);
    // console.log(dataStr);

    // Send data to DB
    let contactAPI = this.baseAPI + 'contact.php';
    this.http.post(contactAPI, dataStr).map((res) => res.json()).subscribe((reply) => {
      // TODO: acknowledgement and thank you
    });

    // clear fields
    this.name = '';
    this.email = '';
    this.affiliation = '';
    this.msg = '';
    this.subject = '';
  }
}

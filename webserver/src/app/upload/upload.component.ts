import { Component, OnInit, Inject, ElementRef, ViewChild
} from '@angular/core';

import { FormControl, FormGroup, FormBuilder, Validators
} from '@angular/forms';

import { Http
} from '@angular/http';

import { ActivatedRoute
} from '@angular/router';

@Component({
  selector: 'upload',
  templateUrl: './upload.component.html',
  styleUrls: [ './upload.component.css' ]
})
export class UploadComponent implements OnInit {
  public type;
  public content1;
  public content2;
  public description;
  public name;
  public email;
  public affiliation;
  public publicationTitle;
  public publicationAuthor;
  public publicationYear;
  public publicationJournal;
  public publicationLink;
  public msg;
  public subject;

  // private baseAPI = 'http://ijah.apps.cs.ipb.ac.id/api/';
  // private baseAPI ='http://localhost/ijah-api/';// Comment this if you run online!
  private baseAPI = 'http://ijah.agri.web.id/api/';

  constructor(public route: ActivatedRoute, private http: Http) {
    // Do nothing
  }

  public ngOnInit() {
    // Do nothing
  }

  public onSubmit(): void {
    // capture data
    let data = {type: this.type, data: this.content1 + ' | ' + this.content2,
                description: this.description, name: this.name, email: this.email,
                affiliation: this.affiliation, publication_detail: this.publicationTitle + ', '
                + this.publicationAuthor + ', ' + this.publicationYear + ', '
                + this.publicationJournal + ', ' + this.publicationLink,
                message: this.msg, subject: this.subject};
    let dataStr = JSON.stringify(data);
    // console.log(dataStr);

    // Send data to DB
    let uploadAPI = this.baseAPI + 'upload.php';
    this.http.post(uploadAPI, dataStr).map((res) => res.json()).subscribe((reply) => {
      // TODO: acknowledgement and thank you
    });

    // clear fields
    this.type = '';
    this.content1 = '';
    this.content2 = '';
    this.description = '';
    this.name = '';
    this.email = '';
    this.affiliation = '';
    this.publicationTitle = '';
    this.publicationAuthor = '';
    this.publicationYear = '';
    this.publicationJournal = '';
    this.publicationLink = '';
    this.msg = '';
    this.subject = '';
  }

}

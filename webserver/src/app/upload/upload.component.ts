import { Component, OnInit, Inject, ElementRef, ViewChild } from '@angular/core';
import { FormControl, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Http, Headers } from '@angular/http';
import { ActivatedRoute } from '@angular/router';
import { FileUploader } from 'ng2-file-upload';

import { WebserverConfig } from '../config_webserver';

const uploadURL = 'http://ijah.apps.cs.ipb.ac.id/api-node/upload';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
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
  public uploader: FileUploader = new FileUploader({url: uploadURL});
  public hasBaseDropZoneOver: boolean = false;

  public baseAPI = WebserverConfig['api_url'];

  constructor(public route: ActivatedRoute, private http: Http) {
  // do nothing
 }

  public ngOnInit() {
    this.uploader.onAfterAddingFile = (file) => { file.withCredentials = false; };
  }

  public onSubmit(): void {
    // capture data
    let data = {type: this.type, data: this.content1 + ' | ' + this.content2,
                description: this.description, name: this.name, email: this.email,
                affiliation: this.affiliation, publication_detail: this.publicationTitle + ', '
                + this.publicationAuthor + ', ' + this.publicationYear + ', '
                + this.publicationJournal + ', ' + this.publicationLink};
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
  }

  public fileOverBase(e: any): void {
    this.hasBaseDropZoneOver = e;
  }
}

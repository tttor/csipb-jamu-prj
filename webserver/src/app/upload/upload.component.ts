import { Component, OnInit, Inject, ElementRef, ViewChild } from '@angular/core';
import { FormControl, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Http, Headers } from '@angular/http';
import { ActivatedRoute } from '@angular/router';
import { FileUploader } from 'ng2-file-upload';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.css']
})
export class UploadComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}

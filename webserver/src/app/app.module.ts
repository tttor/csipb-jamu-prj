import { BrowserModule } from '@angular/platform-browser';
import { NgModule, ApplicationRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule, Http, RequestOptions } from '@angular/http';
import { RouterModule, PreloadAllModules } from '@angular/router';
import { LocationStrategy, HashLocationStrategy } from '@angular/common';
import { CommonModule } from "@angular/common";
import { enableProdMode } from '@angular/core';

import { Ng2PageScrollModule } from 'ng2-page-scroll';
import { FileUploadModule } from 'ng2-file-upload';
import { ChartsModule } from 'ng2-charts';
import { TreeviewModule } from 'ngx-treeview';

import { ROUTES } from './app.routes';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';
import { ContactComponent } from './contact/contact.component';
import { DownloadComponent } from './download/download.component';
import { HelpComponent } from './help/help.component';
import { Ijahv1Component } from './ijahv1/ijahv1.component';
import { UploadComponent } from './upload/upload.component';

enableProdMode();

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    AboutComponent,
    ContactComponent,
    DownloadComponent,
    HelpComponent,
    Ijahv1Component,
    UploadComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(ROUTES, { useHash: true }),
    FormsModule,
    HttpModule,
    FileUploadModule,
    ChartsModule,
    Ng2PageScrollModule.forRoot(),
    TreeviewModule.forRoot(),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

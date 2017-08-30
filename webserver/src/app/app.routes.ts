import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';
import { ContactComponent } from './contact/contact.component';
import { DownloadComponent } from './download/download.component';
import { HelpComponent } from './help/help.component';
import { Ijahv1Component } from './ijahv1/ijahv1.component';
import { UploadComponent } from './upload/upload.component';

export const ROUTES: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home',  component: HomeComponent, pathMatch: 'full' },
  { path: 'downloads', component: DownloadComponent, pathMatch: 'full' },
  { path: 'upload', component: UploadComponent, pathMatch: 'full' },
  { path: 'help-faq', component: HelpComponent, pathMatch: 'full' },
  { path: 'ijahv1', component: Ijahv1Component, pathMatch: 'full' },
  { path: 'contact', component: ContactComponent, pathMatch: 'full' },
  { path: 'about', component: AboutComponent, pathMatch: 'full' },
];

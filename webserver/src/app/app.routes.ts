import { Routes } from '@angular/router';
import { HomeComponent } from './home';
import { DownloadComponent } from './download';
import { UploadComponent } from './upload';
import { HelpComponent } from './help';
import { DisclaimerComponent } from './disclaimer';
import { V1Component } from './v1';
import { ContactComponent } from './contact';
import { AboutComponent } from './about';
import { DataResolver } from './app.resolver';

export const ROUTES: Routes = [
  { path: '',      component: HomeComponent },
  { path: 'home',  component: HomeComponent },
  { path: 'downloads', component: DownloadComponent },
  { path: 'upload', component: UploadComponent },
  { path: 'help-faq', component: HelpComponent },
  { path: 'disclaimer', component: DisclaimerComponent },
  { path: 'ijahv1', component: V1Component },
  { path: 'contact', component: ContactComponent },
  { path: 'about', component: AboutComponent },
];

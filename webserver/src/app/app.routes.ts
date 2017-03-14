import { Routes } from '@angular/router';
import { Home } from './home';
import { ManualComponent } from './manual';
import { DownloadComponent } from './download';
import { HelpComponent } from './help';
import { DisclaimerComponent } from './disclaimer';
import { V1Component } from './v1';
import { ContactComponent } from './contact';
import { AboutComponent } from './about';
import { DataResolver } from './app.resolver';

export const ROUTES: Routes = [
  { path: '',      component: Home },
  { path: 'home',  component: Home },
  { path: 'manual',  component: ManualComponent },
  { path: 'downloads', component: DownloadComponent },
  { path: 'help-faq', component: HelpComponent },
  { path: 'disclaimer', component: DisclaimerComponent },
  { path: 'ijahv1', component: V1Component },
  { path: 'contact', component: ContactComponent },
  { path: 'about', component: AboutComponent },
];

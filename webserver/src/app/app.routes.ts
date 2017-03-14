import { Routes } from '@angular/router';
import { Home } from './home';
import { Manual } from './manual';
import { Download } from './download';
import { Help } from './help';
import { Disclaimer } from './disclaimer';
import { V1Component } from './v1';
import { Contact } from './contact';
import { AboutComponent } from './about';
import { DataResolver } from './app.resolver';

export const ROUTES: Routes = [
  { path: '',      component: Home },
  { path: 'home',  component: Home },
  { path: 'manual',  component: Manual },
  { path: 'downloads', component: Download },
  { path: 'help-faq', component: Help },
  { path: 'disclaimer', component: Disclaimer },
  { path: 'ijahv1', component: V1Component },
  { path: 'contact', component: Contact },
  { path: 'about', component: AboutComponent },
];

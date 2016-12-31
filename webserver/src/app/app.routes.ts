import { Routes, RouterModule } from '@angular/router';

import { Home } from './home';
import { Manual } from './manual';
import { Download } from './download';
import { Help } from './help';
import { Disclaimer } from './disclaimer';
import { V1 } from './v1';
import { About } from './about';

import { DataResolver } from './app.resolver';


export const ROUTES: Routes = [
  { path: '',      component: Home },
  { path: 'home',  component: Home },
  { path: 'manual',  component: Manual },
  { path: 'downloads', component: Download },
  { path: 'help-faq', component: Help },
  { path: 'disclaimer', component: Disclaimer },
  { path: 'ijahv1', component: V1 },
  { path: 'about', component: About },
];

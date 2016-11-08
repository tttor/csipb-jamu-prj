import { Routes, RouterModule } from '@angular/router';
import { Home } from './home';
import { About } from './about';
import { Disclaimer } from './disclaimer';
import { Download } from './download';
import { Help } from './help';
import { NoContent } from './no-content';

import { DataResolver } from './app.resolver';


export const ROUTES: Routes = [
  { path: '',      component: Home },
  { path: 'home',  component: Home },
  { path: 'about', component: About },
  { path: 'downloads', component: Download },
  { path: 'help-faq', component: Help },
  { path: 'disclaimer', component: Disclaimer },
  {
    path: 'manual', loadChildren: () => System.import('./+detail')
  },
  { path: '**',    component: NoContent },
];

import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';

export const ROUTES: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home',  component: HomeComponent, pathMatch: 'full' },
];

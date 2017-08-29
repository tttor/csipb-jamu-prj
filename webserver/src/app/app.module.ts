import { BrowserModule } from '@angular/platform-browser';
import { NgModule, ApplicationRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule, Http, RequestOptions } from '@angular/http';
import { RouterModule } from '@angular/router';
import { LocationStrategy, HashLocationStrategy } from '@angular/common';
import { CommonModule } from "@angular/common";
import { enableProdMode } from '@angular/core';

import { ROUTES } from './app.routes';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';

enableProdMode();

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(ROUTES, { useHash: true }),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

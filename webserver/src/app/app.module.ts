import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { TypeaheadModule } from 'ng2-bootstrap/typeahead';
import { Ng2PageScrollModule } from 'ng2-page-scroll';
import { FileUploadModule } from 'ng2-file-upload';
import { ChartsModule } from 'ng2-charts';
import { DropdownTreeviewModule } from 'ng2-dropdown-treeview';
import {
  NgModule,
  ApplicationRef
} from '@angular/core';
import {
  removeNgStyles,
  createNewHosts,
  createInputTransfer
} from '@angularclass/hmr';
import {
  RouterModule,
  PreloadAllModules
} from '@angular/router';

import { ENV_PROVIDERS } from './environment';
import { ROUTES } from './app.routes';
import { AppComponent } from './app.component';
import { APP_RESOLVER_PROVIDERS } from './app.resolver';
import { AppState, InternalStateType } from './app.service';
import { HomeComponent } from './home';
import { DownloadComponent } from './download';
import { UploadComponent } from './upload';
import { HelpComponent } from './help';
import { DisclaimerComponent } from './disclaimer';
import { IjahV1Component } from './ijahv1';
import { ContactComponent } from './contact';
import { AboutComponent } from './about';
import { TestComponent } from './test';

import '../styles/styles.scss';
import '../styles/headings.css';
import '../assets/js/chart.js/src/chart.js';

const APP_PROVIDERS = [
  ...APP_RESOLVER_PROVIDERS,
  AppState
];

type StoreType = {
  state: InternalStateType,
  restoreInputValues: () => void,
  disposeOldHosts: () => void
};

@NgModule({
  bootstrap: [ AppComponent ],
  declarations: [
    AppComponent,
    HomeComponent,
    HelpComponent,
    DownloadComponent,
    UploadComponent,
    DisclaimerComponent,
    IjahV1Component,
    ContactComponent,
    AboutComponent,
    TestComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    FileUploadModule,
    ChartsModule,
    Ng2PageScrollModule.forRoot(),
    TypeaheadModule.forRoot(),
    DropdownTreeviewModule.forRoot(),
    RouterModule.forRoot(ROUTES, { useHash: true, preloadingStrategy: PreloadAllModules })
  ],
  providers: [
    ENV_PROVIDERS,
    APP_PROVIDERS
  ]
})
export class AppModule {

  constructor(
    public appRef: ApplicationRef,
    public appState: AppState
  ) {}

  public hmrOnInit(store: StoreType) {
    if (!store || !store.state) {
      return;
    }
    console.log('HMR store', JSON.stringify(store, null, 2));
    this.appState._state = store.state;
    if ('restoreInputValues' in store) {
      let restoreInputValues = store.restoreInputValues;
      setTimeout(restoreInputValues);
    }

    this.appRef.tick();
    delete store.state;
    delete store.restoreInputValues;
  }

  public hmrOnDestroy(store: StoreType) {
    const cmpLocation = this.appRef.components.map((cmp) => cmp.location.nativeElement);
    const state = this.appState._state;
    store.state = state;
    store.disposeOldHosts = createNewHosts(cmpLocation);
    store.restoreInputValues  = createInputTransfer();
    removeNgStyles();
  }

  public hmrAfterDestroy(store: StoreType) {
    store.disposeOldHosts();
    delete store.disposeOldHosts;
  }

}

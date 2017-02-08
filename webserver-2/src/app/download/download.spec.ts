import { ActivatedRoute } from '@angular/router';
import { Component } from '@angular/core';
import {
  addProviders,
  inject,
  TestComponentBuilder
} from '@angular/core/testing';
import { TestBed } from '@angular/core/testing/test_bed';

// Load the implementations that should be tested
import { Download } from './download.component';

describe('Download', () => {
  // provide our implementations or mocks to the dependency injector
  beforeEach(() => TestBed.configureTestingModule({
    providers: [
      // provide a better mock
      {
        provide: ActivatedRoute,
        useValue: {
          data: {
            subscribe: (fn) => fn({
              yourData: 'yolo'
            })
          }
        }
      },
      Download
    ]
  }));

  it('should log ngOnInit', inject([Download], (download) => {
    spyOn(console, 'log');
    expect(console.log).not.toHaveBeenCalled();

    download.ngOnInit();
    expect(console.log).toHaveBeenCalled();
  }));

});

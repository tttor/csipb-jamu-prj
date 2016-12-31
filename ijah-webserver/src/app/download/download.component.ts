import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Http } from '@angular/http';

declare var saveAs: any;

@Component({
  selector: 'download',
  styles: [`
  `],
  templateUrl: './download.template.html'
})
export class Download {
  localState;
  constructor(public route: ActivatedRoute, private http: Http) {

  }

  ngOnInit() {


  }
  asyncDataWithWebpack() {

  }

  downloadList(type,fname) {
    console.log('downloadList')

    // Query Data from DB
    this.http.get('http://ijah.apps.cs.ipb.ac.id/ijah/plant.php')
      .map(res => res.json())
      .subscribe(data => {
        let list: string[] = [];
        for (let i = 0; i < data.length; i++) {
          list.push(data[i]['pla_name']);
        }

        // Download
        let str = list.join("\n");
        let blob = new Blob([str], {type: "text/plain;charset=utf-8"});
        saveAs(blob, 'ijah_plantList.txt');
      })
  }

}

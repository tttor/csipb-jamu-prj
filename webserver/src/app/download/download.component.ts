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

    if(type == 1){
      this.http.get('http://ijah.apps.cs.ipb.ac.id/ijah/plant.php')
        .map(res => res.json())
        .subscribe(data => {
          let list: string[] = [];
          for (let i = 0; i < data.length; i++) {
            list.push(data[i]['pla_id']+','+data[i]['pla_name']);
          }

          let str = list.join("\n");
          let blob = new Blob([str], {type: "text/plain;charset=utf-8"});
          saveAs(blob, fname);
        })
    } else{
        if(type == 2){
        this.http.get('http://ijah.apps.cs.ipb.ac.id/ijah/compound.php')
          .map(res => res.json())
          .subscribe(data => {
            let list: string[] = [];
            for (let i = 0; i < data.length; i++) {
              list.push(data[i]['com_id']+','+data[i]['com_drugbank_id']+','+data[i]['com_knapsack_id']+','+data[i]['com_kegg_id']+','+data[i]['com_pubchem_id']+','+data[i]['com_cas_id']+','+data[i]['com_inchikey']+','+data[i]['com_smiles']);
            }

            let str = list.join("\n");
            let blob = new Blob([str], {type: "text/plain;charset=utf-8"});
            saveAs(blob, fname);
          })
      } else{
          if(type == 3){
          this.http.get('http://ijah.apps.cs.ipb.ac.id/ijah/protein.php')
            .map(res => res.json())
            .subscribe(data => {
              let list: string[] = [];
              for (let i = 0; i < data.length; i++) {
                list.push(data[i]['pro_id']+','+data[i]['pro_name']+','+data[i]['pro_uniprot_id']+','+data[i]['pro_uniprot_abbrev']);
              }

              let str = list.join("\n");
              let blob = new Blob([str], {type: "text/plain;charset=utf-8"});
              saveAs(blob, fname);
            })
        } else{
            if(type == 4){
            this.http.get('http://ijah.apps.cs.ipb.ac.id/ijah/disease.php')
              .map(res => res.json())
              .subscribe(data => {
                let list: string[] = [];
                for (let i = 0; i < data.length; i++) {
                  list.push(data[i]['dis_id']+','+data[i]['dis_omim_id']+','+data[i]['dis_name']+','+data[i]['dis_uniprot_abbrv']);
                }

                let str = list.join("\n");
                let blob = new Blob([str], {type: "text/plain;charset=utf-8"});
                saveAs(blob, fname);
              })
          } else{
              if(type == 5){
              this.http.get('http://localhost/ijah/query_pla_com.php')
                .map(res => res.json())
                .subscribe(data => {
                  let list: string[] = [];
                  for (let i = 0; i < data.length; i++) {
                    list.push(data[i]['pla_id']+','+data[i]['com_id']+','+data[i]['source']+','+data[i]['weight']+','+data[i]['time_stamp']);
                  }

                  let str = list.join("\n");
                  let blob = new Blob([str], {type: "text/plain;charset=utf-8"});
                  saveAs(blob, fname);
                })
            } else{
                if(type == 6){
                this.http.get('http://localhost/ijah/query_com_pro.php')
                  .map(res => res.json())
                  .subscribe(data => {
                    let list: string[] = [];
                    for (let i = 0; i < data.length; i++) {
                      list.push(data[i]['com_id']+','+data[i]['pro_id']+','+data[i]['source']+','+data[i]['weight']+','+data[i]['time_stamp']);
                    }

                    let str = list.join("\n");
                    let blob = new Blob([str], {type: "text/plain;charset=utf-8"});
                    saveAs(blob, fname);
                  })
              } else{
                  if(type == 7){
                  this.http.get('http://localhost/ijah/query_pro_dis.php')
                    .map(res => res.json())
                    .subscribe(data => {
                      let list: string[] = [];
                      for (let i = 0; i < data.length; i++) {
                        list.push(data[i]['pro_id']+','+data[i]['dis_id']+','+data[i]['source']+','+data[i]['weight']+','+data[i]['time_stamp']);
                      }

                      let str = list.join("\n");
                      let blob = new Blob([str], {type: "text/plain;charset=utf-8"});
                      saveAs(blob, fname);
                    })
                }
              }
            }
          }
        }
      }
    }
  }
}

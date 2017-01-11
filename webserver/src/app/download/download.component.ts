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

  downloadList(type, api_link, fname){
    this.http.get(api_link)
      .map(res => res.json())
      .subscribe(data => {
        let list: string[] = [];
        for (let i = 0; i < data.length; i++) {
          if(type == 1){
            list.push(data[i]['pla_id']+','+data[i]['pla_name']);
          } else{
            if(type == 2){
              list.push(data[i]['com_id']+','+data[i]['com_drugbank_id']+','+data[i]['com_knapsack_id']+','+data[i]['com_kegg_id']+','+data[i]['com_pubchem_id']+','+data[i]['com_cas_id']+','+data[i]['com_inchikey']+','+data[i]['com_smiles']);
          } else{
            if(type == 3){
              list.push(data[i]['pro_id']+','+data[i]['pro_name']+','+data[i]['pro_uniprot_id']+','+data[i]['pro_uniprot_abbrev']);
            } else{
              if(type == 4){
                list.push(data[i]['dis_id']+','+data[i]['dis_omim_id']+','+data[i]['dis_name']+','+data[i]['dis_uniprot_abbrv']);
              } else{
                if(type == 5){
                  list.push(data[i]['pla_id']+','+data[i]['com_id']+','+data[i]['source']+','+data[i]['weight']+','+data[i]['time_stamp']);
                } else{
                  if(type == 6){
                    list.push(data[i]['com_id']+','+data[i]['pro_id']+','+data[i]['source']+','+data[i]['weight']+','+data[i]['time_stamp']);
                  } else{
                    if(type == 7){
                      list.push(data[i]['pro_id']+','+data[i]['dis_id']+','+data[i]['source']+','+data[i]['weight']+','+data[i]['time_stamp']);
                    }
                  }
                }
              }
            }
          }
        }
      }
        let str = list.join("\n");
        let blob = new Blob([str], {type: "text/plain;charset=utf-8"});
        saveAs(blob, fname);
      })
  }
}

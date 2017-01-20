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
  baseAPI;
  interactionQueryAPI;
  metaQueryAPI;
  localState;
  constructor(public route: ActivatedRoute, private http: Http) {

  }

  ngOnInit() {


  }
  asyncDataWithWebpack() {

  }

  getProps(type){
    // This method actually duplicates the one in apps.home class
    // TODO merge them
    let props = [];
    if (type === 'pla') {
      props.push('pla_id');
      props.push('pla_name');
      props.push('pla_idr_name');
    }
    if (type === 'com') {
      props.push('com_id');
      props.push('com_cas_id');
      props.push('com_drugbank_id');
      props.push('com_knapsack_id');
      props.push('com_kegg_id');
      props.push('com_inchikey');
      props.push('com_pubchem_id');
      props.push('com_smiles');
    }
    if (type === 'pro') {
      props.push('pro_id');
      props.push('pro_name');
      props.push('pro_uniprot_id');
      props.push('pro_uniprot_abbrv');
    }
    if (type === 'dis') {
      props.push('dis_id');
      props.push('dis_omim_id');
      props.push('dis_name');
      props.push('dis_uniprot_abbrv');
    }
    if (type === 'pla_vs_com') {
      props.push('pla_id');
      props.push('com_id');
      props.push('weight');
      props.push('source');
      props.push('time_stamp');
    }
    if (type === 'com_vs_pro') {
      props.push('com_id');
      props.push('pro_id');
      props.push('weight');
      props.push('source');
      props.push('time_stamp');
    }
    if (type === 'pro_vs_dis') {
      props.push('pro_id');
      props.push('dis_id');
      props.push('weight');
      props.push('source');
      props.push('time_stamp');
    }
    return props;
  }

  getHeader(type) {
    let header = '';
    if (type === 'pla') {
      header = '[Plant ID,Latin Name,Indonesian Name]';
    }
    if (type === 'com') {
      header = '[Compound ID,CAS,Drugbank ID,Knapsack ID,Kegg ID,PubchemID,InChIKey,SMILES]';
    }
    if (type === 'pro') {
      header = '[Protein ID,Uniprot Name,Uniprot ID/Accession,Uniprot Abbreviation]';
    }
    if (type === 'dis') {
      header = '[Disease ID,OMIM ID,OMIM Name,Uniprot Abbreviation]';
    }
    if (type === 'pla_vs_com') {
      header = '[Plant ID,Compound ID,weight,source,timestamp]';
    }
    if (type === 'com_vs_pro') {
      header = '[Compound ID,Protein ID,weight,source,timestamp]';
    }
    if (type === 'pro_vs_dis') {
      header = '[Protein ID,Disease ID,weight,source,timestamp]';
    }
    return header;
  }

  getFilename(type) {
    let prefix = 'ijah_'
    let suffix = '';
    let ext = '.txt';
    let body = '';
    if (type === 'pla') {
      body = 'plant';
      suffix = '_metadata';
    }
    if (type === 'com') {
      body = 'compound';
      suffix = '_metadata';
    }
    if (type === 'pro') {
      body = 'protein';
      suffix = '_metadata';
    }
    if (type === 'dis') {
      body = 'disease';
      suffix = '_metadata';
    }
    if (type === 'pla_vs_com') {
      body = 'plant_vs_compound';
      suffix = '_connectivity';
    }
    if (type === 'com_vs_pro') {
      body = 'compound_vs_protein';
      suffix = '_connectivity';
    }
    if (type === 'pro_vs_dis') {
      body = 'protein_vs_disease';
      suffix = '_connectivity';
    }
    let filename = prefix+body+suffix+ext;
    return filename;
  }

  download(type) {
    this.baseAPI = 'http://ijah.apps.cs.ipb.ac.id/api/';
    // this.baseAPI ='http://localhost/';// Comment this if you run online!

    let api = this.baseAPI+'metadata.php';
    if (type.indexOf('_vs_') !== -1) {
      api = this.baseAPI+'connectivity.php';
    }

    let msg = '[{"id":"'+type.toUpperCase()+'_ALL_ROWS"}]';
    this.http.post(api,msg).map(res => res.json())
      .subscribe(data => {
        let txt = this.getHeader(type)+'\n';
        for (let i = 0; i < data.length; i++){
          let props = this.getProps(type);
          for (let j=0; j < props.length;j++) {
            txt += data[i][props[j]];
            if (j<props.length-1) {
              txt += ',';
            }
          }
          txt = txt + '\n';
        }
        let blob = new Blob([txt], {type: "text/plain;charset=utf-8"});
        saveAs(blob,this.getFilename(type));
      })
  }

  downloadList(type, api_link, fname){
    this.baseAPI = 'http://ijah.apps.cs.ipb.ac.id/api/';
    // this.baseAPI ='http://localhost/';// Comment this if you run online!
    this.interactionQueryAPI = this.baseAPI+'connectivity.php';
    this.metaQueryAPI = this.baseAPI+'metadata.php';

    // this.http.get(api_link)
    //   .map(res => res.json())
    let downloadPostMsg = [type+'_ALL_ROWS'];
    this.http.post(this.metaQueryAPI,downloadPostMsg).map(res => res.json())
      .subscribe(data => {
        let list: string[] = [];
        for (let i = 0; i < data.length; i++) {
          if(type == 1){
            list.push(data[i]['pla_id']+','+data[i]['pla_name']+','+data[i]['pla_idr_name']);
          } else{
            if(type == 2){
              list.push(data[i][type+'_id']+','+data[i]['com_drugbank_id']+','+data[i]['com_knapsack_id']+','+data[i]['com_kegg_id']+','+data[i]['com_pubchem_id']+','+data[i]['com_cas_id']+','+data[i]['com_inchikey']+','+data[i]['com_smiles']);
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
        saveAs(blob, 'ijah_'+fname+'_list.txt');
      })
  }
}

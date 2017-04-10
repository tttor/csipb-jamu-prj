import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Http } from '@angular/http';

declare var saveAs: any;

@Component({
  selector: 'download',
  styles: [`
  `],
  templateUrl: './download.component.html'
})
export class DownloadComponent implements OnInit {
  private baseAPI;
  constructor(public route: ActivatedRoute, private http: Http) {
    // this.baseAPI = 'http://ijah.apps.cs.ipb.ac.id/api/';
    // this.baseAPI = 'http://ijah.agri.web.id/api/';
    this.baseAPI ='http://localhost/ijah-api/';// Comment this if you run online!
  }

  public ngOnInit() {
    // do nothing
  }

  public asyncDataWithWebpack() {
    // do nothing
  }

  private getProps(type) {
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

  private getHeader(type) {
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

  private getFilename(type) {
    let prefix = 'ijah_all_';
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

    const dateTime = +new Date();
    const unixTS = Math.floor(dateTime / 1000);
    let date = new Date(unixTS * 1000);
    let y = date.getFullYear();
    let m = this.makeTwoDigitStr(date.getMonth() + 1);
    let d = this.makeTwoDigitStr(date.getDate());
    let hh = this.makeTwoDigitStr(date.getHours());
    let mm = this.makeTwoDigitStr(date.getMinutes());
    let ss = this.makeTwoDigitStr(date.getSeconds());
    let timestamp = '_' + y + m + d + '-' + hh + mm + ss;

    let filename = prefix + body + suffix + timestamp + ext;
    return filename;
  }

  private makeTwoDigitStr(str) {
    str = str.toString();
    if (str.length === 2) {
      return str;
    } else {
      return '0' + str;
    }
  }

  public download(type) {
    let api = this.baseAPI + 'metadata.php';
    if (type.indexOf('_vs_') !== -1) {
      api = this.baseAPI + 'connectivity.php';
    }

    let msg = '[{"id":"' + type.toUpperCase() + '_ALL_ROWS"}]';
    this.http.post(api, msg).map((res) => res.json())
      .subscribe((data) => {
        let txt = this.getHeader(type) + '\n';
        for (let i = 0; i < data.length; i++) { // tslint:disable-line
          let props = this.getProps(type);
          for (let j  = 0; j < props.length; j++) {
            txt += data[i][props[j]];
            if (j < props.length - 1) {
              txt += ',';
            }
          }
          txt = txt + '\n';
        }
        let blob = new Blob([txt], {type: 'text/plain;charset=utf-8'});
        saveAs(blob, this.getFilename(type));
      });
  }
}

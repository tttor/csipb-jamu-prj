import { Component } from '@angular/core';
import { AppState } from '../app.service';

import { FormControl, FormGroup } from '@angular/forms';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';

import { Http } from '@angular/http';

declare var saveAs: any;

@Component({
  selector: 'home',
  providers: [
  ],
  directives: [
  ],
  pipes: [ ],
  styleUrls: [ './home.style.css' ],
  templateUrl: './home.template.html'
})
export class Home {
  // count variable
  countTanaman = 0;
  countCompound = 0;
  countProtein = 0;
  countDisease = 0;

  // active variable
  activeTanaman = true;
  activeCompound = true;
  activeProtein = true;
  activeDisease = true;

  // Search data for auto completion, search while filling
  plantSearch: Array<string>;
  compoundSearch: Array<string>;
  proteinSearch: Array<string>;
  diseaseSearch: Array<string>;

  // Total number of items in each set
  plant_total;
  compound_total;
  protein_total;
  disease_total;

  // Items selected by users
  selectedPlants = [];
  selectedCompounds = [];
  selectedProteins = [];
  selectedDiseases = [];

  // This 3 vars are used in text output
  jsonPlantCompound;
  jsonCompoundProtein;
  jsonProteinDisease;

  // Misc.
  // TODO explain the usage
  show = false;
  dataLocal = [];
  FileSaver: any;
  click = false;
  baseAPI;
  interactionQueryAPI;
  metaQueryAPI;
  typeaheadNoResults:boolean = false;
  noResultPlant = false;
  noResultCompound = false;
  noResultProtein = false;
  noResultDisease = false;
  pTanaman = false;
  pProtein = false;
  pCompound = false;
  pDisease = false;
  data: any;
  plant: any;
  compound: any;
  protein: any;
  disease: any;

  //////////////////////////////////////////////////////////////////////////////
  ngOnInit() {

  }

  public stateCtrl:FormControl = new FormControl();

  public myForm:FormGroup = new FormGroup({
    state: this.stateCtrl
  });

  public typeaheadOnSelect(e:any):void {

  }

  public changeTypeaheadNoResults(e:boolean, id):void {
    this.typeaheadNoResults = e;

    if (id == 1) {
      this.noResultPlant = e;
    }

    else if (id == 2) {
      this.noResultCompound = e;
    }

    else if (id == 3) {
      this.noResultProtein = e;
    }

    else if (id == 4) {
      this.noResultDisease = e;
    }
  }

  constructor(public appState: AppState, private http: Http) {
    this.baseAPI = 'http://ijah.apps.cs.ipb.ac.id/ijah/';
    this.baseAPI ='http://localhost/';// Comment this if you run online!

    this.interactionQueryAPI = this.baseAPI+'query_interaction.php';
    this.metaQueryAPI = this.baseAPI+'query_metadata.php';

    this.plant = [{ 'index': this.countTanaman, 'value' : ''}];
    this.compound = [{ 'index': this.countCompound, 'value' : ''}];
    this.protein = [{ 'index': this.countProtein, 'value' : ''}];
    this.disease = [{ 'index': this.countDisease, 'value' : ''}];

    this.http.get(this.baseAPI+'total.php').map(res => res.json())
      .subscribe(data => {
        this.plant_total = data[0]['plant_total'];
        this.compound_total = data[0]['compound_total'];
        this.protein_total = data[0]['protein_total'];
        this.disease_total = data[0]['disease_total'];
      })

    // Query for metadata for _text_ _completion_ //////////////////////////////
    let plaPostMsg = ['PLA_ALL_ROWS'];
    let plaPostMsgJSON = this.makeJSONFormat(plaPostMsg,'id');
    this.http.post(this.metaQueryAPI,plaPostMsgJSON).map(res => res.json())
      .subscribe(data => {
        for (let i = 0; i < data.length; i++) {
          let temp = data[i]['pla_name'];
          data[i]['search'] = temp;
        }
        this.plantSearch = data;
      })

    let proPostMsg = ['PRO_ALL_ROWS'];
    let proPostMsgJSON = this.makeJSONFormat(proPostMsg,'id');
    this.http.post(this.metaQueryAPI,proPostMsgJSON).map(res => res.json())
      .subscribe(data => {
        for (let i = 0; i < data.length; i++) {
          let temp = data[i]['pro_uniprot_id']+' | '+data[i]['pro_name'];
          data[i]['search'] = temp;
        }
        this.proteinSearch = data;
      })

    let disPostMsg = ['DIS_ALL_ROWS'];
    let disPostMsgJSON = this.makeJSONFormat(disPostMsg,'id');
    this.http.post(this.metaQueryAPI,disPostMsgJSON).map(res => res.json())
      .subscribe(data => {
        for (let i = 0; i < data.length; i++) {
          let temp = data[i]['dis_omim_id']+' | '+data[i]['dis_name'];
          data[i]['search'] = temp;
        }
        this.diseaseSearch = data;
      })

    let comPostMsg = ['COM_ALL_ROWS'];
    let comPostMsgJSON = this.makeJSONFormat(comPostMsg,'id');
    this.http.post(this.metaQueryAPI,comPostMsgJSON).map(res => res.json())
      .subscribe(data => {
        for (let i = 0; i < data.length; i++) {
          let valid = [];
          if (data[i]['com_cas_id']) {
            valid.push(data[i]['com_cas_id']);
          }
          if (data[i]['com_drugbank_id']) {
            valid.push(data[i]['com_drugbank_id']);
          }
          if (data[i]['com_knapsack_id']) {
            valid.push(data[i]['com_knapsack_id']);
          }
          if (data[i]['com_kegg_id']) {
            valid.push(data[i]['com_kegg_id']);
          }

          let str = '';
          for (let j=0;j<valid.length;j++) {
            str = str + valid[j];
            if (j<valid.length-1) {
              str = str + ' | ';
            }
          }
          data[i]['search'] = str;
        }
        this.compoundSearch = data;
      })
  }

  // INPUT HANDLING METHODS ////////////////////////////////////////////////////
  selectPlant(e:any, index):void {
    if (index != this.countTanaman) {
      this.selectedPlants.push({ 'index': this.countTanaman, 'value' : e.item.pla_id});
    }
  }

  selectCompound(e:any, index):void {
    if (index != this.countCompound) {
      this.selectedCompounds.push({ 'index': this.countCompound, 'value' : e.item.com_id});
    }
  }

  selectProtein(e:any, index):void {
    if (index != this.countProtein) {
      this.selectedProteins.push({ 'index': this.countProtein, 'value' : e.item.pro_id});
    }
  }

  selectDisease(e:any, index):void {
    if (index != this.countDisease) {
      this.selectedDiseases.push({ 'index': this.countDisease, 'value' : e.item.dis_id});
    }
  }

  focusPlant(index: number) {
    this.activeCompound = false;
    if (index == this.countTanaman) {
      this.countTanaman++;
      this.plant.push({ 'index': this.countTanaman, 'value' : ''});
    }
  }

  focusCompound(index: number) {
    this.activeTanaman = false;
    if (index == this.countCompound) {
      this.countCompound++;
      this.compound.push({ 'index': this.countCompound, 'value' : ''});
    }
  }

  focusProtein(index: number) {
    this.activeDisease = false;
    if (index == this.countProtein) {
      this.countProtein++;
      this.protein.push({ 'index': this.countProtein, 'value' : ''});
    }
  }

  focusDisease(index: number) {
    this.activeProtein = false;
    if (index == this.countDisease) {
      this.countDisease++;
      this.disease.push({ 'index': this.countDisease, 'value' : ''});
    }
  }

  // SEARCH+PREDICT METHODS ////////////////////////////////////////////////////
  searchAndPredictButtonCallback() {
    this.click = true;

    let showPlant = false;
    let showCompound = false;
    let showProtein = false;
    let showDisease = false;

    if (this.plant.length > 1 && this.disease.length <= 1 && this.protein.length <= 1) {
      this.searchFromDrugSide(this.selectedPlants);
      showPlant = true;
    }
    else if (this.compound.length > 1 && this.protein.length <= 1 && this.disease.length <= 1) {
      this.searchFromDrugSide(this.selectedCompounds);
      showCompound = true;
    }

    else if (this.protein.length > 1 && this.plant.length <= 1 && this.compound.length <= 1) {
      this.searchFromTargetSide(this.selectedProteins);
      showProtein = true;
    }
    else if (this.disease.length > 1 && this.plant.length <= 1 && this.compound.length <= 1) {
      this.searchFromTargetSide(this.selectedDiseases);
      showDisease = true;
    }
    // Use case 1: both sides are specified ////////////////////////////////////
    else if (this.plant.length > 1 && this.protein.length > 1) {
        this.searchAndPredict(this.selectedPlants,this.selectedProteins);
    }
    else if (this.plant.length > 1 && this.disease.length > 1) {
        this.searchAndPredict(this.selectedPlants,this.selectedDiseases)
    }
    else if (this.compound.length > 1 && this.protein.length > 1) {
        this.searchAndPredict(this.selectedCompounds,this.selectedProteins);
    }
    else if (this.compound.length > 1 && this.disease.length > 1) {
        this.searchAndPredict(this.selectedCompounds,this.selectedDiseases);
    }

    ////////////////////////////////////////////////////////////////////////////
    var inter = setInterval(() => {
      if (showPlant && !showProtein && !showDisease) {
        if (this.pTanaman) {
          localStorage.setItem('data', JSON.stringify(this.dataLocal));
          this.show = true;
          this.click = false;
          clearInterval(inter);
        }
      }
      else if (showCompound && !showProtein && !showDisease) {
        if(this.pCompound) {
          localStorage.setItem('data', JSON.stringify(this.dataLocal));
          this.show = true;
          this.click = false;
          clearInterval(inter);
        }
      }
      else if (showProtein && !showPlant && !showCompound) {
        if (this.pProtein) {
          localStorage.setItem('data', JSON.stringify(this.dataLocal));
          this.show = true;
          this.click = false;
          clearInterval(inter);
        }
      }
      else if (showDisease && !showPlant && !showCompound) {
        if (this.pDisease) {
          localStorage.setItem('data', JSON.stringify(this.dataLocal));
          this.show = true;
          this.click = false;
          clearInterval(inter);
        }
      }
      if (this.show) this.click = false;
    }, 100);
  }

  searchFromDrugSide(drugSideInput) {
    console.log('searchOnly: drugSideInput');

    let dsi = JSON.stringify(drugSideInput);
    // console.log(dsi);

    this.http.post(this.interactionQueryAPI,dsi).map(resp => resp.json())
    .subscribe(plaVScom => {
      let comSet = this.getSet(plaVScom,'com_id');
      let comSetJSON = this.makeJSONFormat(comSet,'comId');
      // console.log(comSetJSON);

      this.http.post(this.interactionQueryAPI,comSetJSON).map(resp2 => resp2.json())
      .subscribe(comVSpro => {
        let proSet = this.getSet(comVSpro,'pro_id');
        let proSetJSON = this.makeJSONFormat(proSet,'value');
        // console.log(proSetJSON);

        this.http.post(this.interactionQueryAPI,proSetJSON).map(resp3 => resp3.json())
        .subscribe(proVSdis => {
          let plaSet = this.getSet(plaVScom,'pla_id');
          let disSet = this.getSet(proVSdis,'dis_id');

          this.makeOutput(plaSet,comSet,proSet,disSet,
                          plaVScom,comVSpro,proVSdis);
        })
      })
    })
  }

  searchFromTargetSide(targetSideInput) {
    console.log('searchOnly: targetSideInput');

    let tsi = JSON.stringify(targetSideInput);
    // console.log(tsi);

    this.http.post(this.interactionQueryAPI,tsi).map(resp => resp.json())
    .subscribe(proVSdis => {
      let proSet = this.getSet(proVSdis,'pro_id');
      let proSetJSON = this.makeJSONFormat(proSet,'proId');
      // console.log(proSetJSON);

      this.http.post(this.interactionQueryAPI,proSetJSON).map(resp2 => resp2.json())
      .subscribe(comVSpro => {
        let comSet = this.getSet(comVSpro,'com_id');
        let comSetJSON = this.makeJSONFormat(comSet,'value');
        // console.log(comSetJSON);

        this.http.post(this.interactionQueryAPI,comSetJSON).map(resp3 => resp3.json())
        .subscribe(plaVScom => {
          let plaSet = this.getSet(plaVScom,'pla_id');
          let disSet = this.getSet(proVSdis,'dis_id');

          this.makeOutput(plaSet,comSet,proSet,disSet,
                          plaVScom,comVSpro,proVSdis);
        })
      })
    })
  }

  searchAndPredict(drugSideInput,targetSideInput) {
    console.log('searchAndPredict');

    let dsi = JSON.stringify(drugSideInput);
    let tsi = JSON.stringify(targetSideInput);
    // console.log(dsi);
    // console.log(tsi);

    this.http.post(this.interactionQueryAPI,dsi).map(resp => resp.json())
    .subscribe(plaVScom => {
      this.http.post(this.interactionQueryAPI,tsi).map(resp2 => resp2.json())
      .subscribe(proVSdis => {
        let comVSproList = [];

        for (let i=0;i<plaVScom.length;i++) {
          for (let j=0;j<proVSdis.length;j++) {
            let comId = '"'+plaVScom[i]['com_id']+'"';
            let proId = '"'+proVSdis[j]['pro_id']+'"';
            let comVSpro = '{'+'"comId":'+comId+','+'"proId":'+proId+'}';
            comVSproList.push(comVSpro);
          }
        }

        // make unique
        comVSproList = comVSproList.filter((v, i, a) => a.indexOf(v) === i);

        // make it JSON-format
        let comVSproStr = '';
        for (let k=0;k<comVSproList.length;k++) {
          comVSproStr = comVSproStr+comVSproList[k];
          if (k<comVSproList.length-1) {
            comVSproStr = comVSproStr + ',';
          }
        }
        comVSproStr = '['+comVSproStr+']';
        // console.log(comVSproStr);

        this.http.post(this.interactionQueryAPI,comVSproStr).map(resp3 => resp3.json())
        .subscribe(comVSpro => {
          // Get unique items
          let plaSet = this.getSet(plaVScom,'pla_id');
          let comSet = this.getSet(plaVScom,'com_id');
          let proSet = this.getSet(proVSdis,'pro_id');
          let disSet = this.getSet(proVSdis,'dis_id');
          // let comSet2 = this.getSet(comVSpro,'com_id');
          // let proSet2 = this.getSet(comVSpro,'pro_id');

          this.makeOutput(plaSet,comSet,proSet,disSet,
                          plaVScom,comVSpro,proVSdis);
        })
      })
    })
  }

  // UTILITY METHODS ///////////////////////////////////////////////////////////
  makeOutput(plaSet,comSet,proSet,disSet,plaVScom,comVSpro,proVSdis) {
    plaSet = this.handleIfEmptySet(plaSet,'pla');
    comSet = this.handleIfEmptySet(comSet,'com');
    proSet = this.handleIfEmptySet(proSet,'pro');
    disSet = this.handleIfEmptySet(disSet,'dis');

    // Get metadata of each unique item
    let plaMetaPost = this.makeJSONFormat(plaSet,'id');
    let comMetaPost = this.makeJSONFormat(comSet,'id');
    let proMetaPost = this.makeJSONFormat(proSet,'id');
    let disMetaPost = this.makeJSONFormat(disSet,'id');

    // console.log('getting meta ...');
    this.http.post(this.metaQueryAPI,plaMetaPost).map(resp4 => resp4.json())
    .subscribe(plaMeta => {
      this.http.post(this.metaQueryAPI,comMetaPost).map(resp5=>resp5.json())
      .subscribe(comMeta => {
        this.http.post(this.metaQueryAPI,proMetaPost).map(resp6=>resp6.json())
        .subscribe(proMeta => {
          this.http.post(this.metaQueryAPI,disMetaPost).map(resp7=>resp7.json())
          .subscribe(disMeta => {
            // text output with detail metadata //////////////////////////
            this.jsonPlantCompound = this.makeTextOutput(plaVScom,
                                                         plaMeta,comMeta,
                                                         'pla','com');
            this.jsonCompoundProtein = this.makeTextOutput(comVSpro,
                                                           comMeta,proMeta,
                                                           'com','pro');
            this.jsonProteinDisease = this.makeTextOutput(proVSdis,
                                                         proMeta,disMeta,
                                                         'pro','dis');

            // graph output data prep ////////////////////////////////////
            let graphData = [];
            let nNodeMax = 20;

            let plaForGraph = this.getItemForGraph(plaSet,nNodeMax);
            let comForGraph = this.getItemForGraph(comSet,nNodeMax);
            let proForGraph = this.getItemForGraph(proSet,nNodeMax);
            let disForGraph = this.getItemForGraph(disSet,nNodeMax);

            let graphDataArr = [this.getGraphData(plaVScom,
                                                  plaMeta,comMeta,
                                                  'pla','com',
                                                  plaForGraph,comForGraph),
                                this.getGraphData(comVSpro,
                                                  comMeta,proMeta,
                                                  'com','pro',
                                                  comForGraph,proForGraph),
                                this.getGraphData(proVSdis,
                                                  proMeta,disMeta,
                                                   'pro','dis',
                                                   proForGraph,disForGraph)];

            for (let ii=0;ii<graphDataArr.length;ii++) {
              for(let jj=0;jj<graphDataArr[ii].length;jj++) {
                  let datum = graphDataArr[ii][jj];
                  graphData.push(datum);
              }
            }

            localStorage.setItem('data', JSON.stringify(graphData));
            this.show = true;
          })//disMeta
        })//proMeta
      })//comMeta
    })//plaMeta
  }

  makeJSONFormat(arr,key) {
    let str = '';
    for (let j=0;j<arr.length;j++){
      str = str+'{'+'"'+key+'"'+':'+'"'+arr[j]+'"'+'}';
      if (j<arr.length-1) {
        str = str+','
      }
    }
    str = '['+str+']';
    return str;
  }

  handleIfEmptySet(set,type) {
    if (set.length>0) {
      return set;
    }
    let newSet = [type.toUpperCase()+'NONE_DUMMY'];
    return newSet;
  }

  getItemForGraph(set,max) {
    let itemForGraph = [];
    for (let kk=0;kk<set.length;kk++) {
      if (kk < max) {
        itemForGraph.push(set[kk]);
      }
      else {
        break;
      }
    }
    return itemForGraph;
  }

  getSet(interaction,id) {
    let set = [];
    for (let i=0;i<interaction.length;i++) {
      let item = interaction[i][id];
      if (set.indexOf(item) === -1) {
        set.push(item);
      }
    }
    return set;
  }

  getPropKeys(type) {
    let keys: string[] = [];
    if (type==='pla') {
      keys.push('pla_name');
    }
    if (type==='com') {
      keys.push('com_cas_id');
      keys.push('com_drugbank_id');
      keys.push('com_kegg_id');
      keys.push('com_knapsack_id');
    }
    if (type==='pro') {
      keys.push('pro_uniprot_id');
      keys.push('pro_uniprot_abbrv');
      keys.push('pro_name');
    }
    if (type==='dis') {
      keys.push('dis_omim_id');
      keys.push('dis_name');
    }
    return keys;
  }

  getHyperlinkStr(type,seed) {
    let baseUrl: string = 'null';

    if (type==='com_knapsack_id') {
      baseUrl = 'http://kanaya.naist.jp/knapsack_jsp/information.jsp?sname=C_ID&word=';
    }
    if (type==='com_drugbank_id') {
      baseUrl = 'https://www.drugbank.ca/drugs/';
    }
    if (type==='com_kegg_id') {
      baseUrl = 'http://www.genome.jp/dbget-bin/www_bget?cpd:';
    }

    if (type==='pro_uniprot_id') {
      baseUrl = 'http://www.uniprot.org/uniprot/';
    }

    if (type==='dis_omim_id') {
      baseUrl = 'https://www.omim.org/entry/';
    }

    let urlStr:string = seed;
    if (seed!=='' && seed!=='null') {
      let url: string = baseUrl + seed;
      urlStr = '<a href="'+url+'" target="_blank">'+seed+'</a>';
    }
    if (urlStr.indexOf('null') !==-1 ) {
      urlStr = seed;
    }
    return urlStr;
  }

  getProps(id,keys,meta) {
    let prefix = id.substr(0,3);
    prefix = prefix.toLowerCase() + '_id';

    let idx = -1;
    for (let i=0;i<meta.length;i++) {
      if (id===meta[i][prefix]) {
        idx = i;
        break;
      }
    }

    let props = []
    for(let j=0;j<keys.length;j++) {
      props.push( meta[idx][keys[j]] );
    }

    return props;
  }

  getHeader(type) {
    let header = 'DEFAULT_HEADER';
    if (type === 'com') {
      header = 'CAS,DrugbankID,KnapsackID,KeggID,weight,source';
    }
    if (type === 'pro') {
      header = 'UniprotID,UniprotAbbrv,UniprotName,weight,source';
    }
    if (type === 'dis') {
      header = 'OmimID,OmimName,weight,source';
    }
    return header;
  }

  concatProps(props) {
    let str = '';
    for (let j=0;j<props.length;j++) {
      let prop = props[j];
      if (prop) {
        str = str+prop;
        if (j<props.length-1) {
          str = str + ',';
        }
      }
    }
    return str;
  }

  getGraphData(interaction,srcMeta,destMeta,srcType,destType,srcItems,destItems) {
    let srcProp = [];
    let destProp = [];

    let srcPropKeys = this.getPropKeys(srcType);
    let destPropKeys = this.getPropKeys(destType);

    let data = [];

    let i=0;
    for(i;i<interaction.length;i++) {
      let datum = [];

      let srcKey = srcType+'_id';
      let destKey = destType+'_id';

      let src = interaction[i][srcKey];
      let dest = interaction[i][destKey];

      if ((srcItems.indexOf(src)!==-1)&&(destItems.indexOf(dest)!==-1)) {
        let source = interaction[i]['source'];
        let weight = parseFloat( interaction[i]['weight'] );

        let srcProps = this.getProps(src,srcPropKeys,srcMeta);
        let destProps = this.getProps(dest,destPropKeys,destMeta);
        let srcText = this.concatProps(srcProps);
        let destText = this.concatProps(destProps);

        datum.push(srcText);
        datum.push(destText);
        datum.push(weight);

        data.push(datum);
      }
    }
    return data;
  }

  makeTextOutput(interaction,srcMeta,destMeta,srcType,destType) {
    let text: string = '';

    let srcProp = [];
    let destProp = [];

    let srcPropKeys = this.getPropKeys(srcType);
    let destPropKeys = this.getPropKeys(destType);

    let i: number = 0;
    let ii: number = 0;// # of unique plants
    let prevSrc = '';
    for(i;i<interaction.length;i++) {
      let srcKey = srcType+'_id';
      let destKey = destType+'_id'
      let src = interaction[i][srcKey];
      let dest = interaction[i][destKey];
      let source = interaction[i]['source'];
      let weight = interaction[i]['weight'];

      if (prevSrc!=src) {
        ii = ii + 1;
        text = text+'#'+ii.toString()+' ';

        let srcProps = this.getProps(src,srcPropKeys,srcMeta);

        let j=0;
        for (j;j<srcProps.length;j++) {
          text = text+this.getHyperlinkStr( srcPropKeys[j],srcProps[j] );
          if (j<srcProps.length-1) {
            text = text + ',';
          }
        }
        text = text+':\n';
        text = text+'  '+this.getHeader(destType)+'\n';

        prevSrc = src;
      }

      let destProps = this.getProps(dest,destPropKeys,destMeta);
      let jj=0;
      text = text+'  ';
      for (jj;jj<destProps.length;jj++) {
        text = text+this.getHyperlinkStr( destPropKeys[jj],destProps[jj] );
        if (jj<destProps.length-1) {
          text = text + ',';
        }
      }
      text = text+','+weight+','+source;
      text = text+'\n';
    }

    if (text==='') {
      text = 'None';
    }
    return text;
  }

  downloadJSON(idata,ifname){
    var json = localStorage.getItem(idata);
    var blob = new Blob([json], {type: "text/plain;charset=utf-8"});
    saveAs(blob, ifname);
  }

  check(data, input1, input2) {

    for(var i = 0; i < data.length; i++) {
      if (data[i][0] == input1 && data[i][1] == input2) {
        return false;
      }
    }

    return true;
  }

  checkJson(data, input1) {

    for(var i = 0; i < data.length; i++) {
      if (data[i] == input1) {
        return false;
      }
    }

    return true;
  }

  getMaxKeys(json) {
    var m;
    for (var i in json) {
        if (json.hasOwnProperty(i)) {
           m = (typeof m == 'undefined' || i > m) ? i : m;
        }
    }
    return m;
  }

  reset() {
    this.activeTanaman = true;
    this.activeCompound = true;
    this.activeProtein = true;
    this.activeDisease = true;

    this.pTanaman = false;
    this.pCompound = false;
    this.pProtein = false;
    this.pDisease = false;

    this.plant = [{ 'index': this.countTanaman, 'value' : ''}];
    this.compound = [{ 'index': this.countCompound, 'value' : ''}];
    this.protein = [{ 'index': this.countProtein, 'value' : ''}];
    this.disease = [{ 'index': this.countDisease, 'value' : ''}];

    this.selectedPlants = [];
    this.selectedCompounds = [];
    this.selectedProteins = [];
    this.selectedDiseases = [];

    this.show = false;
    localStorage.clear();
    this.dataLocal = [];

    this.typeaheadNoResults = false;

    this.noResultPlant = false;
    this.noResultCompound = false;
    this.noResultProtein = false;
    this.noResultDisease = false;
  }

  // EXAMPLE-BUTTON METHODS ////////////////////////////////////////////////////
  example1() {
  this.reset();
  this.plant = [{ 'index': 1, 'value' : 'Datura stramonium'}, { 'index': 2, 'value' : 'Trifolium pratense'}, { 'index': 3, 'value' : 'Acacia senegal'}, { 'index': 4, 'value' : ''}];
  this.selectedPlants = [{"index":1,"value":"PLA00002565"},{"index":2,"value":"PLA00001090"},{"index":3,"value":"PLA00000325"}];

  this.countTanaman = 4;
  this.activeCompound = false;
  this.activeProtein = false;
  this.activeDisease = false;
  }

  example2() {
  this.reset();
  this.compound = [{ 'index': 1, 'value' : '117-39-5 | DB04216 | C00004631 | 5280343'}, { 'index': 2, 'value' : '61-50-7 | DB01488 | C00001407 | 6089'}, { 'index': 3, 'value' : '51-55-8 | DB00572 | C00002277 | 174174'}, { 'index': 4, 'value' : ''}];
  this.selectedCompounds = [{ 'index': 1, 'value' : 'COM00000058'}, { 'index': 2, 'value' : 'COM00000014'}, { 'index': 3, 'value' : 'COM00000039'}];

  this.countCompound = 2;
  this.activeDisease = false;
  this.activeTanaman = false;
  this.activeProtein = false;
  }

  example3() {
  this.reset();
  this.protein = [{ 'index': 1, 'value' : 'P07437 | Tubulin beta chain'}, { 'index': 2, 'value' : 'P02768 | Serum albumin'}, { 'index': 3, 'value' : ''}];
  this.selectedProteins = [{ 'index': 1, 'value' : 'PRO00002823'}, { 'index': 2, 'value' : 'PRO00001554'}];

  this.countProtein = 3;
  this.activeDisease = false;
  this.activeTanaman = false;
  this.activeCompound = false;
  }

  example4() {
  this.reset();
  this.disease = [{ 'index': 1, 'value' : '156610 | Skin creases, congenital symmetric circumferential, 1'}, { 'index': 2, 'value' : '614373 | Amyotrophic lateral sclerosis 16, juvenile'}, { 'index': 3, 'value' : '612244 | Inflammatory bowel disease 13'}, { 'index': 4, 'value' : ''}];
  this.selectedDiseases = [{ 'index': 1, 'value' : 'DIS00001455'}, { 'index': 2, 'value' : 'DIS00000803'}, { 'index': 3, 'value' : 'DIS00003796'}];

  this.countDisease = 4;
  this.activeProtein = false;
  this.activeTanaman = false;
  this.activeCompound = false;
  }

  example5() {
  this.reset();
  this.plant = [{ 'index': 1, 'value' : 'Catharanthus roseus'}, { 'index': 2, 'value' : 'Nigella sativa'}, { 'index': 3, 'value' : 'Cocos nucifera'}, { 'index': 4, 'value' : ''}];
  this.selectedPlants = [{"index":1,"value":"PLA00001025"},{"index":2,"value":"PLA00003511"},{"index":3,"value":"PLA00001600"}];
  this.countTanaman = 4;

  this.protein = [{ 'index': 1, 'value' : 'P07437 | Tubulin beta chain'}, { 'index': 2, 'value' : 'P02768 | Serum albumin'}, { 'index': 3, 'value' : ''}];
  this.selectedProteins = [{ 'index': 1, 'value' : 'PRO00002823'}, { 'index': 2, 'value' : 'PRO00001554'}];

  this.countProtein = 3;

  this.activeDisease = false;
  this.activeCompound = false;
  }

  example6() {
  this.reset();
  this.compound = [{ 'index': 1, 'value' : '51-55-8 | DB00572 | C00002277 | 174174'}, { 'index': 2, 'value' : '51-34-3 | DB00747 | C00002292 | C01851'}, { 'index': 3, 'value' : '53-86-1 | DB00328 | C00030512 | C01926'}, { 'index': 4, 'value' : ''}];
  this.selectedCompounds = [{ 'index': 1, 'value' : 'COM00000039'}, { 'index': 2, 'value' : 'COM00001628'}, { 'index': 3, 'value' : 'COM00005599'}];

  this.countCompound = 2;

  this.disease = [{ 'index': 1, 'value' : '608516 | Major depressive disorder'}, { 'index': 2, 'value' : '100100 | Prune belly syndrome'}, { 'index': 3, 'value' : '614473 | Arterial calcification of infancy, generalized, 2'}, { 'index': 4, 'value' : ''}];
  this.selectedDiseases = [{ 'index': 1, 'value' : 'DIS00000849'}, { 'index': 2, 'value' : 'DIS00003796'}, { 'index': 3, 'value' : 'DIS00000853'}];

  this.countDisease = 4;

  this.activeTanaman = false;
  this.activeProtein = false;
  }

  example7() {
  this.reset();
  this.plant = [{ 'index': 1, 'value' : 'Aloe vera'}, { 'index': 2, 'value' : 'Cocos nucifera'}, { 'index': 3, 'value' : 'Panax ginseng'}, { 'index': 4, 'value' : ''}];
  this.selectedPlants = [{"index":1,"value":"PLA00001504"},{"index":2,"value":"PLA00001600"},{"index":3,"value":"PLA00003447"}];
  this.countDisease = 4;

  this.disease = [{ 'index': 1, 'value' : '61600 | Analbuminemia'}, { 'index': 2, 'value' : '615999 | Hyperthyroxinemia, familial dysalbuminemic'}, { 'index': 3, 'value' : ''}];
  this.selectedDiseases = [{ 'index': 1, 'value' : 'DIS00003787'}, { 'index': 2, 'value' : 'DIS00003675'}];

  this.countDisease = 3;

  this.activeCompound = false;
  this.activeProtein = false;
  }

  example8() {
  this.reset();
  this.compound = [{ 'index': 1, 'value' : '51-55-8 | DB00572 | C00002277 | 174174'}, { 'index': 2, 'value' : '61-50-7 | DB01488 | C00001407 | 6089'}, { 'index': 3, 'value' : '117-39-5 | DB04216 | C00004631 | 5280343'}, { 'index': 4, 'value' : ''}];
  this.selectedCompounds = [{ 'index': 1, 'value' : 'COM00000039'}, { 'index': 2, 'value' : 'COM00000014'}, { 'index': 3, 'value' : 'COM00000058'}];

  this.countCompound = 2;

  this.protein = [{ 'index': 1, 'value' : 'P53985 | Monocarboxylate transporter 1'}, { 'index': 2, 'value' : 'P20309 | Muscarinic acetylcholine receptor M3'}, { 'index': 3, 'value' : 'Q99720 | Sigma non-opioid intracellular receptor 1'}, { 'index': 4, 'value' : ''}];
  this.selectedProteins = [{ 'index': 1, 'value' : 'PRO00000040'}, { 'index': 2, 'value' : 'PRO00000452'}, { 'index': 3, 'value' : 'PRO00000377'}];

  this.countProtein = 4;

  this.activeTanaman = false;
  this.activeDisease = false;
  }
}

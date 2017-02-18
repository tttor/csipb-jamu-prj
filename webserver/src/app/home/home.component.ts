import {
  Component, OnInit, Inject, ElementRef, ViewChild
} from '@angular/core';

import { FormControl, FormGroup } from '@angular/forms';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/of';

import { Http } from '@angular/http';

declare var saveAs: any;

import { AppState } from '../app.service';

@Component({
  selector: 'home',
  providers: [],
  styleUrls: [ './home.component.css' ],
  templateUrl: './home.component.html'
})
export class Home implements OnInit {
  // count number of input rows
  nPlaInputHolders = 0;
  nComInputHolders = 0;
  nProInputHolders = 0;
  nDisInputHolders = 0;
  plaInputHolders = [];
  comInputHolders = [];
  proInputHolders = [];
  disInputHolders = [];

  // active variable
  activeTanaman = true;
  activeCompound = true;
  activeProtein = true;
  activeDisease = true;

  // Search data for auto completion, search while filling
  plantSearch = [];
  compoundSearch = [];
  proteinSearch = [];
  diseaseSearch = [];

  // Total number of items in each set
  nPlantInDB;
  nCompoundInDB;
  nProteinInDB;
  nDiseaseInDB;

  // Items selected by users
  selectedPlants = [];
  selectedCompounds = [];
  selectedProteins = [];
  selectedDiseases = [];

  // Used in connectivity text output
  plaVScomTxtOutput;
  comVSproTxtOutput;
  proVSdisTxtOutput;
  comVSplaTxtOutput;
  proVScomTxtOutput;
  disVSproTxtOutput;
  plaVScomSwapped = false;
  comVSproSwapped = false;
  proVSdisSwapped = false;

  // Used in metadata text output
  plaMetaTxtOutput;
  comMetaTxtOutput;
  proMetaTxtOutput;
  disMetaTxtOutput;

  // Used in summary text output
  summaryTxtOutput;
  summaryTxtOutput2;
  summaryTxtOutput3;

  // API URL addresses
  baseAPI;
  interactionQueryAPI;
  metaQueryAPI;
  predictAPI;

  // Misc.
  // TODO explain the usage
  show = false;// whether to show the output in home.page
  click = false;// whether searchAndPredictButton was clicked
  elapsedTime = 0;
  mode = 'unknown';
  inputType = 'unknown';

  comProConnExperimentSrcs = 'drugbank.ca';
  comProConnPredictionSrcs = 'blm-nii-svm';

  dataLocal = [];
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

  //////////////////////////////////////////////////////////////////////////////
  public ngOnInit() {
    // Do nothing
  }

  public stateCtrl:FormControl = new FormControl();

  public myForm:FormGroup = new FormGroup({
    state: this.stateCtrl
  });

  public typeaheadOnSelect(e:any):void {
    // Do nothing
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
    this.baseAPI = 'http://ijah.apps.cs.ipb.ac.id/api/';
    this.baseAPI ='http://localhost/ijah-api/';// Comment this if you run online!

    this.interactionQueryAPI = this.baseAPI+'connectivity.php';
    this.metaQueryAPI = this.baseAPI+'metadata.php';
    this.predictAPI = this.baseAPI+'predict.php';

    this.plaInputHolders = [{ 'index': this.nPlaInputHolders, 'value' : ''}];
    this.comInputHolders = [{ 'index': this.nComInputHolders, 'value' : ''}];
    this.proInputHolders = [{ 'index': this.nProInputHolders, 'value' : ''}];
    this.disInputHolders = [{ 'index': this.nDisInputHolders, 'value' : ''}];

    this.http.get(this.baseAPI+'total.php').map(res => res.json())
      .subscribe(data => {
        this.nPlantInDB = data[0]['plant_total'];
        this.nCompoundInDB = data[0]['compound_total'];
        this.nProteinInDB = data[0]['protein_total'];
        this.nDiseaseInDB = data[0]['disease_total'];
      })

    // Query for metadata for _text_ _completion_ //////////////////////////////
    let plaPostMsg = ['PLA_ALL_ROWS'];
    let plaPostMsgJSON = this.makeJSONFormat(plaPostMsg,'id');
    this.http.post(this.metaQueryAPI,plaPostMsgJSON).map(res => res.json())
      .subscribe(data => {
        for (let i = 0; i < data.length; i++) {
          let valid = [];
          if (data[i]['pla_name']) {
            valid.push(data[i]['pla_name']);
          }
          if (data[i]['pla_idr_name']) {
            valid.push(data[i]['pla_idr_name']);
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
            if (j < valid.length -1) {
              str = str + ' | ';
            }
          }
          data[i]['search'] = str;
        }
        this.compoundSearch = data;
      })
  }

  // INPUT HANDLING METHODS ////////////////////////////////////////////////////
  private selectPlant(e:any, index):void {
    if (index != this.nPlaInputHolders) {
      this.selectedPlants.push({ 'index': this.nPlaInputHolders, 'value' : e.item.pla_id});
    }
  }

  private selectCompound(e:any, index):void {
    if (index != this.nComInputHolders) {
      this.selectedCompounds.push({ 'index': this.nComInputHolders, 'value' : e.item.com_id});
    }
  }

  private selectProtein(e:any, index):void {
    if (index != this.nProInputHolders) {
      this.selectedProteins.push({ 'index': this.nProInputHolders, 'value' : e.item.pro_id});
    }
  }

  private selectDisease(e:any, index):void {
    if (index != this.nDisInputHolders) {
      this.selectedDiseases.push({ 'index': this.nDisInputHolders, 'value' : e.item.dis_id});
    }
  }

  private focusPlant(index: number) {
    let MAX_INPUT_PLANTS = 5;
    this.activeCompound = false;
    if (index == this.nPlaInputHolders) {
      if (this.nPlaInputHolders+1 < MAX_INPUT_PLANTS) {
        this.nPlaInputHolders++;
        this.plaInputHolders.push({ 'index': this.nPlaInputHolders, 'value' : ''});
      }
    }
  }

  private focusCompound(index: number) {
    let MAX_INPUT_COMPOUNDS = 5;
    this.activeTanaman = false;
    if (index == this.nComInputHolders) {
      if (this.nComInputHolders+1 < MAX_INPUT_COMPOUNDS) {
        this.nComInputHolders++;
        this.comInputHolders.push({ 'index': this.nComInputHolders, 'value' : ''});
      }
    }
  }

  private focusProtein(index: number) {
    let MAX_INPUT_PROTEINS = 5;
    this.activeDisease = false;
    if (index == this.nProInputHolders) {
      if (this.nProInputHolders+1 < MAX_INPUT_PROTEINS) {
        this.nProInputHolders++;
        this.proInputHolders.push({ 'index': this.nProInputHolders, 'value' : ''});
      }
    }
  }

  private focusDisease(index: number) {
    let MAX_INPUT_DISEASES = 5;
    this.activeProtein = false;
    if (index == this.nDisInputHolders) {
      if (this.nDisInputHolders+1 < MAX_INPUT_DISEASES) {
        this.nDisInputHolders++;
        this.disInputHolders.push({ 'index': this.nDisInputHolders, 'value' : ''});
      }
    }
  }

  // SEARCH+PREDICT METHODS ////////////////////////////////////////////////////
  private searchAndPredictButtonCallback() {
    if (this.selectedPlants.length==0 && this.selectedCompounds.length==0 &&
        this.selectedProteins.length==0 && this.selectedDiseases.length==0) {
      this.reset();
      return;
    }

    ////////////////////////////////////////////////////////////////////////////
    this.click = true;

    let showPlant = false;
    let showCompound = false;
    let showProtein = false;
    let showDisease = false;

    if (this.plaInputHolders.length > 1 && this.disInputHolders.length <= 1 && this.proInputHolders.length <= 1) {
      this.searchFromDrugSide(this.selectedPlants);
      this.mode = 'search_only';
      this.inputType = 'plant';
      showPlant = true;
    }
    else if (this.comInputHolders.length > 1 && this.proInputHolders.length <= 1 && this.disInputHolders.length <= 1) {
      this.searchFromDrugSide(this.selectedCompounds);
      this.mode = 'search_only';
      this.inputType = 'compound';
      showCompound = true;
    }

    else if (this.proInputHolders.length > 1 && this.plaInputHolders.length <= 1 && this.comInputHolders.length <= 1) {
      this.searchFromTargetSide(this.selectedProteins);
      this.mode = 'search_only';
      this.inputType = 'protein';
      showProtein = true;
    }
    else if (this.disInputHolders.length > 1 && this.plaInputHolders.length <= 1 && this.comInputHolders.length <= 1) {
      this.mode = 'search_only';
      this.inputType = 'disease';
      this.searchFromTargetSide(this.selectedDiseases);
      showDisease = true;
    }
    // Use case 1: both sides are specified ////////////////////////////////////
    else if (this.plaInputHolders.length > 1 && this.proInputHolders.length > 1) {
      this.mode = 'search_and_predict';
      this.inputType = 'plant+protein';
      this.searchAndPredict(this.selectedPlants,this.selectedProteins);
    }
    else if (this.plaInputHolders.length > 1 && this.disInputHolders.length > 1) {
      this.mode = 'search_and_predict';
      this.inputType = 'plant+disease';
      this.searchAndPredict(this.selectedPlants,this.selectedDiseases)
    }
    else if (this.comInputHolders.length > 1 && this.proInputHolders.length > 1) {
      this.mode = 'search_and_predict';
      this.inputType = 'compound+protein';
      this.searchAndPredict(this.selectedCompounds,this.selectedProteins);
    }
    else if (this.comInputHolders.length > 1 && this.disInputHolders.length > 1) {
      this.mode = 'search_and_predict';
      this.inputType = 'compound+disease';
      this.searchAndPredict(this.selectedCompounds,this.selectedDiseases);
    }

    ////////////////////////////////////////////////////////////////////////////
    let inter = setInterval(() => {
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
      if (this.show) {
        this.click = false;
      }
    }, 100);
  }

  predictMore() {
    this.show = false;
    this.searchAndPredictButtonCallback();
  }

  searchFromDrugSide(drugSideInput) {
    console.log('searchOnly: drugSideInput');
    let t0 = performance.now();

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

          let t1 = performance.now();
          this.elapsedTime += (t1-t0);

          this.makeOutput(plaSet,comSet,proSet,disSet,
                          plaVScom,comVSpro,proVSdis);
        })
      })
    })
  }

  searchFromTargetSide(targetSideInput) {
    console.log('searchOnly: targetSideInput');
    let t0 = performance.now();

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

          let t1 = performance.now();
          this.elapsedTime += (t1-t0);

          this.makeOutput(plaSet,comSet,proSet,disSet,
                          plaVScom,comVSpro,proVSdis);
        })
      })
    })
  }

  searchAndPredict(drugSideInput,targetSideInput) {
    console.log('searchAndPredict');
    let t0 = performance.now();

    let dsi = JSON.stringify(drugSideInput);
    let tsi = JSON.stringify(targetSideInput);
    // console.log(dsi);
    // console.log(tsi);

    this.http.post(this.interactionQueryAPI,dsi).map(resp => resp.json())
    .subscribe(plaVScom => {
      this.http.post(this.interactionQueryAPI,tsi).map(resp2 => resp2.json())
      .subscribe(proVSdis => {
        // Ijah also accomodates syntetic compound vs protein.
        // This means that some compounds have no plant, and some some protein have no disease.
        // However, all plants have compounds, and all diseases have proteins
        let comArr = [];
        if (plaVScom.length===0) {
          for (let i=0;i<drugSideInput.length;i++) {
            let comId = drugSideInput[i]['value'];
            comArr.push(comId)
          }
        }
        else {
          for (let i=0;i<plaVScom.length;i++) {
            let comId = plaVScom[i]['com_id'];
            comArr.push(comId)
          }
        }

        let proArr = [];
        if (proVSdis.length===0) {
          for (let i=0;i<targetSideInput.length;i++) {
            let proId = targetSideInput[i]['value'];
            proArr.push(proId)
          }
        }
        else {
          for (let i=0;i<proVSdis.length;i++) {
            let proId = proVSdis[i]['pro_id'];
            proArr.push(proId)
          }
        }

        let comVSproList = [];
        for (let i=0;i<comArr.length;i++) {
          for (let j=0;j<proVSdis.length;j++) {
            let comId = '"'+comArr[i]+'"';
            let proId = '"'+proArr[j]+'"';
            let comVSpro = '{'+'"comId":'+comId+','+'"proId":'+proId+'}';
            comVSproList.push(comVSpro);
          }
        }

        // make unique
        comVSproList = comVSproList.filter((v, i, a) => a.indexOf(v) === i);

        // make it JSON-format
        let comVSproStr = '';
        for (let k=0;k<comVSproList.length;k++) {
          comVSproStr += comVSproList[k];
          if (k<comVSproList.length-1) {
            comVSproStr = comVSproStr + ',';
          }
        }
        comVSproStr = '['+comVSproStr+']';

        this.http.post(this.interactionQueryAPI,comVSproStr).map(resp3 => resp3.json())
        .subscribe(comVSpro => {
          let comToPredictArr = [];
          let proToPredictArr = [];
          let idxToPredictArr = [];
          for (let i=0;i<comVSpro.length;i++) {
            let src = comVSpro[i]['source'];
            if (src==='null') {
              comToPredictArr.push(comVSpro[i]['com_id']);
              proToPredictArr.push(comVSpro[i]['pro_id']);
              idxToPredictArr.push(i);
            }
          }
          let comVSproToPredictStr = '';
          for (let i=0;i<comToPredictArr.length;i++) {
            let comId = '"'+comToPredictArr[i]+'"';
            let proId = '"'+proToPredictArr[i]+'"';
            comVSproToPredictStr += '{'+'"comId":'+comId+','+'"proId":'+proId+'}';
            if (i<comToPredictArr.length-1) {
              comVSproToPredictStr += ',';
            }
          }
          comVSproToPredictStr = '['+comVSproToPredictStr+']';
          // console.log(comVSproToPredictStr);

          this.http.post(this.predictAPI,comVSproToPredictStr).map(resp4 => resp4.json())
          .subscribe(hasWaitedForMsg => {
            let hasWaitedFor = parseFloat( hasWaitedForMsg[0]['has_waited_for'] );
            console.log('hasWaitedFor= '+hasWaitedFor.toString());

            this.http.post(this.interactionQueryAPI,comVSproToPredictStr).map(resp5 => resp5.json())
              .subscribe(comVSproPred => {
                let comVSproMerged = comVSpro;
                for (let i=0; i<comVSproPred.length; i++) {
                  let idx = idxToPredictArr[i];
                  comVSproMerged[idx]['com_id'] = comVSproPred[i]['com_id'];
                  comVSproMerged[idx]['pro_id'] = comVSproPred[i]['pro_id'];
                  comVSproMerged[idx]['weight'] = comVSproPred[i]['weight'];
                  comVSproMerged[idx]['source'] = comVSproPred[i]['source'];
                  comVSproMerged[idx]['timestamp'] = comVSproPred[i]['timestamp'];
                }
                // Get unique items
                let plaSet = this.getSet(plaVScom,'pla_id');
                let comSet = this.getSet(comVSproMerged,'com_id');
                let proSet = this.getSet(comVSproMerged,'pro_id');
                let disSet = this.getSet(proVSdis,'dis_id');

                let t1 = performance.now();
                this.elapsedTime += (t1-t0);

                this.makeOutput(plaSet,comSet,proSet,disSet,
                                plaVScom,comVSproMerged,proVSdis);
            })
          })
        })
      })
    })
  }

  // OUTPUT MAKING METHODS /////////////////////////////////////////////////////
  makeOutput(iplaSet,icomSet,iproSet,idisSet,plaVScom,comVSpro,proVSdis) {
    let t0 = performance.now();

    let plaSet = this.handleIfEmptySet(iplaSet,'pla');
    let comSet = this.handleIfEmptySet(icomSet,'com');
    let proSet = this.handleIfEmptySet(iproSet,'pro');
    let disSet = this.handleIfEmptySet(idisSet,'dis');

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
            // connectivity text output ////////////////////////////////////////
            this.plaVScomTxtOutput = this.makeConnectivityTextOutput(plaVScom,
                                                                     plaMeta,comMeta,
                                                                     'pla','com');
            this.comVSproTxtOutput = this.makeConnectivityTextOutput(comVSpro,
                                                                     comMeta,proMeta,
                                                                     'com','pro');
            this.proVSdisTxtOutput = this.makeConnectivityTextOutput(proVSdis,
                                                                     proMeta,disMeta,
                                                                     'pro','dis');

            this.comVSplaTxtOutput = this.makeConnectivityTextOutput(plaVScom,
                                                                     comMeta,plaMeta,
                                                                     'com','pla');
            this.proVScomTxtOutput = this.makeConnectivityTextOutput(comVSpro,
                                                                     proMeta,comMeta,
                                                                     'pro','com');
            this.disVSproTxtOutput = this.makeConnectivityTextOutput(proVSdis,
                                                                     disMeta,proMeta,
                                                                     'dis','pro');


            // metadata text output ////////////////////////////////////////
            this.plaMetaTxtOutput = this.makeMetaTextOutput('pla',plaSet,plaMeta);
            this.comMetaTxtOutput = this.makeMetaTextOutput('com',comSet,comMeta);
            this.proMetaTxtOutput = this.makeMetaTextOutput('pro',proSet,proMeta);
            this.disMetaTxtOutput = this.makeMetaTextOutput('dis',disSet,disMeta);

            // connectivity graph output ///////////////////////////////////////
            let nNodeMax = 20;
            let plaForGraph = plaSet;//plaSet.slice(0,nNodeMax);
            let comForGraph = comSet;//comSet.slice(0,nNodeMax);
            let proForGraph = proSet;//proSet.slice(0,nNodeMax);
            let disForGraph = disSet;//disSet.slice(0,nNodeMax);

            let graphDataArr = [this.makeGraphDataOutput(plaVScom,
                                                         plaMeta,comMeta,
                                                         'pla','com',
                                                         plaForGraph,comForGraph),
                                this.makeGraphDataOutput(comVSpro,
                                                         comMeta,proMeta,
                                                         'com','pro',
                                                         comForGraph,proForGraph),
                                this.makeGraphDataOutput(proVSdis,
                                                         proMeta,disMeta,
                                                         'pro','dis',
                                                         proForGraph,disForGraph)];

            let graphData = [];
            for (let ii=0;ii<graphDataArr.length;ii++) {
              for(let jj=0;jj<graphDataArr[ii].length;jj++) {
                  let datum = graphDataArr[ii][jj];
                  graphData.push(datum);
              }
            }

            localStorage.setItem('connectivityGraphData', JSON.stringify(graphData));
            this.show = true;

            // summary text output /////////////////////////////////////////////
            let plaComConnScore = this.getConnectivityScore(plaVScom);
            let comProConnScore = this.getConnectivityScore(comVSpro);
            let proDisConnScore = this.getConnectivityScore(proVSdis);
            let totConnScore = plaComConnScore+comProConnScore+proDisConnScore;
            let nDecimalDigits = 5;

            let nUnknownComProConn = 0;
            let nUndefinedComProConn = 0;
            let nKnownByExperimentComProConn = 0;
            let nKnownByPredictionComProConn = 0;
            for (let i=0; i<comVSpro.length; i++) {
              let src = comVSpro[i]['source']
              if (src==='null') {// unknown
                nUnknownComProConn += 1;
              }
              else if (this.comProConnExperimentSrcs.indexOf(src)!==-1) {
                nKnownByExperimentComProConn += 1;
              }
              else if (this.comProConnPredictionSrcs.indexOf(src)!==-1) {
                nKnownByPredictionComProConn += 1;
              }
              else {
                nUndefinedComProConn += 1;
              }
            }

            if (this.mode==='search_only') {
              nUnknownComProConn = (icomSet.length*iproSet.length)-(nKnownByPredictionComProConn+nKnownByExperimentComProConn);
            }

            this.summaryTxtOutput = 'Connectivity Score:\n';
            this.summaryTxtOutput += '   Total: '+this.floatToStrTruncated(totConnScore,nDecimalDigits)+'\n';
            this.summaryTxtOutput += '   Plant-Compound  : '+plaComConnScore.toString()+'\n';
            this.summaryTxtOutput += '   Compound-Protein: '+this.floatToStrTruncated(comProConnScore,nDecimalDigits)+'\n';
            this.summaryTxtOutput += '   Protein-Disease : '+proDisConnScore.toString()+'\n';

            this.summaryTxtOutput2 = 'Number of unique items:\n';
            this.summaryTxtOutput2 += '   #Plants   : '+iplaSet.length.toString()+this.getInputMark('plant')+'\n';
            this.summaryTxtOutput2 += '   #Compounds: '+icomSet.length.toString()+this.getInputMark('compound')+'\n';
            this.summaryTxtOutput2 += '   #Proteins : '+iproSet.length.toString()+this.getInputMark('protein')+'\n';
            this.summaryTxtOutput2 += '   #Diseases : '+idisSet.length.toString()+this.getInputMark('disease')+'\n';
            this.summaryTxtOutput2 += 'Compound-Protein Connectivity:\n';
            this.summaryTxtOutput2 += '   #known_by_experiment: '+nKnownByExperimentComProConn.toString()+'\n';
            this.summaryTxtOutput2 += '   #known_by_prediction: '+nKnownByPredictionComProConn.toString()+'\n';
            this.summaryTxtOutput2 += '   #unknown            : '+nUnknownComProConn.toString()+'\n';
            if (nUndefinedComProConn>0) {
              this.summaryTxtOutput2 += '   #undefined            : '+nUndefinedComProConn.toString()+'\n';
            }

            let t1 = performance.now();
            this.elapsedTime += (t1-t0);
            this.elapsedTime = this.elapsedTime/1000.0;// from ms to s

            this.summaryTxtOutput3 = 'Mode: \n';
            this.summaryTxtOutput3 += '   '+this.mode+'\n';
            this.summaryTxtOutput3 += 'Elapsed Time: \n';
            this.summaryTxtOutput3 += '   '+this.floatToStrTruncated(this.elapsedTime,nDecimalDigits)+' seconds\n';
          }) // disMeta
        }) // proMeta
      }) // comMeta
    }) // plaMeta
  }

  makeMetaTextOutput(type,idList,meta) {
    let keys = this.getPropKeys(type);
    let txt = '#0 '+this.getHeader(type)+'\n';
    for (let i=0; i<idList.length;i++) {
      txt += '#'+(i+1).toString()+' ';
      let props = this.getProps(idList[i],keys,meta);
      txt += this.concatProps(props,keys,true,true)
      txt += '\n';
    }
    return txt;
  }

  makeConnectivityTextOutput(interaction,srcMeta,destMeta,srcType,destType) {
    let conn = this.groupBy(srcType,destType,interaction);

    let text = this.getHeader(srcType+'_vs_'+destType)+'\n';
    let srcPropKeys = this.getPropKeys(srcType);
    let destPropKeys = this.getPropKeys(destType);
    let indent = '  ';

    let nUnique = 0;
    let nUniquePerConnSrc = 0;
    let pos = -1;// in which, we will insert nUniquePerConnSrc
    let prevSrc = '';
    let prevConnSource = '';

    for (let i=0;i<conn.length;i++) {
      for (let j=0;j<conn[i].length;j++) {
        let comps = conn[i][j].split(",");
        let src = comps[0];
        let dest = comps[1];
        let weight = comps[2];
        let source = comps[3];

        if (prevSrc!==src) {
          if (i>0) {
            text = [text.slice(0,pos),nUniquePerConnSrc.toString(), text.slice(pos)].join('');
          }

          nUnique = nUnique + 1;
          text = text+'#'+nUnique.toString()+' ';

          let srcProps = this.getProps(src,srcPropKeys,srcMeta);
          text += this.concatProps(srcProps,srcPropKeys,true,true)
          text +=':\n';

          prevSrc = src;
          prevConnSource = '';
        }

        if (prevConnSource!==source) {
          text += indent+'['+source+':]\n';
          pos = text.length - 2;
          prevConnSource = source;
          nUniquePerConnSrc = 1;
        }
        else {
          nUniquePerConnSrc += 1;
        }

        let destProps = this.getProps(dest,destPropKeys,destMeta);
        text += indent+'['+weight+'] ';
        text += this.concatProps(destProps,destPropKeys,true,true)
        text += '\n';
      }
    }
    text = [text.slice(0,pos),nUniquePerConnSrc.toString(), text.slice(pos)].join('');

    if (text==='') {
      text = 'No Connectivity';
    }

    return text;
  }

  makeGraphDataOutput(interaction,srcMeta,destMeta,srcType,destType,srcItems,destItems) {
    let srcPropKeys = this.getPropKeys(srcType);
    let destPropKeys = this.getPropKeys(destType);
    let data = [];

    let srcHasDestArr = [];
    let destHasSrcArr = [];
    for (let i=0;i<srcItems.length;i++) {
      srcHasDestArr.push(false);
    }
    for (let i=0;i<destItems.length;i++) {
      destHasSrcArr.push(false);
    }

    for(let i=0;i<interaction.length;i++) {
      let datum = [];

      let srcKey = srcType+'_id';
      let destKey = destType+'_id';

      let src = interaction[i][srcKey];
      let dest = interaction[i][destKey];

      let srcIdx = srcItems.indexOf(src);
      let destIdx = destItems.indexOf(dest);

      if ((srcIdx!==-1)&&(destIdx!==-1)) {
        srcHasDestArr[srcIdx] = true;
        destHasSrcArr[destIdx] = true;

        let source = interaction[i]['source'];
        let weight = parseFloat( interaction[i]['weight'] );

        let srcProps = this.getProps(src,srcPropKeys,srcMeta);
        let destProps = this.getProps(dest,destPropKeys,destMeta);
        let srcText = this.concatProps(srcProps,srcPropKeys,false,false);
        let destText = this.concatProps(destProps,destPropKeys,false,false);

        srcText = this.truncateText(srcText);
        destText = this.truncateText(destText);

        datum.push(srcText);
        datum.push(destText);
        datum.push(weight);

        data.push(datum);
      }
    }

    // Make _dummy_ interaction (... vs anchor) to beautify the graph rendering
    let wDummy = 0.00001;// to become "invisible"
    let prefix = '';
    let srcDummyText = prefix+srcType.toUpperCase();
    let destDummyText = prefix+destType.toUpperCase();

    let anchor = [];
    anchor.push(srcDummyText);
    anchor.push(destDummyText);
    anchor.push(wDummy);
    data.push(anchor);

    for (let i=0;i<srcHasDestArr.length;i++) {
      if (srcHasDestArr[i] === false) {
        let src = srcItems[i];
        let srcProps = this.getProps(src,srcPropKeys,srcMeta);
        let srcText = this.concatProps(srcProps,srcPropKeys,false,false);
        let destText = destDummyText;
        let w = wDummy;

        srcText = this.truncateText(srcText);
        destText = this.truncateText(destText);

        let dummy = [];
        dummy.push(srcText);
        dummy.push(destText);
        dummy.push(w);
        data.push(dummy);
      }
    }
    for (let i=0;i<destHasSrcArr.length;i++) {
      if (destHasSrcArr[i] === false) {
        let srcText = srcDummyText;
        let dest = destItems[i];
        let destProps = this.getProps(dest,destPropKeys,destMeta);
        let destText = this.concatProps(destProps,destPropKeys,false,false);
        let w = wDummy;

        srcText = this.truncateText(srcText);
        destText = this.truncateText(destText);

        let dummy = [];
        dummy.push(srcText);
        dummy.push(destText);
        dummy.push(w);
        data.push(dummy);
      }
    }

    return data;
  }

  // UTILITY METHODS ///////////////////////////////////////////////////////////
  private find(k,arr) {
    let idx = -1;
    for (let i=0;i<arr.length;i++) {
      if (arr[i]===k) {
        idx = i;
        break;
      }
    }
    return idx;
  }

  private groupBy(srcT,destT,iconn) {
    let srcSet = new Array();
    let connSet = new Array();
    for (let i=0;i<iconn.length;i++) {
      let srcV = iconn[i][srcT+'_id'];
      let destV = iconn[i][destT+'_id'];

      let idx = this.find(srcV,srcSet);
      if (idx === -1) {
        idx = srcSet.length;
        srcSet.push(srcV);
        connSet.push( new Array() );
      }

      let w = iconn[i]['weight'];
      let s = iconn[i]['source'];
      let str = srcV+","+destV+","+w+","+s;
      connSet[idx].push(str);
    }

    return connSet;
  }

  toggleConnectivitySwap(type) {
    if (type==='plaVScom') {
      this.plaVScomSwapped = !this.plaVScomSwapped;
    }
    if (type==='comVSpro') {
      this.comVSproSwapped = !this.comVSproSwapped;
    }
    if (type==='proVSdis') {
      this.proVSdisSwapped = !this.proVSdisSwapped;
    }
  }

  floatToStrTruncated(f,nDecimalDigits) {
    let raw = f.toString();
    let radixPos = raw.indexOf('.');
    if (radixPos===-1) {
      return raw;
    }
    else {
      let intStr = raw.slice(0,radixPos);
      let decStr = raw.slice(radixPos+1,radixPos+nDecimalDigits+1);
      return intStr+'.'+decStr;
    }
  }

  private getConnectivityScore(connectivity) {
    let score = 0.0;
    for (let i=0;i<connectivity.length;i++) {
      score += parseFloat(connectivity[i]['weight'])
    }
    return score;
  }

  private getInputMark(type) {
    let mark = '';
    if (this.inputType.indexOf(type)!==-1) {
      mark = ' (as inputs)';
    }
    return mark;
  }

  private makeJSONFormat(arr,key) {
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

  private handleIfEmptySet(set,type) {
    if (set.length>0) {
      return set;
    }
    let newSet = [type.toUpperCase()+'_NONE_DUMMY'];
    return newSet;
  }

  private getSet(interaction,id) {
    let set = [];
    for (let i=0;i<interaction.length;i++) {
      let item = interaction[i][id];
      if (set.indexOf(item) === -1) {
        set.push(item);
      }
    }
    return set;
  }

  private getPropKeys(type) {
    let keys: string[] = [];
    if (type==='pla') {
      keys.push('pla_name');
      keys.push('pla_idr_name')
    }
    if (type==='com') {
      keys.push('com_cas_id');
      keys.push('com_drugbank_id');
      keys.push('com_kegg_id');
      keys.push('com_knapsack_id');
    }
    if (type==='pro') {
      keys.push('pro_uniprot_id');
      // keys.push('pro_uniprot_abbrv');
      keys.push('pro_name');
      keys.push('pro_pdb_id');
    }
    if (type==='dis') {
      keys.push('dis_omim_id');
      keys.push('dis_name');
    }
    return keys;
  }

  private getHyperlinkStr(type,seed) {
    let baseUrl = '';
    if (type==='pla_name') {
      baseUrl = 'https://en.wikipedia.org/wiki/';
    }
    else if (type==='com_knapsack_id') {
      baseUrl = 'http://kanaya.naist.jp/knapsack_jsp/information.jsp?sname=C_ID&word=';
    }
    else if (type==='com_drugbank_id') {
      baseUrl = 'https://www.drugbank.ca/drugs/';
    }
    else if (type==='com_kegg_id') {
      baseUrl = 'http://www.genome.jp/dbget-bin/www_bget?cpd:';
    }
    else if (type==='pro_uniprot_id') {
      baseUrl = 'http://www.uniprot.org/uniprot/';
    }
    else if (type==='pro_pdb_id') {
      baseUrl = 'http://www.rcsb.org/pdb/explore/explore.do?structureId='
    }
    else if (type==='dis_omim_id') {
      baseUrl = 'https://www.omim.org/entry/';
    }
    else {
      baseUrl = 'unknown';
    }

    let urlStr = '';
    if (baseUrl.indexOf('unknown')===-1 && seed && seed!=='' && seed!=='null') {
      let seedComps = seed.split(',');
      for (let i=0; i<seedComps.length;i++) {
        let s = seedComps[i];
        let url: string = baseUrl + s;

        urlStr += '<a href="'+url+'" target="_blank">'+s+'</a>';
        if (i < seedComps.length-1) {
          urlStr += ',';
        }
      }
    }
    else {
      urlStr = seed;
    }

    return urlStr;
  }

  private getProps(id,keys,meta) {
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
    if (idx !== -1) {
      for(let j=0;j<keys.length;j++) {
        let k = keys[j];
        props.push( meta[idx][k] );
      }
    }
    else {
      // console.log('ERROR: NOT FOUND');
    }

    return props;
  }

  private getHeader(type) {
    let indent = '  ';
    let headerArr = new Array();
    headerArr['pla'] = 'LatinName|IndonesianName';
    headerArr['com'] = 'CAS|DrugbankID|KnapsackID|KeggID';
    headerArr['pro'] = 'UniprotID|UniprotName|PDBId(s)';
    headerArr['dis'] = 'OmimID|OmimName';

    headerArr['pla_vs_com'] ='#0 '+headerArr['pla']+':\n'+
                              indent+'[source:#data]'+'\n'+
                              indent+'[weight] '+headerArr['com'];
    headerArr['com_vs_pro'] = '#0 '+headerArr['com']+':\n'+
                              indent+'[source:#data]'+'\n'+
                              indent+'[weight] '+headerArr['pro'];
    headerArr['pro_vs_dis'] = '#0 '+headerArr['pro']+':\n'+
                              indent+'[source:#data]'+'\n'+
                              indent+'[weight] '+headerArr['dis'];

    headerArr['com_vs_pla'] = '#0 '+headerArr['com']+':\n'+
                              indent+'[source:#data]'+'\n'+
                              indent+'[weight] '+headerArr['pla'];
    headerArr['pro_vs_com'] = '#0 '+headerArr['pro']+':\n'+
                              indent+'[source:#data]'+'\n'+
                              indent+'[weight] '+headerArr['com'];
    headerArr['dis_vs_pro'] = '#0 '+headerArr['dis']+':\n'+
                              indent+'[source:#data]'+'\n'+
                              indent+'[weight] '+headerArr['pro'];

    return headerArr[type];
  }

  private concatProps(props,keys,showNull,hyperlinked) {
    let sep = '|';
    let str = '';

    for (let j=0;j<props.length;j++) {
      let prop = props[j];
      let key = keys[j];

      if (!showNull && (!prop || prop==='')) {
        continue;
      }

      if (j>0) {
        str += sep;
      }

      if (hyperlinked) {
        str += this.getHyperlinkStr(key,prop);
      }
      else {
        str += prop;
      }
    }

    return str;
  }

  private truncateText(text) {
    let MAX_NODE_LABEL_LEN = 32;
    let suffix = '...';

    let trunText = text.substr(0,MAX_NODE_LABEL_LEN);
    if (text.length>MAX_NODE_LABEL_LEN) {
      trunText += suffix;
    }

    return trunText;
  }

  private downloadTextOutput(type){
    let txtArr = new Array();
    txtArr['plant_vs_compound'] = this.plaVScomTxtOutput;
    txtArr['compound_vs_protein'] = this.comVSproTxtOutput;
    txtArr['protein_vs_disease'] = this.proVSdisTxtOutput;
    txtArr['compound_vs_plant'] = this.comVSplaTxtOutput;
    txtArr['protein_vs_compound'] = this.proVScomTxtOutput;
    txtArr['disease_vs_protein'] = this.disVSproTxtOutput;
    txtArr['plant'] = this.plaMetaTxtOutput;
    txtArr['compound'] = this.comMetaTxtOutput;
    txtArr['protein'] = this.proMetaTxtOutput;
    txtArr['disease'] = this.disMetaTxtOutput;

    let suffix = '_metadata';
    if (type.indexOf('vs')!==-1) {
      suffix = '_connectivity';
    }

    let filename = 'ijah_'+type+suffix+'.txt';
    let blob = new Blob([ txtArr[type] ], {type: "text/plain;charset=utf-8"});
    saveAs(blob,filename);
  }

  private reset() {
    this.activeTanaman = true;
    this.activeCompound = true;
    this.activeProtein = true;
    this.activeDisease = true;

    this.pTanaman = false;
    this.pCompound = false;
    this.pProtein = false;
    this.pDisease = false;

    this.plaVScomSwapped = false;
    this.comVSproSwapped = false;
    this.proVSdisSwapped = false;

    this.nPlaInputHolders = 0;
    this.nComInputHolders = 0;
    this.nProInputHolders = 0;
    this.nDisInputHolders = 0;
    this.plaInputHolders = [{ 'index': this.nPlaInputHolders, 'value' : ''}];
    this.comInputHolders = [{ 'index': this.nComInputHolders, 'value' : ''}];
    this.proInputHolders = [{ 'index': this.nProInputHolders, 'value' : ''}];
    this.disInputHolders = [{ 'index': this.nDisInputHolders, 'value' : ''}];

    this.selectedPlants = [];
    this.selectedCompounds = [];
    this.selectedProteins = [];
    this.selectedDiseases = [];

    this.mode = 'unknown';
    this.inputType = 'unknown';
    this.elapsedTime = 0;
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
  private example1() {
  this.reset();
  this.plaInputHolders = [{ 'index': 1, 'value' : 'Datura stramonium'}, { 'index': 2, 'value' : 'Trifolium pratense'}, { 'index': 3, 'value' : 'Acacia senegal'}, { 'index': 4, 'value' : ''}];
  this.selectedPlants = [{"index":1,"value":"PLA00002565"},{"index":2,"value":"PLA00001090"},{"index":3,"value":"PLA00000325"}];

  this.nPlaInputHolders = 4;
  this.activeCompound = false;
  this.activeProtein = false;
  this.activeDisease = false;
  }

  private example2() {
  this.reset();
  this.comInputHolders = [{ 'index': 1, 'value' : '117-39-5 | DB04216 | C00004631 | 5280343'}, { 'index': 2, 'value' : '61-50-7 | DB01488 | C00001407 | 6089'}, { 'index': 3, 'value' : '51-55-8 | DB00572 | C00002277 | 174174'}, { 'index': 4, 'value' : ''}];
  this.selectedCompounds = [{ 'index': 1, 'value' : 'COM00000058'}, { 'index': 2, 'value' : 'COM00000014'}, { 'index': 3, 'value' : 'COM00000039'}];

  this.nComInputHolders = 2;
  this.activeDisease = false;
  this.activeTanaman = false;
  this.activeProtein = false;
  }

  private example3() {
  this.reset();
  this.proInputHolders = [{ 'index': 1, 'value' : 'P07437 | Tubulin beta chain'}, { 'index': 2, 'value' : 'P02768 | Serum albumin'}, { 'index': 3, 'value' : ''}];
  this.selectedProteins = [{ 'index': 1, 'value' : 'PRO00002823'}, { 'index': 2, 'value' : 'PRO00001554'}];

  this.nProInputHolders = 3;
  this.activeDisease = false;
  this.activeTanaman = false;
  this.activeCompound = false;
  }

  private example4() {
  this.reset();
  this.disInputHolders = [{ 'index': 1, 'value' : '156610 | Skin creases, congenital symmetric circumferential, 1'}, { 'index': 2, 'value' : '614373 | Amyotrophic lateral sclerosis 16, juvenile'}, { 'index': 3, 'value' : '612244 | Inflammatory bowel disInputHolders 13'}, { 'index': 4, 'value' : ''}];
  this.selectedDiseases = [{ 'index': 1, 'value' : 'DIS00001455'}, { 'index': 2, 'value' : 'DIS00000803'}, { 'index': 3, 'value' : 'DIS00003796'}];

  this.nDisInputHolders = 4;
  this.activeProtein = false;
  this.activeTanaman = false;
  this.activeCompound = false;
  }

  private example5() {
  this.reset();
  this.plaInputHolders = [{ 'index': 1, 'value' : 'Catharanthus roseus'}, { 'index': 2, 'value' : 'Nigella sativa'}, { 'index': 3, 'value' : 'Cocos nucifera'}, { 'index': 4, 'value' : ''}];
  this.selectedPlants = [{"index":1,"value":"PLA00001025"},{"index":2,"value":"PLA00003511"},{"index":3,"value":"PLA00001600"}];
  this.nPlaInputHolders = 4;

  this.proInputHolders = [{ 'index': 1, 'value' : 'P07437 | Tubulin beta chain'}, { 'index': 2, 'value' : 'P02768 | Serum albumin'}, { 'index': 3, 'value' : ''}];
  this.selectedProteins = [{ 'index': 1, 'value' : 'PRO00002823'}, { 'index': 2, 'value' : 'PRO00001554'}];

  this.nProInputHolders = 3;

  this.activeDisease = false;
  this.activeCompound = false;
  }

  private example6() {
  this.reset();
  this.comInputHolders = [{ 'index': 1, 'value' : '51-55-8 | DB00572 | C00002277 | 174174'}, { 'index': 2, 'value' : '51-34-3 | DB00747 | C00002292 | C01851'}, { 'index': 3, 'value' : '53-86-1 | DB00328 | C00030512 | C01926'}, { 'index': 4, 'value' : ''}];
  this.selectedCompounds = [{ 'index': 1, 'value' : 'COM00000039'}, { 'index': 2, 'value' : 'COM00001628'}, { 'index': 3, 'value' : 'COM00005599'}];

  this.nComInputHolders = 2;

  this.disInputHolders = [{ 'index': 1, 'value' : '608516 | Major depressive disorder'}, { 'index': 2, 'value' : '100100 | Prune belly syndrome'}, { 'index': 3, 'value' : '614473 | Arterial calcification of infancy, generalized, 2'}, { 'index': 4, 'value' : ''}];
  this.selectedDiseases = [{ 'index': 1, 'value' : 'DIS00000849'}, { 'index': 2, 'value' : 'DIS00003796'}, { 'index': 3, 'value' : 'DIS00000853'}];

  this.nDisInputHolders = 4;

  this.activeTanaman = false;
  this.activeProtein = false;
  }

  private example7() {
  this.reset();
  this.plaInputHolders = [{ 'index': 1, 'value' : 'Aloe vera'}, { 'index': 2, 'value' : 'Cocos nucifera'}, { 'index': 3, 'value' : 'Panax ginseng'}, { 'index': 4, 'value' : ''}];
  this.selectedPlants = [{"index":1,"value":"PLA00001504"},{"index":2,"value":"PLA00001600"},{"index":3,"value":"PLA00003447"}];
  this.nDisInputHolders = 4;

  this.disInputHolders = [{ 'index': 1, 'value' : '61600 | Analbuminemia'}, { 'index': 2, 'value' : '615999 | Hyperthyroxinemia, familial dysalbuminemic'}, { 'index': 3, 'value' : ''}];
  this.selectedDiseases = [{ 'index': 1, 'value' : 'DIS00003787'}, { 'index': 2, 'value' : 'DIS00003675'}];

  this.nDisInputHolders = 3;

  this.activeCompound = false;
  this.activeProtein = false;
  }

  private example8() {
  this.reset();
  this.comInputHolders = [{ 'index': 1, 'value' : '51-55-8 | DB00572 | C00002277 | 174174'}, { 'index': 2, 'value' : '61-50-7 | DB01488 | C00001407 | 6089'}, { 'index': 3, 'value' : '117-39-5 | DB04216 | C00004631 | 5280343'}, { 'index': 4, 'value' : ''}];
  this.selectedCompounds = [{ 'index': 1, 'value' : 'COM00000039'}, { 'index': 2, 'value' : 'COM00000014'}, { 'index': 3, 'value' : 'COM00000058'}];

  this.nComInputHolders = 2;

  this.proInputHolders = [{ 'index': 1, 'value' : 'P53985 | Monocarboxylate transporter 1'}, { 'index': 2, 'value' : 'P20309 | Muscarinic acetylcholine receptor M3'}, { 'index': 3, 'value' : 'Q99720 | Sigma non-opioid intracellular receptor 1'}, { 'index': 4, 'value' : ''}];
  this.selectedProteins = [{ 'index': 1, 'value' : 'PRO00000040'}, { 'index': 2, 'value' : 'PRO00000452'}, { 'index': 3, 'value' : 'PRO00000377'}];

  this.nProInputHolders = 4;

  this.activeTanaman = false;
  this.activeDisease = false;
  }
}

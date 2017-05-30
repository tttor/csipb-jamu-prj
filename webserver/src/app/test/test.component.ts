import { Component, OnInit, Injectable, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NodeEvent, TreeModel, RenamableNode, Ng2TreeSettings } from 'ng2-tree';
import * as _ from 'lodash';
import {
    TreeviewI18n, TreeviewItem, TreeviewConfig, TreeviewHelper,
    TreeviewComponent, TreeviewEventParser, OrderDownlineTreeviewEventParser,
    DownlineTreeviewItem
  } from 'ng2-dropdown-treeview';
import { TreeService } from './test.service';

declare const alertify: any;

@Injectable()
export class ProductTreeviewConfig extends TreeviewConfig {
    isShowAllCheckBox = true;
    isShowFilter = true;
    isShowCollapseExpand = false;
    maxHeight = 500;
}

@Component({
  selector: 'test',
  styles: [`
  `],
  templateUrl: './test.component.html',
  providers: [
        TreeService,
        { provide: TreeviewEventParser, useClass: OrderDownlineTreeviewEventParser },
        { provide: TreeviewConfig, useClass: ProductTreeviewConfig }
    ]
})

export class TestComponent implements OnInit {

  @ViewChild(TreeviewComponent) treeviewComponent: TreeviewComponent;
    items: TreeviewItem[];
    rows: string[];

  public settings: Ng2TreeSettings = {
    rootIsVisible: false
  };

  public ijahtree: TreeModel;

  private static logEvent(e: NodeEvent, message: string): void {
    console.log(e);
    alertify.message(`${message}: ${e.node.value}`);
  }

  private localState;
  constructor(public route: ActivatedRoute, private service: TreeService) {
    // do nothing
  }

  public ngOnInit(): void {

    this.items = this.service.getProducts();

    this.ijahtree = {
      value: 'From Plants',
      children: [
          { value: 'Plant 3',
          loadChildren: (callback) => {
            setTimeout(() => {
              callback([
                {value: 'Compound 3.1',
                  loadChildren: (callback) => {
                    setTimeout(() => {
                      callback([
                        {value: 'Protein 3.1.1'},
                        {value: 'Protein 3.1.2'},
                      ]);
                    }, 100);
                  }
                },
                {value: 'Compound 3.2'},
                {value: 'Compound 3.3'},
                {value: 'Compound 3.4'},
                {value: 'Compound 3.5'},
              ]);
            }, 100);
          }
          },
      ]
    };
  }

  onItemCheckedChange(item: TreeviewItem) {
      console.log(item);
  }

  onSelectedChange(downlineItems: DownlineTreeviewItem[]) {
      this.rows = [];
      downlineItems.forEach(downlineItem => {
          const item = downlineItem.item;
          const value = item.value;
          const texts = [item.text];
          let parent = downlineItem.parent;
          while (!_.isNil(parent)) {
              texts.push(parent.item.text);
              parent = parent.parent;
          }
          const reverseTexts = _.reverse(texts);
          const row = `${reverseTexts.join(' -> ')} : ${value}`;
          this.rows.push(row);
      });
  }

  removeItem(item: TreeviewItem) {
      TreeviewHelper.removeItem(item, this.items);
      this.treeviewComponent.raiseSelectedChange();
  }

  // DON'T DELETE - will be used again later ///////////////////////////////////
  // public treeTest1() {
  //   this.ijahtree = {
  //     value: 'From Plants',
  //     children: [
  //         { value: 'Plant 3',
  //         loadChildren: (callback) => {
  //           setTimeout(() => {
  //             callback([
  //               {value: 'Compound 3.1',
  //                 loadChildren: (callback) => {
  //                   setTimeout(() => {
  //                     callback([
  //                       {value: 'Protein 3.1.1'},
  //                       {value: 'Protein 3.1.2'},
  //                     ]);
  //                   }, 100);
  //                 }
  //               },
  //               {value: 'Compound 3.2'},
  //               {value: 'Compound 3.3'},
  //               {value: 'Compound 3.4'},
  //               {value: 'Compound 3.5'},
  //             ]);
  //           }, 100);
  //         }
  //         },
  //     ]
  //   };
  // }

  public onNodeRemoved(e: NodeEvent): void {
    TestComponent.logEvent(e, 'Removed');
  }

  public onNodeMoved(e: NodeEvent): void {
    TestComponent.logEvent(e, 'Moved');
  }

  public onNodeRenamed(e: NodeEvent): void {
    TestComponent.logEvent(e, 'Renamed');
  }

  public onNodeCreated(e: NodeEvent): void {
    TestComponent.logEvent(e, 'Created');
  }

  public onNodeSelected(e: NodeEvent): void {
    TestComponent.logEvent(e, 'Name');
  }

}

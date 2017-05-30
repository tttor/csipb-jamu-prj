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
    public isShowAllCheckBox = true;
    public isShowFilter = true;
    public isShowCollapseExpand = false;
    public maxHeight = 500;
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
    public items: TreeviewItem[];
    public rows: string[];

  private localState;
  constructor(public route: ActivatedRoute, private service: TreeService) {
    // do nothing
  }

  public ngOnInit(): void {

    this.items = this.service.getProducts();
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

}

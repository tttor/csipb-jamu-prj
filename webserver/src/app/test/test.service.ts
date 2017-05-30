import { Injectable } from '@angular/core';
import { TreeviewItem } from 'ng2-dropdown-treeview';

export class TreeService {
    public getProducts(): TreeviewItem[] {
        const fruitCategory = new TreeviewItem({
            text: 'Fruit', value: 1, collapsed: true, children: [
                { text: 'Apple', value: 11, collapsed: true, children: [
                  { text: 'Ganja', value: 12 }
                ] },
                { text: 'Mango', value: 12 }
            ]
        });
        const vegetableCategory = new TreeviewItem({
            text: 'Vegetable', value: 2, collapsed: true, children: [
                { text: 'Salad', value: 21 },
                { text: 'Potato', value: 22 }
            ]
        });
        const plantCategory = new TreeviewItem({
          text: 'Plants', value: 0, collapsed: true, children: [
            {
              text: 'Plant 1', value: 1.0, collapsed: true, children: [
                { text: 'Compound 1', value: 1.0, collapsed: true, children: [
                  { text: 'Protein 1', value: 0.8, collapsed: true, children: [
                    { text: 'Disease 1', value: 1.0 }
                  ] }
                ] },
                { text: 'Compound 2', value: 0.6 }
              ]
            },
            {
              text: 'Plant 2', value: 1.0, collapsed: true, children: [
                { text: 'Compound 1', value: 1.0, collapsed: true, children: [
                  { text: 'Protein 1', value: 0.8, collapsed: true, children: [
                    { text: 'Disease 1', value: 1.0 }
                  ] }
                ] },
                { text: 'Compound 2', value: 0.6 }
              ]
            }
          ]
        });
        vegetableCategory.children.push(new TreeviewItem({ text: 'Mushroom', value: 23, checked: false }));
        vegetableCategory.correctChecked(); // need this to make 'Vegetable' node to change checked value from true to false
        plantCategory.correctChecked();
        return [fruitCategory, vegetableCategory, plantCategory];
    }
}

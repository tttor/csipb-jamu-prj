import { Injectable } from '@angular/core';
import { TreeviewItem } from 'ng2-dropdown-treeview';

export class TreeService {
    getProducts(): TreeviewItem[] {
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
        vegetableCategory.children.push(new TreeviewItem({ text: 'Mushroom', value: 23, checked: false }));
        vegetableCategory.correctChecked(); // need this to make 'Vegetable' node to change checked value from true to false
        return [fruitCategory, vegetableCategory];
    }
}

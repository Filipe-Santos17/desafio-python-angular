import { Component, EventEmitter, Input, Output } from "@angular/core";
import { tProduct } from "../../../../../@types";

@Component({
    selector: 'delete-modal-product',
    templateUrl: './delete-modal-product.html'
})
export class DeleteModalProduct {
    @Input() product!: tProduct; 
    @Input() onConfirmDelete!: () => void;
    @Output() close = new EventEmitter<void>();
}
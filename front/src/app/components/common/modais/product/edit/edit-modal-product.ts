import { FormsModule } from "@angular/forms";
import { Component, EventEmitter, Input, Output, OnChanges, SimpleChanges } from "@angular/core";
import { tProduct } from "../../../../../@types";

@Component({
    selector: 'edit-modal-product',
    standalone: true,
    templateUrl: './edit-modal-product.html',
    imports: [FormsModule],
})
export class EditModalProduct implements OnChanges {

    @Input() product!: tProduct;

    @Input() onConfirmEdit!: (data: {
        id: number;
        name: string;
        mark: string;
        value: number;
    }) => void;

    @Output() close = new EventEmitter<void>();

    name!: string;
    mark!: string;
    value!: number;

    ngOnChanges(changes: SimpleChanges) {
        if (changes['product'] && this.product) {
            this.name = this.product.name;
            this.mark = this.product.mark;
            this.value = this.product.value;
        }
    }

    handleSubmit() {
        this.onConfirmEdit({
            id: this.product.id,
            name: this.name,
            mark: this.mark,
            value: this.value,
        });
    }
}
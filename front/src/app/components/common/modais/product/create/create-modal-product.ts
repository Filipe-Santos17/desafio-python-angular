import { Component, EventEmitter, Input, Output } from "@angular/core";

@Component({
    selector: 'create-modal-product',
    templateUrl: './create-modal-product.html',
    standalone: true,
})
export class CreateModalProduct {
    name!: string;
    mark!: string;
    value!: number;

    @Input() onConfirmCreate!: (data: {
        name: string;
        mark: string;
        value: number;
    }) => void;

    @Output() close = new EventEmitter<void>();

    handleSubmit() {
        this.onConfirmCreate({
            name: this.name,
            mark: this.mark,
            value: this.value,
        });
    }
}
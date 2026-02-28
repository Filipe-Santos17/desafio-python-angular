import { Component, Input, Output, EventEmitter } from "@angular/core";
import { CommonModule } from "@angular/common";

@Component({
  selector: "input-component",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./input.component.html",
})
export class InputComponent {
  /**
   * Este componente aceita todas as propriedades
   * nativas de um input HTML:
   *
   * - type
   * - placeholder
   * - autocomplete
   * - disabled
   * - required
   * - name
   * - id
   * - value
   * - etc...
   *
   * Basta passá-las via property binding no uso do componente.
   */

  @Input() type: string = "text";
  @Input() id?: string;
  @Input() placeholder?: string;
  @Input() autocomplete?: string;
  @Input() disabled: boolean = false;
  @Input() value: string = "";
  @Input() invalid: boolean = false;

  @Output() valueChange = new EventEmitter<string>();

  onInput(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.valueChange.emit(value);
  }
}
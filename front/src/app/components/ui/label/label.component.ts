import { Component, Input } from "@angular/core";
import { CommonModule } from "@angular/common";

@Component({
  selector: "label-component",
  standalone: true,
  imports: [CommonModule],
  templateUrl: "./label.component.html",
})
export class LabelComponent {
  @Input() text: string = "";
  @Input() for: string = "";
}
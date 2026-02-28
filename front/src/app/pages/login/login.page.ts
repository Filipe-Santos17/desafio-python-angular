import { Component, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InputComponent } from '../../components/ui/input/input.component';
import { LabelComponent } from '../../components/ui/label/label.component';

@Component({
  selector: 'page-login',
  standalone: true,
  imports: [CommonModule, InputComponent, LabelComponent],
  templateUrl: './login.page.html',
})
export class LoginPage {
  // STATE
  email = signal('');
  password = signal('');
  submitted = signal(false);

  // VALIDATIONS
  emailError = computed(() => {
    if (!this.submitted()) return '';
    if (!this.email()) return 'Email é obrigatório';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email()))
      return 'Email inválido';
    return '';
  });

  passwordError = computed(() => {
    if (!this.submitted()) return '';
    if (!this.password()) return 'Senha é obrigatória';
    if (this.password().length < 6)
      return 'Senha deve ter no mínimo 6 caracteres';
    return '';
  });

  isValid = computed(() =>
    !this.emailError() && !this.passwordError()
  );

  async onSubmit() {
    this.submitted.set(true);

    if (!this.isValid()) return;

    const data = {
      email: this.email(),
      password: this.password(),
    }

    const request = await fetch("", {
      body: JSON.stringify(data),
    })
  }
}
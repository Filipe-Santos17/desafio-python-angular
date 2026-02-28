import { Component, signal, computed, inject  } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InputComponent } from '../../components/ui/input/input.component';
import { LabelComponent } from '../../components/ui/label/label.component';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { globalFetch } from '../../services/global_fetch';
import { tDataLogin } from '../../@types';

@Component({
  selector: 'page-login',
  standalone: true,
  imports: [CommonModule, InputComponent, LabelComponent, FormsModule],
  templateUrl: './login.page.html',
})
export class LoginPage {
  private router = inject(Router);

  // STATE
  email = signal('');
  password = signal('');
  submitted = signal(false);
  loading = signal(false);
  serverError = signal('');

  // VALIDATIONS
  emailError = computed(() => {
    if (!this.submitted()) return '';
    if (!this.email().trim()) return 'Email é obrigatório';
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

    // evita duplo submit
    if (this.loading()) return; 

    this.serverError.set('');

    if (!this.isValid()) return;

    this.loading.set(true);

    try {
      const { data } = await globalFetch<{email:string, password: string}, tDataLogin>("auth-login", {
        email: this.email().trim(),
        password: this.password()
      })

      localStorage.setItem('access_token', data.access_token);

      this.router.navigate(['/app']);
    } catch (error: any) {
      this.serverError.set(error.message || 'Erro ao autenticar');
    } finally {
      this.loading.set(false);
    }
  }
}
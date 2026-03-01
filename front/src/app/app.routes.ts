import { Routes } from '@angular/router';
import { LoginPage } from './pages/login/login.page';
import { ProductsPage } from './pages/products/products.page';
import { authGuard } from './guards/auth-guard';
import { guestGuard } from './guards/guest-guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'products',
    pathMatch: 'full'
  },
  {
    path: 'products', 
    component: ProductsPage,
    canActivate: [authGuard] 
  },
  {
    path: 'login',
    component: LoginPage,
    canActivate: [guestGuard]
  },
  {
    path: '**',
    redirectTo: 'products'
  }
];
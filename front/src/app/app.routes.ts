import { Routes } from '@angular/router';
import { LoginPage } from './pages/login/login.page';
import { ProductsPage } from './pages/products/products.page';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'products',
    pathMatch: 'full'
  },
  {
    path: 'products', 
    component: ProductsPage,
  },
  {
    path: 'login',
    component: LoginPage,
  },
  {
    path: '**',
    redirectTo: 'products'
  }
];
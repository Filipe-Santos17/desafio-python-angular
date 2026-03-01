import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { getToken } from '../services/token';

export const authGuard: CanActivateFn = () => {
  const router = inject(Router);

  const token = getToken();

  return token ? true : router.createUrlTree(['/login']);
};
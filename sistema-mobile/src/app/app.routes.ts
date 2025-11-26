import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.TenisPage),
  },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full',
  },
  {
    path: 'login',
    loadComponent: () => import('./login/login.page').then(m => m.LoginPage)
  },
  {
    path: 'cadastrar-tenis',
    loadComponent: () => import('./cadastrar-tenis/cadastrar-tenis.page').then(m => m.CadastrarTenisPage)
  },
  {
    path: 'editar-tenis/:id',
    loadComponent: () => import('./editar-tenis/editar-tenis.page').then(m => m.EditarTenisPage)
  },
];

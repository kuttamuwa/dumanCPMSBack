import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AboutComponent } from './about/about.component';
import { CheckAccountComponent } from './check-account/check-account.component';

import { LoginComponent } from './login/login.component';
import { ConfigComponent } from './config/config.component';
import { RiskAnalysisComponent } from './risk-analysis/risk-analysis.component';
import { LayoutComponent } from './layout/layout.component';
import { AuthGuard } from './auth.service';

const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full'},
  { path: 'login', component: LoginComponent },
  { path: '', component: LayoutComponent, children: [
    {
      path: "checkaccount", component: CheckAccountComponent, canActivate: [AuthGuard]
    },
    {
      path: 'riskanalysis', component: RiskAnalysisComponent, canActivate: [AuthGuard]
    },
    {
      path: 'about', component: AboutComponent, canActivate: [AuthGuard]
    },
    {
      path: 'config', component: ConfigComponent, canActivate: [AuthGuard]
    }]
  }];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

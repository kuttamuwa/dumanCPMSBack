import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { MaterialModule } from './material.module';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { LoginDialogComponent } from './login-dialog/login-dialog.component';
import { CheckAccountComponent } from './check-account/check-account.component';
import { CheckAccountDialogComponent } from './check-account/check-account.dialog';
import { RiskAnalysisComponent } from './risk-analysis/risk-analysis.component';
import { AboutComponent } from './about/about.component';
import { ConfigComponent } from './config/config.component';

import { AppService } from './app.service';
import { AuthGuard, AuthService, AuthInterceptor } from './auth.service';
import { MatDialogModule, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { LoginComponent } from './login/login.component';
import { LayoutComponent } from './layout/layout.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginDialogComponent,
    CheckAccountComponent,
    RiskAnalysisComponent,
    AboutComponent,
    ConfigComponent,
    CheckAccountDialogComponent,
    LoginComponent,
    CheckAccountComponent,
    LayoutComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MaterialModule,
    MatDialogModule,
    MatProgressSpinnerModule
  ],
  providers: [
    { provide: MatDialogRef, useValue: {} },
    { provide: MAT_DIALOG_DATA, useValue: {} },
    AppService,
    AuthService,
    AuthGuard,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    }
  ],
  entryComponents: [LoginDialogComponent],
  bootstrap: [AppComponent]
})
export class AppModule { }

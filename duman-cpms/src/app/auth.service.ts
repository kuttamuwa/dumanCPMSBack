import { Injectable } from '@angular/core';
import { HttpClient, HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpHeaders } from '@angular/common/http';
import { CanActivate, Router } from '@angular/router';

import { Observable } from 'rxjs';
import { tap, shareReplay } from 'rxjs/operators';

import * as moment from 'moment';
import jwtDecode from 'jwt-decode';
import { AppState } from './app.state';

@Injectable()
export class AuthService {

  private apiRoot = 'http://127.0.0.1:8000/auth/';

  constructor(private http: HttpClient, private router: Router) { }

  private setSession(authResult) {
    const token = authResult.token;
    const payload = <JWTPayload> jwtDecode(token);
    const expiresAt = moment.unix(payload.exp);
    AppState.username = payload.username;

    localStorage.setItem('username', payload.username);
    localStorage.setItem('token', authResult.token);
    localStorage.setItem('expires_at', JSON.stringify(expiresAt.valueOf()));
  }

  get token(): string {
    return localStorage.getItem('token');
  }

  login(username: string, password: string) {
    let formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    return this.http.post(
      this.apiRoot.concat('login/'), formData
    ).pipe(
      tap(response => this.setSession(response)),
      shareReplay(),
    );
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('expires_at');
    AppState.username = undefined;
    this.router.navigate(['login']);
  }

  getExpiration() {
    const expiration = localStorage.getItem('expires_at');
    const expiresAt = JSON.parse(expiration);

    return moment(expiresAt);
  }

  isLoggedIn() {
    return moment().isBefore(this.getExpiration());
  }
}

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = localStorage.getItem('token');

    if (token) {
      const cloned = req.clone({
        headers: req.headers.set('Authorization', 'JWT '.concat(token))
      });

      return next.handle(cloned);
    } else {
      return next.handle(req);
    }
  }
}

@Injectable()
export class AuthGuard implements CanActivate {

  constructor(private authService: AuthService, private router: Router) { }

  canActivate() {
    if (this.authService.isLoggedIn()) {
      AppState.username = localStorage.getItem('username');
      return true;
    } else {
      this.authService.logout();

      return false;
    }
  }
}

interface JWTPayload {
  user_id: number;
  username: string;
  email: string;
  exp: number;
}
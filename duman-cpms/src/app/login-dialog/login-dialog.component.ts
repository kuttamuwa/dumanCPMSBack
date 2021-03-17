import { Component, ElementRef, Inject, ViewChild } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormControl, NgForm, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-dialog',
  templateUrl: './login-dialog.component.html',
  styleUrls: ['./login-dialog.component.css']
})
export class LoginDialogComponent {
  username = new FormControl('', [Validators.required]);
  password = new FormControl('', [Validators.required]);

  error: any;

  @ViewChild('passwordInput') passwordInput: ElementRef;

  constructor(
    private authService: AuthService, private router: Router,
    public dialogRef: MatDialogRef<LoginDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) { }

  PeepButtonOnClick = () => {
    this.passwordInput.nativeElement.setAttribute("type", "text");
    let _this = this;
    setTimeout(function() {
      _this.passwordInput.nativeElement.setAttribute("type", "password");
    }, 1000);
  }

  UsernameOnKeyup = (e: KeyboardEvent) => {
    if (e.key === "Enter" && this.username.value !== '' && this.password.value !== '')
      this.login();
  }

  PasswordOnKeyup = (e: KeyboardEvent) => {
    if (e.key === "Enter" && this.username.value !== '' && this.password.value !== '')
      this.login();
  }

  login() {
    this.authService.login(this.username.value, this.password.value).subscribe(
      success => { 
        this.dialogRef.close();
        this.router.navigate(['checkaccount'])
      },
      error => {
        this.error = error
      });
  }
}

export interface DialogData {
  username: string;
  password: string;
}

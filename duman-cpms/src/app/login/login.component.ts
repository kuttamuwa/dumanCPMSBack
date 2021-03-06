import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../auth.service';
import { LoginDialogComponent } from '../login-dialog/login-dialog.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(public dialog: MatDialog, private authService: AuthService, private router: Router) {
    if (authService.isLoggedIn())
      router.navigate(['checkaccount']);
  }

  ngOnInit(): void {
    this.dialog.open(LoginDialogComponent, {
      width: "25vw",
      hasBackdrop: false,
      disableClose: true
    });
  }

}

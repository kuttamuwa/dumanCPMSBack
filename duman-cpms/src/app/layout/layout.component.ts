import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { AppService } from '../app.service';
import { AppState } from '../app.state';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.css']
})
export class LayoutComponent implements OnInit {

  AppState = AppState;

  isPersonCardOpen = false;

  @ViewChild('personCard', {read: ElementRef}) personCard: ElementRef;

  constructor(private appService: AppService, private authService: AuthService) {
  }

  ngOnInit() {
    this.appService.getCities().subscribe(cities => {
      AppState.cities = cities.map(c => c["name"]);
    });
    this.appService.getAccounts().subscribe(accounts => {
      AppState.accounts = accounts;
      AppState.accountsOnLoad.emit(accounts);
    });
  }

  PersonIconOnClick = () => {
    if (this.isPersonCardOpen) {
      (this.personCard.nativeElement as HTMLElement).style.display = "none";
    }
    else {
      (this.personCard.nativeElement as HTMLElement).style.display = "block";
    }
    this.isPersonCardOpen = !this.isPersonCardOpen;
  }
  LogoutButtonOnClick = () => {
    this.authService.logout();
  }
}

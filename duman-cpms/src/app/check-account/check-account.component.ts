import { Component, ViewChild, AfterViewInit, ChangeDetectorRef } from '@angular/core';
import { AppState } from '../app.state';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { Account } from '../../model/Account';
import { MatDialog } from '@angular/material/dialog';
import { CheckAccountDialogComponent, AccountDialogObject, AccountDialogType } from './check-account.dialog';

@Component({
  selector: 'app-check-account',
  templateUrl: './check-account.component.html',
  styleUrls: ['./check-account.component.css']
})
export class CheckAccountComponent implements AfterViewInit {

  AppState = AppState;

  isBusy = true;

  dataSource: MatTableDataSource<Account>;
  columns: string[] = ['firm_full_name', 'firm_type', 'taxpayer_number', 'sector', 'city', 'phone_number', 'email_addr', 'actions'];

  @ViewChild(MatSort) sort: MatSort;
  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(public dialog: MatDialog, private changeDetectorRef: ChangeDetectorRef) { }

  ngAfterViewInit() {
    if (AppState.accounts) {
      this.dataSource = new MatTableDataSource<Account>(AppState.accounts);
      this.dataSource.sort = this.sort;
      this.dataSource.paginator = this.paginator;
      this.isBusy = false;
      this.changeDetectorRef.detectChanges();
    }
    else{
      AppState.accountsOnLoad.subscribe(accounts => {
        this.dataSource = new MatTableDataSource<Account>(accounts);
        this.dataSource.sort = this.sort;
        this.dataSource.paginator = this.paginator;
        this.isBusy = false;
        this.changeDetectorRef.detectChanges();
      });
    }
  }

  CreateAccountOnClick = () => {
    this.dialog.open(CheckAccountDialogComponent, {
      data: {account: undefined, text: 'Yeni Cari Hesap', type: AccountDialogType.Create}
    });
  }
  RowEditOnClick = (row: Account) => {
    this.dialog.open(CheckAccountDialogComponent, {
      data: {account: row, text: 'Cari Hesap Detay/Düzenleme', type: AccountDialogType.Edit}
    });
  }
  RowDeleteOnClick = (row: Account) => {
    this.dialog.open(CheckAccountDialogComponent, {
      data: {account: row, text: undefined, type: AccountDialogType.Delete}
    });
  }
}

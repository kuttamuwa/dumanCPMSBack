import { Component, ElementRef, Inject, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormControl, Validators } from '@angular/forms';
import { Account } from '../../model/Account';
import { AppState } from '../app.state';
import { AppService } from '../app.service';
import { MatSelectChange } from '@angular/material/select';

@Component({
  selector: 'app-check-account-dialog',
  templateUrl: './check-account.dialog.html'
})
export class CheckAccountDialogComponent implements OnInit {

  AppState = AppState;

  districts: string[];
  sectors: string[]; 

  activity_certificate_pdf: FormControl;
  authorized_signatures_list_pdf: FormControl;
  birthplace: FormControl;
  board_management: FormControl;
  city: FormControl;
  district: FormControl;  
  email_addr: FormControl; 
  fax: FormControl; 
  firm_address: FormControl; 
  firm_full_name: FormControl; 
  firm_key_contact_personnel: FormControl; 
  firm_type: FormControl; 
  identity_copies: FormControl;
  partnership_structure_identity_copies: FormControl;
  phone_number: FormControl; 
  sector: FormControl; 
  tax_department: FormControl; 
  tax_return_pdf: FormControl; 
  taxpayer_number: FormControl; 
  web_url: FormControl; 

  AccountDialogType = AccountDialogType;

  constructor(
    private appService: AppService,
    public dialogRef: MatDialogRef<CheckAccountDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: AccountDialogObject) {
        if (data.type == AccountDialogType.Delete)
            data.text = "Hesap kaydı silinecektir. Devam etmek istiyor musunuz?";
        else {
            //text - both - req
            this.firm_full_name = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.firm_full_name , [Validators.required]);
            //number - TCKN: şahıs(11), VKN: tüzel(10) - req
            this.taxpayer_number = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.taxpayer_number , [Validators.required]);
            //radiobutton - both - req
            this.firm_type = new FormControl(data.type == AccountDialogType.Create ? 'Tüzel Kişilik' : data.account.firm_type , [Validators.required]);
            //multiline - both - req
            this.firm_address = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.firm_address);
            //phone - both - req
            this.firm_key_contact_personnel = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.firm_key_contact_personnel);
            //text - both - req
            this.tax_department = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.tax_department , [Validators.required]);
            //combobox - both - req
            this.sector = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.sector);
            //combobox - both - req
            this.city = new FormControl(data.type == AccountDialogType.Create ? 'ISTANBUL' : data.account.city , [Validators.required]);
            //combobox - both - req
            this.district = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.district , [Validators.required]);
            //phone - both - req
            this.phone_number = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.phone_number , [Validators.required]);
            //phone - both
            this.fax = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.fax);
            //email - both - req
            this.email_addr = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.email_addr , [Validators.required]);
            //url - both - req
            this.web_url = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.web_url);
            //combobox - şahıs - req
            this.birthplace = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.birthplace);
            //file - tüzel
            this.board_management = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.board_management);
            //file - both
            this.activity_certificate_pdf = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.activity_certificate_pdf);
            //file - both
            this.authorized_signatures_list_pdf = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.authorized_signatures_list_pdf);
            //file - both
            this.tax_return_pdf = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.tax_return_pdf);
            //file - both
            this.identity_copies = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.identity_copies);
            //file - tüzel
            this.partnership_structure_identity_copies = new FormControl(data.type == AccountDialogType.Create ? '' : data.account.partnership_structure_identity_copies);
        }
    }

    ngOnInit() {
        let currentCity = this.data.type == AccountDialogType.Create ? 'ISTANBUL' : this.data.account.city.toUpperCase();
        this.appService.getDistricts(currentCity).subscribe(d => {
            this.districts = d.map(d_ => d_["name"]);
        });
        this.appService.getSectors().subscribe(s => {
            console.log(s);
        })
    }

    cityOnSelectionChange = (e: MatSelectChange) => {
        this.appService.getDistricts(e.value).subscribe(d => {
            this.districts = d.map(d_ => d_["name"]);
            this.district.enable();
        });
        this.district.disable();
    }
}

export interface AccountDialogObject {
    account: Account;
    text: string;
    type: AccountDialogType;
}

export enum AccountDialogType {
    Create,
    Edit,
    Delete
}

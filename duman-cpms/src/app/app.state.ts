import { EventEmitter } from "@angular/core";
import { Observable } from "rxjs";
import { Account } from "src/model/Account";

export class AppState {
    static accounts: Account[];
    static accountsOnLoad: EventEmitter<Account[]> = new EventEmitter<Account[]>();

    static username: string;

    static cities: string[];
}
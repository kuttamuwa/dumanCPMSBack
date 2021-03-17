import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Account } from '../model/Account';
import { RiskDataset } from 'src/model/RiskDataset';

@Injectable({
  providedIn: 'root',
})
export class AppService {

  private apiRoot = 'http://127.0.0.1:8000/';

  constructor(private http: HttpClient) { }

  getCities(): Observable<string[]> {
    return this.http.get<string[]>(this.apiRoot.concat('checkaccount/api/cities/'));
  }
  
  getDistricts(city: string): Observable<string[]> {
    return this.http.get<string[]>(this.apiRoot.concat('checkaccount/api/district/?city=' + city));
  }

  getAccounts(): Observable<Account[]> {
    return this.http.get<Account[]>(this.apiRoot.concat('checkaccount/api/accounts/'));
  }

  getSectors(): Observable<string[]> {
    return this.http.get<string[]>(this.apiRoot.concat('checkaccount/api/sectors/'));
  }

  postRiskDataset(excelFile: Blob): Observable<any> {
    let formData = new FormData();
    formData.append('excel', excelFile);
    return this.http.post(this.apiRoot.concat('riskanalysis/api/dataset/'), formData);
  }

  getRiskDataset(): Observable<RiskDataset[]> {
    return this.http.get<RiskDataset[]>(this.apiRoot.concat('riskanalysis/api/dataset/'));
  }

  getRiskPoint(riskid: number): Observable<number> {
    return this.http.post<number>(
      this.apiRoot.concat('riskanalysis/api/points/?riskdataset_pk=' + riskid.toString() + '&again=True'),
      {}
    );
  }
}
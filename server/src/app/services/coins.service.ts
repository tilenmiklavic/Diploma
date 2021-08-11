import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CoinsService {

  constructor(private http: HttpClient) { }
  private url = environment.coins_url

  public getCoinsData(): Promise<any> {


    return this.http
      .get(this.url)
      .toPromise()
      .then(data => data as any)
      .catch(CoinsService.obdelajNapako)

  }

  private static obdelajNapako(napaka: any): Promise<any> {
    console.error('Prišlo je do napake', napaka);
    return Promise.reject(napaka.message || napaka);
  }

}

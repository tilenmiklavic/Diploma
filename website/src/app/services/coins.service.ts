import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CoinsService {

  constructor(private http: HttpClient) { }
  private url = environment.coins_url

  // function for getting coins data
  public get(): Promise<any> {
    return this.http
      .get(this.url + "get")
      .toPromise()
      .then(data => data as any)
      .catch(CoinsService.obdelajNapako)
  }

  // function for getting coins tweets
  public getTweets(): Promise<any> {
    return this.http
      .get(this.url + "getTweets")
      .toPromise()
      .then(data => data as any)
      .catch(CoinsService.obdelajNapako)
  }

  // function for scraping new data
  public scrapeData(): Promise<any> {
    return this.http
      .get(this.url + "scrape")
      .toPromise()
      .then(data => data as any)
      .catch(CoinsService.obdelajNapako)
  }

  // function for refreshing coins data
  public refreshCoinsData(): Promise<boolean> {

    return this.http
      .post(this.url, {"time": Date.now()})
      .toPromise()
      .then(odgovor => odgovor as any)
      .catch(CoinsService.obdelajNapako)
  }

  private static obdelajNapako(napaka: any): Promise<any> {
    console.error('Prišlo je do napake', napaka);
    return Promise.reject(napaka.message || napaka);
  }

}

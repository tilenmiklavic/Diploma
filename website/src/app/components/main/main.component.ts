import { Component, OnInit } from '@angular/core';
import { CoinsService } from 'src/app/services/coins.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  constructor(
    private coinService: CoinsService
  ) { }

  // actual coins data used in html
  public coins = []

  // function for calling service for coins data
  private populateTable(): void {
    this.coinService.getCoinsData()
      .then(odgovor => {
        console.log(odgovor)

        this.coins = odgovor.coins
      })
      .catch(napaka => {
        console.error("Napaka:", napaka)
      })
  }

  ngOnInit(): void {
    this.populateTable()
  }
}

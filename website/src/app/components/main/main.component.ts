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

  populateTable() {
    this.coinService.getCoinsData()
      .then(odgovor => {
        console.log("Odgovor")
        console.log(odgovor)
      })
      .catch(napaka => {
        console.error("Napaka:", napaka)
      })
  }

  ngOnInit(): void {
    this.populateTable()
  }
}

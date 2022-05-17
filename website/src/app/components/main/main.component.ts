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
  public coins = [];

  // function for calling service for coins data
  private populateTable(): void {
    this.coinService.get()
      .then(odgovor => {
        for (const [key, value] of Object.entries(odgovor.data)) {
          this.coins.push(value[0])
        }
        console.log("This coins", this.coins)
      })
      .catch(napaka => {
        console.error("Napaka:", napaka)
      })
      .finally(() => {
        this.coinService.getTweets()
        .then(odgovor => {
          console.log(odgovor.tweets)

          odgovor.tweets.forEach(tweet => {
            this.coins.forEach(coin => {
              if (coin.symbol.toLowerCase() === tweet.symbol.toLowerCase()) {
                coin.tweets = tweet.tweet
              }
            })
          });
        })
      })
  }

  ngOnInit(): void {
    this.populateTable()
  }
}

# Recovering Incomplete Monero Wallet

Challenge by [this post](https://steemit.com/giveaway/@generalizethis/free-monero).

This was used to recover the funds from the steemit post linked above. The post reads: 

> During Christmas in 2014, I made Monero wallets as stocking stuffers. Each wallet had a 100 monero in it ($25 at the time, now about $180). I'm not the most detailed orientated person, so needless to say, I forgot a word on one of the wallets. I never gave it away--figuring it would make a nice prize for someone with free time and a dictionary hack.

## Installation
Note: Instruction only tested on Ubuntu

1. Clone repo
2. pip install -r requirements.txt
3. Add [firefox webdriver for selenium](https://github.com/mozilla/geckodriver/releases) to the path.


## How to use
Run the module with the incomplete mnemonic and any wallets with a non-zero transaction history with be printed to the console.
    `python recover_mm_wallet [INCOMPLETE_MNEMONIC]`

Example:
    `python recover_mm_wallet mailed large soothe doctor onward odds zodiac avidly addicted fishing shyness avidly`

## Original Write Up
https://steemit.com/monero/@amustafa/recovering-an-incomplete-monero-mnemonic-wallet

Note: The write-up describes the original path to completing the challenge. I updated the code to make it a little easier for people to use and understand. The logical steps are the same but this works differently.


### Donations

**ETH**: 0x1819c59cA38366A193C8fa02170F254fc9e942E0

**BTC**: 16zRJPnpXiGrNEN3L27nFfrqN239WGyKFb

**XMR**: 48TZ91tfy7w2LVcRape2dPfqchMgkjizm8Ukpr31cHRMgFHkM5DjwPxahs1zby5fQHeAXinhT4U4x8ygEK4zq1gq2A6G4Hy

**DASH**: Xm6MBLdnaafZkGS4ZETtjHq1C5toQuHm7Y

**LTC**: LhbiUiXs8HBybqfNkmHFienvBxtoWaebsX

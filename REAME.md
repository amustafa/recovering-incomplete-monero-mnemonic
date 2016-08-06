# Recovering Incomplete Monero Wallet

Challenge by [this post](https://steemit.com/giveaway/@generalizethis/free-monero).

This was used to recover the funds from the steemit post linked above. The post reads: 

> During Christmas in 2014, I made Monero wallets as stocking stuffers. Each wallet had a 100 monero in it ($25 at the time, now about $180). I'm not the most detailed orientated person, so needless to say, I forgot a word on one of the wallets. I never gave it away--figuring it would make a nice prize for someone with free time and a dictionary hack.

##How to use
1. Enter your incomplete mnemonic into the conf.ini file and change any other settings to fit your nedes.
2. Run discover_mnemonics.py
3. Take the resulting discovered_seeds json object in the output folder and insert it into myMoneroKeyGeneratorScript.js
4. Open mymonero.com, open the developer tools ([in Chrome](https://developers.google.com/web/tools/chrome-devtools/?hl=en))
5. Copy the script with the seeds from myMoneroKeyGeneratorScript.js, paste it into the console, and run. Note: This might take a little bit.
6. Export the result into output/myMoneroAddressKeySets.json. In chrome, this can be done by right clicking the result, choosing "Save As", and then moving the file into the correct folder. Make sure it's the right name.
7. Run check_wallets.py
8. Any wallets with a non-zero transaction history with be printed to the console.

##Write Up
https://steemit.com/monero/@amustafa/recovering-an-incomplete-monero-mnemonic-wallet

###Donations

ETH: 0x1819c59cA38366A193C8fa02170F254fc9e942E0
BTC: 16zRJPnpXiGrNEN3L27nFfrqN239WGyKFb
XMR: 48TZ91tfy7w2LVcRape2dPfqchMgkjizm8Ukpr31cHRMgFHkM5DjwPxahs1zby5fQHeAXinhT4U4x8ygEK4zq1gq2A6G4Hy
DASH: Xm6MBLdnaafZkGS4ZETtjHq1C5toQuHm7Y
LTC: LhbiUiXs8HBybqfNkmHFienvBxtoWaebsX
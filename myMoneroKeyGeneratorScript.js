/*
MyMonero.com Helper

This is the script to convert the discovered seeds into actual addresses and keys that are using to view account
information for mymonero.com

Instead of recreating all the functions they use to generate the addresses:

- go to mymonero.com and click "Login"
- Enter the developer console by pressing CTRL+I or right clicking
- Copy the code below, replacing the seeds variable with the output in seeds.json
 */
var seeds = [];  // Replace the empty array with the json object in discovered_seeds.json
var addresses = [];
for (var seed in seeds){
    var addr = cnUtil.create_address(seeds[seed][1]);
    addresses.push([addr.public_addr, addr.view.sec]);
}

JSON.stringify(addresses);
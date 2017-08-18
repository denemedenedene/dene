## Scraping Guide

This guide describes scraping process for Coflight project. It defines input formats to be passed and output formats to be emitted.

### Input Format

Input format will be in CSV format and it will include the following in the written order

* Departure airport code
* Arrival airport code
* Departure date and time
* Return date and time
* One way/roundtrip info

Sample input format for one way trip

`IST,ADA,09282017-1530,,OW`

Sample input format for round trip

`IST,BEG,09282017-2250,09302017-0010,RT`

It is optional to query flights from dataset or from command line arguments.

Sample input via command line arguments format

`--depAirport IST --arrAirport ADA --depDate 09282017-2250 --OWRT OW --ss take`

This sample is to query a one way flight that
* Departures from Istanbul Ataturk Airport
* Arrives to Adana Sakirpasa Airport
* On 28 September 2017 - 22:50
* Saves screenshots while querying the flight.

### Output Format

Output format will be in CSV format and it will include the following in the written order

* Departure airport code
* Arrival airport code
* Departure date and time
* Return date and time
* Current date and time
* Ticket price
* Cookie info values

Sample output format of one way trip with cookies

`SAW,OTP,03272017-2300,,07052017-1247,127.99,WC`

Sample output format of round trip without cookies

`LHR,IST,20171230-0515,01052017-1500,07052017-1245,215.00,WOC`
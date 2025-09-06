Why?\
In California the majority of people drive everywhere fast and loud.  This means that there is even more emphasis on a quiet street to stay.  Most of the quiet streets Mark has personally lived on were 1 lane streets.  1 lane streets may be signed (best), or have just barely the width of two cars to pass further limiting the speed.  

quiet_streets.py performs three main steps:
1) From a given city search open street maps for quiet streets (one lane streets)
2) From a filtered zillow rental search for the same city extract all rental addresses
3) Find (if any) rentals that are on one lane streets

Gotchas:

Zillow street names are compressed in 'street-name suffix':
https://pe.usps.com/text/pub28/28apc_002.htm also
https://en.wikipedia.org/wiki/Street_suffix#United_States


street_name_suffix_us.csv is provided to uncompress
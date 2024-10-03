# Spider-Dork
A web crawler script for finding web servers from random ip ranges and searching for strings.

## Files
- spiderdork.py - Main crawler script
- dorks.txt - list of strings to search for on discovered web pages
- found_targets.tsv - Tab separated data collected on matching HTTP servers (address, title, page hash, country, region, city, ISP, dork matches)
- scanned_netblocks.txt - Log of /24 netblocks searched through previously
- unscanned_netblocks.txt - Log of /24 netblocks to be searched through


## Usage / Configuration
Run the crawler script as is:

`python spiderdork.py`

Or edit it first to change some settings:
- The `thread_count` variable can be edited on line 18. I have no frame of reference for what a good upper bound to this number should be.
- The `delay_between_threads` variable can be edited on line 19. This delay is applied after each thread is created.
- Update the if statement on line 33 to force the crawler to search for random or user-supplied netblocks.

## Example Results
![image](https://github.com/user-attachments/assets/02ccebbc-7a4e-4c08-904a-4d94582c0092)
![image](https://github.com/user-attachments/assets/a947ef84-6a50-4dc7-b3f2-c1026f24637d)



## Notes
Using [Shodan](https://www.shodan.io), you can find ip addresses to seed the web crawler with and potentially reveal similar devices. Gather a list of addresses using Shodan's available search filters, convert them to netblock abbreviations, then add those to the unscanned_netblocks.txt file with a new line between each. Netblocks can be abbreviated in the following way: `111.111.111.` which is equivalent to the CIDR notation `111.111.111.0/24`.

Some other public databases include [ZoomEye](https://www.zoomeye.hk/) and [Censys](https://search.censys.io/).

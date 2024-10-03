# Spider-Dork
A web crawler script for finding web servers from random ip ranges and searching for strings on them.

## Files
- spiderdork.py - Main crawler script
- dorks.txt - list of strings to search for on discovered web pages
- found_targets.tsv - Tab separated data collected on matching HTTP servers (address, title, page hash, country, region, city, ISP, dork matches)
- scanned_netblocks.txt - Log of /24 netblocks searched through previously
- unscanned_netblocks.txt - Log of /24 netblocks to be searched through


## Usage / Configuration
Run the crawler script as is:

`python spiderdork.py`

Or edit it first to change some settings. Update values under the `# Config Variables` comment to configure things.
- `thread_count` - sets the number of scanning threads to run. I have no frame of reference for what a good upper bound to this number should be.
- `delay_between_threads` - a delay in seconds applied after each thread is created.
- `search_mode` - a number (0-2) that determines what ip addresses the crawler will check
    - 0 : Mixed Mode - scan both randomly generated and user supplied/previously discovered netblocks in unscanned_netblocks.txt
    - 1 : Random Mode - scan randomly generated netblocks
    - 2 : File Mode - only scan netblocks listed in unscanned_netblocks.txt
- `extended_port_search` - sets the crawler to check for the default http port (80) or other commonly used http ports
    - False (default) - just checks if port 80 is open
    - True - checks on port 80, 8080, 443, and 8443

## Example Results
![image](https://github.com/user-attachments/assets/02ccebbc-7a4e-4c08-904a-4d94582c0092)
![image](https://github.com/user-attachments/assets/a947ef84-6a50-4dc7-b3f2-c1026f24637d)

## Notes
Using [Shodan](https://www.shodan.io), you can find ip addresses to seed the web crawler with and potentially reveal similar devices. Gather a list of addresses using Shodan's available search filters, convert them to netblock abbreviations, then add those to the unscanned_netblocks.txt file with a new line between each. Netblocks can be abbreviated in the following way: `111.111.111.` which is equivalent to the CIDR notation `111.111.111.0/24`.

Some other public databases include [ZoomEye](https://www.zoomeye.hk/) and [Censys](https://search.censys.io/).

## To Do
- Search for specfic paths on each host (e.g. /login.php, /admin.php, /phpmyadmin, /wp-login.php)
- Setup cli flags to avoid having to edit variables
- Create web viewer + api for uploading found targets to a database
- Create GUI client for configuring and starting a spiderdork job
    - potentially expand on this by adding settings for starting a scan at startup

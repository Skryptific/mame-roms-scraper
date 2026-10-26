# MAME Roms Scraper
Scrape the latest MAME ROMs from [mdk.cab](https://mdk.cab/) for the most recent supported MAME version (currently 0.274).

## Configuring games
This script makes use of the actual rom names, titles are not supported. Provide a list of game rom names in the ``games.txt`` file with every game on a new line. Also change the path ``mame_roms_dir`` within the script to wherever you want the roms to be downloaded to.

## Executing
At the time of making this script Python 3.12.9 was used. You can run the script by running ``py scraper.py`` in a terminal.

# March

So... This is a really easy script (SLOC <100) that I made in 15 minutes. It executes commands written in `~/.config/march.yml` or whatever your XDG_CONFIG_HOME variable is (it generates it on first launch). The script is quite useless, since it just saves me 30 seconds a week.

Usage examples:
    
    march upgrade,junk,cache  # or just `march -ujc`
    march --help  # to view available commands

Sample config entry:

    upgrade:
        short: u
        command: sudo pacman -Syu


## Instalation
Just clone the repository and add script to PATH. You may also make an alias. Do whatever you want


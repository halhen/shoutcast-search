# shoutcast-search

shoutcast-search searches the [shoutcast.com](http://www.shoutcast.com) radio stations from your command line. It is developed and tested on Linux, but since it is written in Python it may run, or at least should be easily portable, to other operating systems.

* [man page](http://www.k2h.se/code/shoutcast-search.man.txt)
* [latest release](http://www.k2h.se/code/dl/shoutcast-search-latest.tar.gz)
* [source repository](http://github.com/halhen/shoutcast-search/tree/master)

Distribution specific links:

* [archlinux AUR package](http://aur.archlinux.org/packages.php?ID=25366)

## Why shoutcast-search?  

* More powerful searches than at shoutcast.com.
* Handy - only a terminal window away.
* Automation.

## Automatic station selection
In default mode, shoutcast-search prints the URLs of the matching radio station, with one URL per line. These lines can be fed to a media player which will start playing the selected tracks. To play a random Top 500 station in VLC for example:

	$ shoutcast-search -n 1 -r | xargs vlc &

## Manual station selection
shoutcast-search can also be run in verbose mode: `shoutcast-search -v`. This is useful in two ways.

* To adjust the search  
  Getting the search can be a little tricky. shoutcast-search prints debug information about the search to help you get it right.

* To manually choose between the stations.  
  In verbose mode, the stations are listed with more information. This allows you to browse the hits and manually copy the URL for whatever station you want to listen to.

An example of verbose output:

     $ shoutcast-search --verbose --sort=rn2l --genre=ambient
     Search summary
     ------------------------------
     Keywords:
       Genres: ambient
      Playing:
     Stations:
      Bitrate:
    Listeners:
         Type:
        Order: by sorters
       Sorter: random order | top 2 | listeners desc
        Limit: 2
       Format: %s [%bkbps %t]\\n\\t%u\\n\\t%g, %l listeners\\n\\tNow playing: %p\\n
     	      
    Bluemars - Music for the Space Traveler [128kbps audio/mpeg]
            http://yp.shoutcast.com/sbin/tunein-station.pls?id=619161
            Ambient, 139 listeners
            Now playing: HIA and Biosphere - Midpoint
      
    X-Pulse 24/7 Ambient Radio [48kbps audio/mpeg]
            http://yp.shoutcast.com/sbin/tunein-station.pls?id=255046
            Ambient, 0 listeners
            Now playing: Zero One - Affirmative
    
    2 station(s) found.

The information for each station is listed below. Copy/paste or type the URL into your shoutcast-enabled music player to play the stream.

          <station name> [<bitrate> <MIME type>]
                  <URL>
                  <genre>, <nr> listeners
                  Now playing: <current track>

## Search criteria
You can perform free-text searches on three pieces of information

* Genre (`-g`)
* Song (`-p`)
* Station (`-s`)

The stations publish this information and they usually match pretty well. You can search for several criteria at once. All criteria must match for a station to be listed. For example searching `shoutcast-search -g synth -g pop -p "depeche mode"` lists all stations that have both the words "rock" *and* "pop" in their genre *and* is currently playing "depeche mode".

If you are searching for multi-word phrases, they can be enclosed in quotes. Searching for `"depeche mode"` requires the full string, including the single space, to be present. `depeche mode` requires depeche *and* mode to appear, the order does however not matter. Criteria are case-insensive, `"Depeche MODE"` and `"depeche mode"` give the same results.

You can also search for words or phrases without specifying which element to search. `shoutcast-search metallica` searches for stations with the word `metallica` in their genre, current song *or* station name. Any phrase that is not specified with an option, e.g. `-p`, will be used as a free text search. `shoutcast-search -g rock metallica` finds all stations with rock as their genre and metallica in any of genre, current song or station name. Use verbose mode to get your search right if you need to..

If you don't provide any criteria, shoutcast-search returns the current Top 500 stations.

*Note: due to caching at shoutcast.com, the currently played song per station is a bit delayed an not always correct.*

## Filters
soutcast-search can filter stations based on quality, number of listeners and codec required.

The bitrate and number of listeners filters require an expression to compare with. The form is `[=><]N` where `N` is a positive integer. `">128"` means more than 128, `"=128"` means exactly 128 and `"<128"` means less than 128. "Equals" is assumed if no operator is given, i.e. `"128"` is identical to `"=128"`.

*Note: you probably need to enclose the operation in quotes, depending on your shell.*

`-b` filter stations based on their bitrate in kbps. `-b ">127"` returns stations with 128 kbps or more bitrate.

`-l` filter stations based on how many listeners they currently have. More listeners usually mean better musical quality, even though it varies depending on genre. `-l ">100"` returns stations with more than a hundred listeners.

Filter stations based on which codec is required for playback. Valid options are `-t mpeg` for MP3 or `-t aacp` for aacPlus. By default, both codecs are included.

## Sorting
If you want more control over how the list is sorted, you can use the `--sort` option. You specify how you want the list sorted by entering letters and control characters in the proper order. Specifying sorters void the `-r` option.

Sorting  is  performed  in written order, for example `ln20r` sorts the retrieved list by number of listeners, trunkates it to twenty  stations and  then randomizes it, giving the top twenty stations randomly sorted. `^` is used to set sort order to ascending for `l` and `b`. The default  sort order is reset to descending for each new sorter.

The available sorting parameters are:

* `^` reverses order for the next variable. Sort order is reset to descending for each variable.
* `b` sorts by bitrate.
* `l` sorts by number of listeners.
* `r` randomizes list.
* `n` truncates the list with the number of elements that is given, for example `n10`.

## Format
You can specify how shoutcast-search prints the information for each matching stations using the `-f` option. The format is specified using a combination of free text and codes that are replaced with the applicable station information. For example, --format=`"Station name: %s"` prints `Station Name: <name>` for each station found. `%u` is the default format.

The following codes are available:
* %u - URL to the stream
* %g - stations genre
* %p - currently played song
* %s - station name
* %b - bitrate in kbps
* %l - number of listeners
* %t - MIME string describing codec
* %% - percent sign where the following character is one of the above
* \n - newline
* \t - tab

## Options
By default, shoutcast-search returns the found stations ordered by number of listeners. You can tell shoutcast-search to randomize the order by providing the `-r` option. This option is not applicable if `--sort` is specified.

You can tell also set a maximum number of stations to be listed by using the `-n` option. `-n 5` returns maximum five stations. Often, it is good to specify `-n 1` when piping the output to an audio player.

## Order of evaluation
shoutcast-search first matches the stations against the criteria; all criteria must match. Next, the results are filtered, again all parameters must match for a station to be listed. The remaining stations are sorted, or randomized based on options, and finally the number of results are limited, if applicable.

## Examples

* Find the most listened to station:

	$ shoutcast-search -n 1

* Find a random station with decent musical and technical quality playing chill:

	$ shoutcast-search -n 1 -r -l ">50" -b ">127" -g chill
	
* Get the five most listened to rock radio stations sorted by bitrate:

	$ shoutcast-search -g rock --sort=ln5b
	
* List the number of listeners and station name of the 50 most listened to stations:

	$ shoutcast-search -n 50 -f "%l %s"

## Automation
I've have a function in my .bashrc to quickly search and start a station with [mpg123](http://en.wikipedia.org/wiki/Mpg123):
	
	radio() {
		killall mpg123; shoutcast-search -n 1 -t mpeg -b ">63" --sort=ln10r $* | xargs mpg123 -q -@ &
	}

This function selects one random station out of the top ten most listened to playing mpeg at 64+ kbps. It also takes arguments to set new options, or change the ones set in the script, from the command line like below.

	$ radio chill

Something similar can easily be put in a shell script and connected to a media button on the keyboard.

## Media players
Check your audio players documentation on how to play shoutcast streams. Here follow a few examples.

* VLC

	$ shoutcast-search [...] | xargs vlc --one-instance &

* MPlayer

	$ killall mplayer; shoutcast-search [...] | xargs mplayer &
	
* mpg123

	$ killall mpg123; shoutcast-search -t mpeg [...] | xargs mpg123 -q -@ &

## More information
For a complete reference, see the [man-page](http://www.k2h.se/code/shoutcast-search.man.txt) (`man shoutcast-search`).

Written by Henrik Hallberg (<halhen@k2h.se>). Please send me an e-mail if you find bugs, have ideas for new features or just to let me know you use the application. I'd be happy to hear from you.

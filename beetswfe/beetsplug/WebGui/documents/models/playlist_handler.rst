.. Beetsplug WebGui documentation master file, created by
   sphinx-quickstart on Mon Nov  9 22:04:00 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Playlist_handler.py
============================================

How do .m3U-files work?

#EXTM3U - hey I'm a m3u-file
#EXTINF - contains the information about the name of the song which is saved. One #EXTINF for each Song is suggested. Each #EXTINF should include the name of the Song and the URL (or Path) of the File where it can be located.  
A m3u-file contains typically more than one #EXTINF 
To get more information about .m3u files see here [LINK]
The use of m3u-files to give the user the opportunity to export the m3u-files and use them for another application. 

Warum wird in jeder Methode das "given_directory" mitgegeben? Im endeffekt hat man es dadurch noch mehr 
parametrisiert und ermöglicht so den Tests entpsrechend einen anderen Folder anzugeben. 

.. warning::
	beetsWFE does just saves the beets Item-ID at the .m3u-file. So the Playlists will not work in other applications! 

.. automodule:: beetsplug.WebGui.models.playlist_handler
   :members:

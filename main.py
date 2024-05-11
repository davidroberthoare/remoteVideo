import vlc
from time import sleep
 
# creating vlc media player object
media = vlc.MediaPlayer("media/test1.mp4")
 
# start playing video
media.play()


sleep(10) # Or however long you expect it to take to open vlc
while media.is_playing():
     sleep(1)
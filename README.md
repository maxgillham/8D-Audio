# binary_audio  

The inspiration for this project came from a series of YouTube videos I was
shown, called [8D Audio](https://www.youtube.com/channel/UCrRpYEytIHGyDgNWO6VbHlQ/videos "Check it out!").  
Yeah, the name doesn't make a ton of sense, but anyways, I thought this was pretty neat. I think it would be cool to try and make a series of signal processing methods to make any song "8D Audio".

## Getting Started  
At this point, the only dependancies are [Librosa](https://librosa.github.io/librosa/index.html) and [Numpy](http://www.numpy.org/). I would reccomend configuring your enviorment using anaconda, you can download it [here](https://www.anaconda.com/download/).  

`audio_features.py` takes files in the first directory and saves them in the seccond.
* ./binary_audio/sample_audio
* ./binary_audio/sample_output  

I have added an example file, it is a youtube not copy right song.  You can play with what I have started by dropping a wav file in sample_audio, or use the exapmple, and running `audio_features.py`.  The result will be in sample_output.  To download another wav file to experiment with, you can use this likely illegal site, [Save Clip Bro](https://www.saveclipbro.com/).

## What needs to be done   
Currently, this only spreads the audio from left to right channel.  The other properties I have noticed in this format of audio conversion that need to be introduced are  

* Left and right channel swapping to match song breakpoints
* Audio elevation swapping 
* Dry reverb


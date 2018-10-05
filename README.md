# binary_audio  

The inspiration for this project came from a series of YouTube videos I was
shown, called [8D Audio](https://www.youtube.com/channel/UCrRpYEytIHGyDgNWO6VbHlQ/videos "Check it out!").  
Yeah, the name doesn't make a ton of sense, but anyways, I thought this was pretty neat. I think it would be cool to try and make a series of signal processing methods to make any song "8D Audio".

## Getting Started  
At this point, the only dependancy is [Librosa](https://librosa.github.io/librosa/index.html). You can download using pip,  
`pip install librosa`  
The python file assumes you have the following directories  
* ./binary_audio/sample_audio
* ./binary_audio/sample_output  

Once you have the enviorment configured, you can play with what I have started by dropping a wav file in sample_audio and running `audio_features.py`.  The result will be in sample_output.  To download an example wav file to experiment with, you can use this likely illegal site, [Save Clip Bro](https://www.saveclipbro.com/).

## What needs to be done   
Currently, this only spreads the audio from left to right channel.  The other properties I have noticed in this format of audio conversion that need to be introduced are  

* Left and right channel swapping to match song breakpoints (currently just out of phase sin wavs)
* Audio elevation swapping 
* Dry reverb


# Humanoidný robot NICO
workshop na sústredení OAI

## Postup inštalácie

Robota riadime v reálnom čase, čo Colab nie je schopný zabezpečiť. 
Je preto nevyhnutné nainštalovať si všetky potrebné knižnice lokálne.

Predpokladáme, že máte 64 bitový operačný systém, MS Windows 10, 11 alebo Linux Ubuntu.

Podporujeme Python 3.7 - 3.12 a cesty ako napríklad C:\Python39 and C:\Python39\Scripts sú v PATH

### Windows

Ak nemáte nainštalované Visual Studio 2019 alebo novšie, 
nainštalujte posledné Visual Studio Redistributables z
https://aka.ms/vs/17/release/vc_redist.x64.exe

pustime cmd 

ak nemate ešte nainstalovanú podporu vytvárania virtuánych mašín:

> \> pip install virtualenv virtualenvwrapper-win <br>

vytvoríme virtuálnu mašinu

> \> mkvirtualenv nico

nainštalujeme knižnice

> (nico)> pip install requests<br>
> (nico)> pip install PySimpleGUI-4-foss<br>
> (nico)> pip install opencv-contrib-python<br>
> (nico)> pip install chime<br>
> (nico)> pip install yourdfpy<br>
> (nico)> pip install "pyglet<2"

> (nico)> pip install ftfy<br>
> (nico)> pip install regex<br>
> (nico)> pip install pyttsx3

> (nico)> pip install torch torchvision (ak nemáme CUDA)

alebo

> (nico)> pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126  (ak máme napríklad CUDA 12.6 v c:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\)  

> (nico)> pip install transformers

> (nico)> pip install pyaudio<br>
> (nico)> pip install SpeechRecognition<br>
> (nico)> pip install openai-whisper


### Linux (Ubuntu)

> $ cd ~/ <br>
> $ git clone https://github.com/andylucny/nico.git <br>
> $ python3 -m venv virtual/nico <br>
> $ source virtual/nico/bin/activate <br>
> (nico)$ sudo apt-get install python3-tk 

> (nico)$ pip install requests  <br>
> (nico)$ pip install PySimpleGUI-4-foss <br>
> (nico)$ pip install opencv-contrib-python <br>
> (nico)$ pip install chime <br>
> (nico)$ pip install "pyglet<2" <br>
> (nico)$ pip install trimesh==3.11.2 <br>
> (nico)$ pip install yourdfpy

> (nico)$ pip install ftfy<br>
> (nico)$ pip install regex

> (nico)$ sudo apt install espeak<br>
> (nico)$ pip install pyttsx3

> (nico)> pip install torch torchvision (ak nemáme CUDA)

alebo

> (nico)> pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126  (ak máme CUDA 12.6)  

> (nico)> pip install torch torchvision (ak nemáme CUDA)

alebo

> (nico)> pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126  (ak máme napríklad CUDA 12.6 v c:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\)  

> (nico)> pip install transformers

> (nico)$ sudo apt install portaudio19-dev python3-pyaudio<br>
> (nico)$ pip install pyaudio<br>
> (nico)$ pip install SpeechRecognition<br>
> (nico)> pip install openai-whisper

## Použitie

### Windows

> \> workon nico <br>
> (nico)> python my.py

### Linux (Ubuntu)

> $ cd ~/ <br>
> $ source virtual/nico/bin/activate <br>
> $ cd nico/... <br>
> (nico)$ python3 my.py 

## Úloha

Navrhnite svoj vlastný projekt v simulátore a (v optimálnom prípade) vyskúšajte na robotovi.

# fretboard-mastery
Wasting my time building a tool that is supposedly helping me practice guitar instead of actually practicing.

## Building

```
pyinstaller main.spec
```

Re-creating the .spec file, usually not needed:
```
pyinstaller --ond --noconsole --windowed \
--add-data "sounds:sounds" \ 
main.py --hidden-import tkinter
```
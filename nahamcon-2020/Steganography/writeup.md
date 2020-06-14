# Scripting

## Ksteg (50)
This must be a typo.... it was kust one letter away!

https://github.com/lukechampine/jsteg
file was named luke.jpg

```
> .\jsteg-windows-amd64.exe
Usage: jsteg [command] [args]

Commands:
    jsteg hide in.jpg [FILE] [out.jpg]
    jsteg reveal in.jpg [FILE]

> .\jsteg-windows-amd64.exe reveal .\luke.jpg
flag{yeast_bit_steganography_oops_another_typo}
```

## Doh (50)
Doh! Stupid steganography...

```
> steghide --extract -p "" -sf doh.jpg
wrote extracted data to "flag.txt".
> cat flag.txt
JCTF{an_annoyed_grunt}
```

## Beep Boop (50)
That must be a really long phone number... right?

http://dialabc.com/sound/detect/index.html

46327402297754110981468069185383422945309689772058551073955248013949155635325

```
>>> val = 46327402297754110981468069185383422945309689772058551073955248013949155635325
>>> def int_to_str(n):
...     s = ''
...     while n > 0:
...         s = chr(n % 256) + s
...         n //= 256
...     return s
...
>>> int_to_str(val)
'flag{do_you_speak_the_beep_boop}'
```

## Snowflake
Frosty the Snowman is just made up of a lot of snowflakes. Which is the right one?



## My Apologies (75)
Prompt: Nothing witty to say here... just that I am sorry.

Twitter secret message
https://holloway.nz/steg/

## Dead Swap (100)
There is a flag in my swap!

## Walkman (100)
Do you hear the flag? Maybe if you walk through it one step at a time.

https://github.com/pavanchhatpar/wav-steg-py

```
> python3 wav-steg.py --recover --sound wazaaa.wav --output output.txt --nlsb 1 --bytes 100
> cat output.txt
flag{do_that_bit_again}
```


## Old School (125)
Did Dade Murphy do this?



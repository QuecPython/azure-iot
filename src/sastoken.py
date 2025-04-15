import utime
from base64 import b64encode, b64decode
from hashlib import sha256
from hmac import HMAC

def generate_sas_token(uri, key, policy_name, expiry=3600):
        #localtime returnes tuple with local RTC time
        ttl = utime.localtime()
        #mktime returnes 6 hours behind, so we have to add 6 hours + expiry
        t = utime.mktime(ttl) + (3600 * 6) + expiry  
        sign_key = "%s\n%d" % ((quote_plus(uri)), int(t))
        #print(sign_key)
        signature = b64encode(HMAC(b64decode(key), sign_key.encode('utf-8'), sha256).digest())
        rawtoken = {
            'sr' :  uri,
            'sig': signature,
            'se' : str(int(t))
        }

        if policy_name is not None:
            rawtoken['skn'] = policy_name

        return 'SharedAccessSignature ' + urlencode(rawtoken)
        
    
def quote(string, safe='/', encoding=None, errors=None):
    if isinstance(string, str):
        if not string:
            return string
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'strict'
        string = string.encode(encoding, errors)
    else:
        if encoding is not None:
            raise TypeError("quote() doesn't support 'encoding' for bytes")
        if errors is not None:
            raise TypeError("quote() doesn't support 'errors' for bytes")
    
    # Mapiraj specijalne karaktere u %XX formatu
    always_safe = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
    safe += always_safe

    result = []
    for char in string:
        if char in safe.encode():
            result.append(chr(char))
        else:
            result.append('%%%02X' % char)
    return ''.join(result)


def quote_plus(string, safe='', encoding=None, errors=None):
    if ((isinstance(string, str) and ' ' not in string) or
        (isinstance(string, bytes) and b' ' not in string)):
        return quote(string, safe, encoding, errors)

    if isinstance(safe, str):
        space = ' '
    else:
        space = b' '

    string = quote(string, safe + space, encoding, errors)
    return string.replace(' ', '+')

def urlencode( query, doseq=False, safe='', encoding=None, errors=None):
    if hasattr(query, "items"):
        query = query.items()
    else:
        try:
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError
        except TypeError as err:
            raise TypeError("not a valid non-string sequence or mapping object") from err

    l = []
    if not doseq:
        for k, v in query:
            if isinstance(k, bytes):
                k = quote_plus(k, safe)
            else:
                k = quote_plus(str(k), safe, encoding, errors)

            if isinstance(v, bytes):
                v = quote_plus(v, safe)
            else:
                v = quote_plus(str(v), safe, encoding, errors)
            l.append(k + '=' + v)
    else:
        for k, v in query:
            if isinstance(k, bytes):
                k = quote_plus(k, safe)
            else:
                k = self.quote_plus(str(k), safe, encoding, errors)

            if isinstance(v, bytes):
                v = quote_plus(v, safe)
                l.append(k + '=' + v)
            elif isinstance(v, str):
                v = quote_plus(v, safe, encoding, errors)
                l.append(k + '=' + v)
            else:
                try:
                    x = len(v)
                except TypeError:
                    v = quote_plus(str(v), safe, encoding, errors)
                    l.append(k + '=' + v)
                else:
                    for elt in v:
                        if isinstance(elt, bytes):
                            elt = quote_plus(elt, safe)
                        else:
                            elt = quote_plus(str(elt), safe, encoding, errors)
                        l.append(k + '=' + elt)
    return '&'.join(l)


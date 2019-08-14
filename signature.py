"""HTTP signature checking."""

import hashlib
import hmac
import base64
import re

from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

class SignatureException(Exception):
    """HTTP signature is not valid"""


def _get_digest(req):
    digest = req.headers['Digest']
    requesthash = re.match('^SHA-256=(.+)', digest)[1]
    datahash = base64.b64encode(hashlib.sha256(req.data).digest()).decode()
    if requesthash != datahash:
        raise SignatureException("Message digest hashes don't match")
    return "SHA-256=" + datahash


def _parse_signature_header(signature_header):
    matches = re.findall('(keyId|algorithm|headers|signature)="([^"]*)",?', signature_header)
    return {m[0]: m[1] for m in matches}

def _get_sign_string(req, headers, host, pathandquery):
    values = {
        '(request-target)': "{} {}".format(req.method.lower(), pathandquery),
        'host': host,
        'date': req.headers['Date'],
        'content-type': req.headers['Content-Type'],
        'content-length': req.headers['Content-Length'],
        'digest': _get_digest(req)
    }

    sign_string = "\n".join([
        "{}: {}".format(header, values[header]) for header in headers
    ])

    return sign_string

def validate_signature(req, keys, host=None, pathandquery=None, max_allowed_time=60):
    """Validated HTTP signature using request."""
    
    if host is None:
        host = req.headers['Host']

    if pathandquery is None:
        pathandquery = req.full_path.rstrip('?')

    sig_params = _parse_signature_header(req.headers['Signature'])

    date = parsedate_to_datetime(req.headers['Date'])
    now = datetime.now(timezone.utc)
    if (date - now).total_seconds() > max_allowed_time:
        raise SignatureException("Query too old: {}".format(date))

    sign_string = _get_sign_string(req, sig_params['headers'].split(' '), host, pathandquery)

    key = keys.get(sig_params['keyId'])
    if key is None:
        raise SignatureException("Key with ID {} does not exist".format(sig_params['keyId']))
    if sig_params['algorithm'] != "hmac-sha256":
        raise SignatureException("Unsupported algorithm: {}".format(sig_params['algorithm']))

    hmac_sha256 = hmac.new(base64.b64decode(key), sign_string.encode(), 'sha256')
    sig_hash = base64.b64encode(hmac_sha256.digest()).decode()

    if sig_hash != sig_params['signature']:
        raise SignatureException(
            "Signature mismatch, computed {}, posted {}".format(sig_hash, sig_params['signature']))

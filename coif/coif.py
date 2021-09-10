'''
coif.py: cover image finder

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2021 by the California Institute of Technology.  This code is
open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

from collections import deque
from commonpy.string_utils import antiformat
from commonpy.network_utils import net, ServiceFailure
import json

if __debug__:
    from sidetrack import log


# Exported functions.
# .............................................................................

def cover_image(identifier, kind = 'isbn', size = 'S', cc_login = ()):
    '''Contact various services and return an image (as binary data).

    The required argument "identifier" must be a book identifier such as an
    ISBN.

    The optional argument "kind" is used to identify the kind of identifier
    provided.  Recognized values are 'isbn', 'lccn', 'olid', 'oclc', and
    'coverid'.  The default is 'isbn'.

    The image data returned is in JPEG format.  None of the services return
    image size information, so there is no way to know how large an image
    will be before attempting to fetch it.

    Optional parameter "size" can be one of the letters "S", "M", "L", to
    indicate a preference for a small, medium, or large image, respectively.
    The default is "S".  If a given size is not found, smaller sizes will be
    attempted automatically.

    Optional parameters "cc_user" and "cc_password" are a user id and password
    to be used with the Content Cafe 2 service offered by Baker & Taylor, if
    you have a login.  If not provided, cover_image(...) will not attempt to
    contact Content Cafe.
    '''

    if not identifier:
        raise ValueError(f'Invalid identifier "{identifier}"')
    if not kind:                        # Guard against kind = ''.
        kind = 'isbn'
    kind = kind.lower()                 # Normalize the value.
    if kind not in ['isbn', 'lccn', 'olid', 'oclc', 'coverid']:
        raise ValueError(f'Unrecognized identifier kind "{kind}"')
    if not size:
        size = 'S'                      # Guard against size = ''.
    size = size.upper()
    if size not in ['S', 'M', 'L']:
        raise ValueError(f'Unrecognized size "{size}"')
    cc_login = cc_login or ()

    services = []
    if kind == 'isbn' and cc_login and len(cc_login) == 2:
        services.append(cover_image_from_cc)
    services.append(cover_image_from_ol)
    if kind == 'isbn':
        services.append(cover_image_from_google)

    sizes_to_try = deque('S')
    if size == 'M':
        sizes_to_try.extendleft('M')
    if size == 'L':
        sizes_to_try.extendleft('L')
    for image_size in sizes_to_try:
        for service in services:
            url, data = service(identifier, kind, image_size, cc_login)
            if url:
                return url, data
    return None, None


def cover_image_from_cc(isbn, kind, size, login):
    '''Given an ISBN, return a URL for an cover image.'''
    if kind != 'isbn':
        return None, None
    if not isbn:
        return None, None
    user, password = login
    url = ('https://contentcafe2.btol.com/ContentCafe/jacket.aspx?'
           + f'UserID={user}&Password={password}&Return=T&Type={size}'
           + f'&Value={isbn}')
    (response, error) = net('get', url)
    if not error and response.status_code == 200:
        # BTOL responses use Transfer-Encoding: chunked and don't provide
        # a Content-Length header, so there's no way to know the size of
        # the image without downloading all of it.
        # If BTOL doesn't find a value, it returns a small default image.
        if len(response.content) > 2800:
            if __debug__: log(f'got image from Content Cafe for {isbn}')
            return url, response.content
    if __debug__: log('Content Cafe did not return an image for {isbn}')
    return None, None


def cover_image_from_ol(identifier, kind, size, login):
    '''Given an ID, return a URL for an cover image thumbnail.'''
    if kind != 'isbn' or not identifier:
        return None, None
    url = f'http://covers.openlibrary.org/b/{kind}/{identifier}-{size}.jpg?default=false'
    (response, error) = net('get', url)
    if not error:
        if response.status_code == 404:
            if __debug__: log(f'OL returned 404 for {size} image for {identifier}')
            return None, None
        elif response.status_code == 200:
            if __debug__: log(f'got image from OL for {identifier}')
            return url, response.content
    if __debug__: log(f'OL did not return an image for {identifier}')
    return None, None


def cover_image_from_google(isbn, kind, size, login):
    '''Given an ISBN, return a URL for an cover image thumbnail.'''
    if not isbn or kind != 'isbn':
        return None, None
    url = f'https://www.googleapis.com/books/v1/volumes?q={isbn}'
    (response, error) = net('get', url)
    if error:
        if __debug__: log(f'got error trying to get image from Google: {antiformat(error)}')
        return None, None
    # Google returns JSON, making it easier to get data directly.
    json_dict = json.loads(response.content.decode())
    if 'items' not in json_dict or 'volumeInfo' not in json_dict['items'][0]:
        if __debug__: log(f'got incomplete data from Google for {isbn}')
        return None, None
    info = json_dict['items'][0]['volumeInfo']
    if 'imageLinks' in info and 'thumbnail' in info['imageLinks']:
        if __debug__: log(f'go image URL from Google for {isbn}')
        image_url = info['imageLinks']['thumbnail']
        (google_response, google_error) = net('get', image_url)
        if not google_error:
            return image_url, google_response.content
        else:
            return None, None
    if __debug__: log(f'Google did not return a URL for {isbn}')
    return None, None

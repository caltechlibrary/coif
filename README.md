# Coif<img width="11%" align="right" src="https://github.com/caltechlibrary/coif/raw/main/.graphics/coif-icon.png">

Coif (_**Co**ver **i**mage **f**inder_) is a Python&nbsp;3 module for contacting multiple services to look for a book jacket image given an identifier such as an ISBN.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/coif.svg?style=flat-square&color=b44e88)](https://github.com/caltechlibrary/coif/releases)
[![DOI](https://data.caltech.edu/badge/201106666.svg)](https://data.caltech.edu/badge/latestdoi/201106666)


## Table of contents

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#authors-and-acknowledgments)


## Introduction

In a variety of situations involving library software systems, it's useful to show a small image of a book's cover or jacket. Coif (_**Co**ver **i**mage **f**inder_) is a simple Python&nbsp;3 library that looks for cover images using multiple network services. When it finds one, Coif returns the image in [JPEG](https://en.wikipedia.org/wiki/JPEG) format.

Coif is most similar to [bookcovers](https://github.com/e-e-e/bookcovers), a JavaScript library that performs federated search for book cover images. A Python package similar to Coif is [booker](https://github.com/krdyke/booker), but that one is limited to searching Google Books.


## Installation

The instructions below assume you have a Python interpreter installed on your computer; if that's not the case, please first [install Python version 3](INSTALL-Python3.md) and familiarize yourself with running Python programs on your system.

On **Linux**, **macOS**, and **Windows** operating systems, you should be able to install `coif` with [`pip`](https://pip.pypa.io/en/stable/installing/).  To install `coif` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```
python3 -m pip install coif
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `coif` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/caltechlibrary/coif.git
```


## Usage

Coif currently offers only an application programming interface (API); it does not offer a command-line interface. The main interface point is the function `cover_image(...)`. Here is a simple demonstration of using it:

```python
from coif import cover_image

(url, image) = cover_image('9781479837243')
if image:
    with open('image.jpg', 'wb') as image_file:
        image_file.write(image)
else:
    print('Unable to find image')
```

As illustrated above, `cover_image` returns **two** values: a URL, and a JPEG image in binary form (if a cover image is found).


### Arguments to `cover_image`

The function takes one required argument, an identifier (preferably an [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number), but possibly other kinds of identifiers), and additional optional arguments. In more detail, the possible arguments are:

* `identifier` (required): an ISBN, OCLC id, LCCN id, OLID and or Open Library [Cover ID](https://openlibrary.org/dev/docs/api/covers). Note that only Open Library accepts anything other than ISBN, so your best bet for finding a cover image is to use an ISBN. Conversely, if you provide anything other than an ISBN, `cover_image` will only contact Open Library.
* `kind` (optional): the kind of identifier given as the first argument. Recognized values are `isbn`, `lccn`, `olid`, `oclc`, and `coverid`. The default is `isbn`.
* `size` (optional): one of the letters `S`, `M`, or `L`, to indicate a preference for small, medium, or large images, respectively. Some cover images may exist in one size and not another, and there is no way to know in advance which size may be available from a service without actually downloading the image. If a `size` is provided, `cover_image` will ask for that size _and smaller_; for example, if you call it with `size = 'M'`, it will try to find `M` first and if none exists, it will try `S`. By default, it wil _only_ try `S`. If you want to get the largest image you can find, call it with `size = 'L'`.
* `cc_login` (optional): one of the best services for finding cover images is [Content Cafè 2](http://www.baker-taylor.com/pdfs/content_cafe.pdf) from Baker & Talor, but it requires an account. If you have a user id and password with their service, provide the credentials as a tuple of values `("user", "password")` to the optional argument `cc_login`.


### Why `cover_image` always returns an image

A frustrating aspect of many of the services is that they provide no way to simply ask whether an image exists. If the services do not have an image for a given identifier, most return a small placeholder image (often containing rendered text to the effect of "no cover found") instead of returning a failure code of some kind. Consequently, `cover_image` must always download images and test them against some size thresholds to determine if it got a placeholder or an actual cover image. This is the reason why the return values from `cover_image` are both a URL and an image: it has already downloaded the image, so it may as well return it, to save the caller the trouble of downloading the image a second time.


## Known issues and limitations

Although the [Open Library Covers API](https://openlibrary.org/dev/docs/api/covers) accepts multiple types of identifiers such as an ISBN, OCLC, LCCN, and more, other services only accept ISBNs. Thus, while you can pass any of these types of identifiers to Coif, if what you use is _not_ an ISBN, then Coif will only contact the Open Library's service.


## Getting help

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/coif/issues) for this repository.


## Contributing

We would be happy to receive your help and participation with enhancing Coif!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


## License

Software produced by the Caltech Library is Copyright © 2021 California Institute of Technology.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


## Authors and history

In this section, list the authors and contributors to your software project.  Adding additional notes here about the history of the project can make it more interesting and compelling.  This is also a place where you can acknowledge other contributions to the work and the use of other people's software or tools.


## Acknowledgments

This work was funded by the California Institute of Technology Library.

The [vector artwork](https://thenounproject.com/term/hair/1710638/) of a man's coiffure, used as the icon for this project, was created by [sarah](https://thenounproject.com/saifulbachrisitubondo/) from the Noun Project.  It is licensed under the Creative Commons [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/) license. I edited the logo in [Boxy SVG](https://boxy-svg.com), a native SVG editor for macOS to change the icon color to the orange used by Caltech in their logo.

<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src="https://raw.githubusercontent.com/caltechlibrary/coif/main/.graphics/caltech-round.png">
  </a>
</div>

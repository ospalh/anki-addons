# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""A list of audio downloaders.

They are intended for use with the Anki2 audiodownload add-on, but can
possibly be used alone. For each downloader in the list, setting its
language variable and then calling download_files(text, base, ruby,
split) downloads audio files to temp files and fills its
downloads_list with the file names.

When PyQt4 is installed, this downolads the site icon (favicon) for
each site first.
"""

from .beolingus import BeolingusDownloader
from .collins_french import CollinsFrenchDownloader
from .collins_german import CollinsGermanDownloader
from .collins_italian import CollinsItalianDownloader
from .collins_spanish import CollinsSpanishDownloader
from .den_danske_ordbog import DenDanskeOrdbogDownloader
from .duden import DudenDownloader
from .howjsay import HowJSayDownloader
from .islex import IslexDownloader
from .japanesepod import JapanesepodDownloader
from .leo import LeoDownloader
from .lexin import LexinDownloader
from .macmillan_american import MacmillanAmericanDownloader
from .macmillan_british import MacmillanBritishDownloader
from .mw import MerriamWebsterDownloader
from .oald import OaldDownloader
from .wiktionary import WiktionaryDownloader


downloaders = [
    JapanesepodDownloader(),
    WiktionaryDownloader(),
    LeoDownloader(),
    LexinDownloader(),
    MerriamWebsterDownloader(),
    # MacmillanAmericanDownloader(),
    MacmillanBritishDownloader(),
    OaldDownloader(),
    DudenDownloader(),
    DenDanskeOrdbogDownloader(),
    HowJSayDownloader(),
    IslexDownloader(),
    CollinsFrenchDownloader(),
    CollinsGermanDownloader(),
    CollinsItalianDownloader(),
    CollinsSpanishDownloader(),
    BeolingusDownloader(),
]
# For each word field, these downloader sites are tried in the order
# they appear here. Lines starting with a “#” are not tried. Change
# the order, or which lines get the “#”, to taste


# # For testing. See also the “Uncomment this …” bit in ..download
# downloaders = [
#     DictNNDownloader(),
# ]

__all__ = ['downloaders']

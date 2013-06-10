# -*- mode: python ; coding: utf-8 -*-

# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Dictionary lookup support for my favorite dictionaries
#
# © 2011–2013 Roland Sieker <ospalh@gmail.com>
#
# Losely based on lookup.py from the JapaneseSupport plugin
# © Damien Elmes <anki@ichi2.net>

u"""Add a menu to Anki2 to look up words in a few more dictionaries. """


import urllib
from aqt import mw
from aqt.qt import QDesktopServices, QUrl, QMenu, QAction, SIGNAL
from aqt.utils import tooltip
from aqt.webview import QWebPage


### Configure in this block
### Hier Konfiguration

## Show Japanese dictonaries
## Japanisch-Wörterbücher anzeigen
show_japanese = True
#show_japanese = False

## There is nothing wrong with the Saiga lookup. It’s just that i
## don’t like it as much as the Kanji-Lexikon. So make it easy to
## switch that on or off.
show_saiga = True
# show_saiga = False

## These two, "expression_fields" and "meaning_fields", are the "field
## name lists" refered to in the popup error message.

## List of fields to use for look-up of the foreign language. The
## first one where a text is found will be used.
## Liste mit Feldern, in denen der Fremdsprachentext gesucht wird. Das
## erste, in dem ein Text gefunden wird, wird benutzt.
expression_fields = [u'Expression', u'Kanji', u'Reading', u'Back']
#expression_fields = [u'Front']

## List of fields to use for the German text for Wadoku look-up. The
## first one where a text is found will be used.
## Liste mit Feldern für den deutschen Text, der bei Wadoku
## nachgeschlagen wird. Das erste, in dem ein Text gefunden wird, wird
## benutzt.
meaning_fields = [u'Meaning', u'Deutsch', u'German', u'Front']
#meaning_fields = [u'Back']


### End configuration block
### Ende Konfiguration

__version__ = "2.0.0"


# A few general-purpose helper functions.


def get_selection():
    "Get the selected text."
    # lazily acquire selection by copying it into clipboard
    mw.web.triggerPageAction(QWebPage.Copy)
    text = mw.app.clipboard().mimeData().text()
    text = u' '.join(text.split())
    if not text:
        raise ValueError(u'Empty selection.')
    return text


def is_han_character(uchar):
    u"""Return True if uchar is a unifed CJK ideograph/han character.

    Return True if uchar is a unifed CJK ideograph/han character.
    N.B. we only check the standard range in the BMP.
    """
    if uchar >= u'\u4e00' and uchar <= u'\u9fff':
        # The code from the JapaneseSupport plugin compares
        # ord(character) to a number. We compare one character
        # with another. Don't know which method is
        # 'better'. (And we skip u'\u2e00' to u'\u4dff', i
        # guess the kana are somwhere in there.)
        return True
    return False


def get_han_characters(text):
    u"""Return only the kanji/hanzi from text."""
    ret = u''
    # Maybe we got utf-8
    try:
        utext = unicode(text, 'utf-8')
    except TypeError:
        # Hope text is already unicode. If we put in
        # a number or something, we'll fail in one of the
        # next lines. EAFP
        utext = text
    for c in utext:
        if is_han_character(c):
            ret += c
    return ret


def get_first_han_character(text):
    u"""Return the first character from text that is a kani/hanzi."""
    # Maybe we got utf-8
    try:
        utext = unicode(text, 'utf-8')
    except TypeError:
        # As above, hope this is unicode (EAFP).
        utext = text
    for c in utext:
        if is_han_character(c):
            return c
    return u''


def get_text_from_fields(fields):
    u"""Return the content of fields of the current note."""
    text = None
    for field in fields:
        try:
            #text = mw.currentCard.fact[field]
            text = mw.reviewer.card.note()[field]
        except KeyError:
            continue
        if len(text):
            return text
    if not text:
        raise ValueError("No field found for lookup. " +
                         "Consider changing the field name lists " +
                         "in the plugin source.")


# Now the lookup functions. Now strictly sorted by dictionary.


def lookup_wadoku(field_list):
    "Look up text with Wadoku (German-Japanese)."
    if field_list:
        text = get_text_from_fields(field_list)
    else:
        text = get_selection()
    if len(text) == 0:
        raise ValueError(u"Kein Text zum nachschlagen.")
    base_url = "http://www.wadoku.de/wadoku/search/"
    url = base_url + urllib.quote(text.encode("utf-8"))
    qurl = QUrl()
    qurl.setEncodedUrl(url)
    QDesktopServices.openUrl(qurl)


def on_lookup_wadoku_expression():
    u"""Wrapper to look up the expression at Wadoku and catch value errors."""
    try:
        lookup_wadoku(expression_fields)
    except ValueError as ve:
        tooltip(str(ve))
    except AttributeError:
        tooltip(u'Error during lookup. (No note?)')


def on_lookup_wadoku_meaning():
    u"""Wrapper to look up the expression at Wadoku and catch value errors."""
    try:
        lookup_wadoku(meaning_fields)
    except ValueError as ve:
        tooltip(str(ve))
    except AttributeError:
        tooltip(u'Error during lookup. (No note?)')


def on_lookup_wadoku_selection():
    u"""Wrapper to look up the expression at Wadoku and catch value errors."""
    try:
        # Empty list (or possibly 'None')  means selection
        lookup_wadoku([])
    except ValueError as ve:
        tooltip(str(ve))


def lookup_saiga(field_list):
    """Look up the first kanji in text on Saiga."""
    # I don’t really use this dictionary any more. Feel free to
    # add it to your menu again.
    if field_list:
        kanji = get_text_from_fields(field_list)
    else:
        kanji = get_selection()
    kanji = get_first_han_character(kanji)
    if len(kanji) == 0:
        raise ValueError("No kanji found.")
    new_text = urllib.quote(kanji.encode("utf-8"))
    url = ("http://www.saiga-jp.com/cgi-bin/dic.cgi?m=search&sc=0&f=0&j=" +
           new_text + "&g=&e=&s=&rt=0&start=1")
    qurl = QUrl()
    qurl.setEncodedUrl(url)
    QDesktopServices.openUrl(qurl)


def on_lookup_saiga_expression():
    u"""
    Wrapper to look up at saiga.

    Wrapper to look up the first kanji from the expression at saiga and
    catch value errors.
    """
    try:
        lookup_saiga(expression_fields)
    except ValueError as ve:
        tooltip(str(ve))
    except AttributeError:
        tooltip(u'Error during lookup. (No note?)')


def on_lookup_saiga_selection():
    u"""
    Wrapper to look up at saiga.

    Wrapper to look up the first kanji from the selection at saiga and
    catch value errors.
    """
    try:
        lookup_saiga([])
    except ValueError as ve:
        tooltip(str(ve))


def lookup_kanjilexikon(field_list):
    """Look up the kanji in text on Kanji-Lexikon."""
    if field_list:
        kanji = get_text_from_fields(field_list)
    else:
        kanji = get_selection()
    kanji = get_han_characters(kanji)
    if len(kanji) == 0:
        raise ValueError("No kanji found.")
    new_text = urllib.quote(kanji.encode("utf-8"))
    url = ("http://lingweb.eva.mpg.de/kanji/index.html?kanji=" + new_text)
    qurl = QUrl()
    qurl.setEncodedUrl(url)
    QDesktopServices.openUrl(qurl)


def on_lookup_kl_expression():
    u"""
    Wrapper for lookup at Kanji-Lexikon.

    Wrapper to look up the expression at Kanjilexikon and catch value
    errors.
    """
    try:
        lookup_kanjilexikon(expression_fields)
    except ValueError as ve:
        tooltip(str(ve))
    except AttributeError:
        tooltip(u'Error during lookup. (No note?)')


def on_lookup_kl_selection():
    u"""
    Wrapper for lookup at Kanji-Lexikon.

    Wrapper to look up the selection at Kanjilexikon and catch value
    errors.
    """
    try:
        lookup_kanjilexikon([])
    except ValueError as ve:
        tooltip(str(ve))


def lookup_forvo(field_list):
    "Look up pronunciation on forvo."
    if field_list:
        text = get_text_from_fields(field_list)
    else:
        text = get_selection()
    if len(text) == 0:
        raise ValueError(u"No text to look up.")
    new_text = urllib.quote(text.encode("utf-8"))
    url = ("http://de.forvo.com/search/" + new_text)
    qurl = QUrl()
    qurl.setEncodedUrl(url)
    QDesktopServices.openUrl(qurl)


def on_lookup_forvo_expression():
    u"""Wrapper to look up the expression at Forvo and catch value errors."""
    try:
        lookup_forvo(expression_fields)
    except ValueError as ve:
        tooltip(str(ve))
    except AttributeError:
        tooltip(u'Error during lookup. (No note?)')


def on_lookup_forvo_selection():
    u"""Wrapper to look up the selection at Forvo and catch value errors."""
    try:
        lookup_forvo([])
    except ValueError as ve:
        tooltip(str(ve))


def create_menu():
    u"""Set up the menu."""
    mn = QMenu()
    mn.setTitle("Nachschlagen")
    mw.form.menuTools.addAction(mn.menuAction())
    #
    mw.form.menu_nachschlagen = mn
    # add actions
    if show_japanese:
        # Maybe not show the Japanese actions.
        wae = QAction(mw)
        wae.setText("Japanisch bei Wadoku")
        # wae.setShortcut("Ctrl+4")
        mn.addAction(wae)
        mw.connect(wae, SIGNAL("triggered()"), on_lookup_wadoku_expression)
        wam = QAction(mw)
        wam.setText("Deutsch bei Wadoku")
        # wam.setShortcut("Ctrl+2")
        mn.addAction(wam)
        mw.connect(wam, SIGNAL("triggered()"), on_lookup_wadoku_meaning)
        was = QAction(mw)
        was.setText("Auswahl bei Wadoku")
        mn.addAction(was)
        mw.connect(was, SIGNAL("triggered()"), on_lookup_wadoku_selection)

        if show_saiga:
            # Personal taste: i like the Kanjilexikon better than the
            # Saiga look up. So i like this switched off.
            sae = QAction(mw)
            sae.setText("Kanji bei Saiga")
            #sae.setShortcut("Ctrl+4")
            mn.addAction(sae)
            mw.connect(sae, SIGNAL("triggered()"), on_lookup_saiga_expression)
            sas = QAction(mw)
            sas.setText("Kanjiauswahl bei Saiga")
            mn.addAction(sas)
            mw.connect(sas, SIGNAL("triggered()"), on_lookup_saiga_selection)

        kle = QAction(mw)
        kle.setText("Kanji bei Kanji-Lexikon")
        # kle.setShortcut("Ctrl+4")
        mn.addAction(kle)
        mw.connect(kle, SIGNAL("triggered()"), on_lookup_kl_expression)
        kls = QAction(mw)
        kls.setText("Kanjiauswahl bei Kanji-Lexikon")
        mn.addAction(kls)
        mw.connect(kls, SIGNAL("triggered()"), on_lookup_kl_selection)
    # Show these always.
    fae = QAction(mw)
    fae.setText("Ausdruck bei Forvo")
    # fae.setShortcut("Ctrl+4")
    mn.addAction(fae)
    mw.connect(fae, SIGNAL("triggered()"), on_lookup_forvo_expression)
    fas = QAction(mw)
    fas.setText("Auswahl bei Forvo")
    mn.addAction(fas)
    mw.connect(fas, SIGNAL("triggered()"), on_lookup_forvo_selection)


# Looks like there isn’t an easy way to switch the menus on or of (at
# the moment).

#def disable_nachschlagen():
#    mw.form.menu_nachschlagen.setEnabled(False)

#def enableLookupMenu():
#    mw.form.menu_nachschlagen.setEnabled(True)

#def initMenus():
#    addHook('disableCardMenuItems', disable_nachschlagen)
#    addHook('enableCardMenuItems', enable_nachschlagen)
#    createMenu()


create_menu()

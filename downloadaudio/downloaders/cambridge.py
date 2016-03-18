import urllib

from .downloader import AudioDownloader
from ..download_entry import DownloadEntry


class CambridgeDownloader(AudioDownloader):
    """Download audio from Cambridge Dictionary."""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.icon_url = 'http://dictionary.cambridge.org'
        self.sound_class = None
        self.extras = {}  # Set in the derived classes.

    def download_files(self, field_data):
        """
        Get pronunciations of a word from Cambridge Dictionary.

        Look up a English word at dictionary.cambridge.org, look for
        pronunciations in the page and get audio files for those.

        """
        self.downloads_list = []
        if not self.language.lower().startswith('en'):
            return
        if not field_data.word:
            return
        if field_data.split:
            return
        word = field_data.word.replace("'", "-")
        self.maybe_get_icon()
        word_soup = self.get_soup_from_url(
            self.url + urllib.quote(word.encode('utf-8')))
        sounds = word_soup.findAll(True, {'class': self.sound_class})
        for sound_tag in sounds:
            audio_url = sound_tag.get('data-src-mp3')
            if audio_url:
                file_path = self.get_tempfile_from_url(audio_url)
                extras = self.extras
                self.downloads_list.append(
                    DownloadEntry(field_data, file_path, extras, self.site_icon))
                break

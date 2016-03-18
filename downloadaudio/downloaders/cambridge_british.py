"""
Download British pronunciations from  Cambridge Dictionary.
"""

from .cambridge import CambridgeDownloader


class CambridgeBritishDownloader(CambridgeDownloader):
    """Download British audio from Cambridge Dictionary."""
    def __init__(self):
        CambridgeDownloader.__init__(self)
        self.url = 'http://dictionary.cambridge.org/dictionary/english/'
        self.sound_class = 'sound audio_play_button pron-icon uk'
        self.extras = dict(Source="Cambridge", Variant="British")

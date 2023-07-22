
import matplotlib.pyplot as plt
from pyannote.core import Annotation, Timeline, Segment
from pyannote.metrics.base import BaseMetric
from pyannote.metrics.errors.identification import IdentificationErrorAnalysis
import copy
from pyannote.audio import Pipeline


class Transcript(Annotation):
    """
    Transcript extends the pyannote.metrics.Annotation class by adding support for
    storing the spoken text and language label alongside each annotated segment.
    """

    def __init__(self, uri=None, modality=None):
        super().__init__(uri=uri, modality=modality)
        self.transcript = dict()
        self.language_tags = dict()

    def __setitem__(self, segment, value):
        if isinstance(value, tuple) and len(value) == 3:
            super().__setitem__(segment, value[0])
            self.transcript[segment] = value[1]
            self.language_tags[segment] = value[2]
        else:
            raise ValueError(
                "Value must be a tuple with length 3: (label, text, language_tag)"
            )

    def get_text(self, segment):
        return self.transcript.get(segment, None)

    def get_language(self, segment):
        return self.language_tags.get(segment, None)



""" a = Transcript()
a[Segment(0, 1)] = ('A', "Hello world", "EN")

# To retrieve the text for a segment
text = a.get_text(Segment(0, 1))
print(text)  # Outputs: "Hello world"

# To retrieve the language tag for a segment
language = a.get_language(Segment(0, 1))
print(language)  # Outputs: "EN"
 """
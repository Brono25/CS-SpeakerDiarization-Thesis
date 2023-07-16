import matplotlib.pyplot as plt
from pyannote.core import Annotation, Segment, Timeline, notebook
from pyannote.metrics.errors.identification import IdentificationErrorAnalysis
import utils 
import metrics as met


#######################################
#           CONFUSION ERRORS
######################################
# speaker A English to Spanish caused confusion
CE_1 = utils.LanguageErrorAnalysis(uri="Test")
CE_1.ref_annotation[Segment(0, 4)] = "A"
CE_1.ref_annotation[Segment(3, 4)] = "B"
CE_1.hyp_annotation[Segment(0, 1)] = "A"
CE_1.hyp_annotation[Segment(1, 3)] = "B"
CE_1.hyp_annotation[Segment(3, 4)] = "A"
CE_1.lang_segments[Segment(0, 1)] = "ENG"
CE_1.lang_segments[Segment(1, 2.5)] = "SPA"
CE_1.lang_segments[Segment(2.5, 4)] = "ENG"
confused_spa = 1.5
confused_eng = 0.5

# speaker B Spanish to English caused confusion
CE_2 = utils.LanguageErrorAnalysis(uri="Test")
CE_2.ref_annotation[Segment(0, 4)] = "B"
CE_2.ref_annotation[Segment(0, 1)] = "A"

CE_2.hyp_annotation[Segment(0, 1.75)] = "C"
CE_2.hyp_annotation[Segment(1.75, 3.25)] = "C"
CE_2.hyp_annotation[Segment(3.25, 4)] = "A"

CE_2.lang_segments[Segment(0, 0.5)] = "ENG"
CE_2.lang_segments[Segment(0.5, 2)] = "SPA"
CE_2.lang_segments[Segment(2, 3)] = "ENG"
CE_2.lang_segments[Segment(3, 4)] = "SPA"
#CE_2.plot_annotation()


ref = CE_1.ref_annotation
hyp = CE_1.hyp_annotation
language_map = CE_1.lang_segments


utils.plot_annotations([(ref, 'ref'), (language_map, 'lang'), (hyp, 'hyp')])
plt.show()
analysis = met.EnglishSpanishErrorRate()
components = analysis.compute_components(ref, hyp, language_map=language_map)
error_rates = analysis.compute_metric(components)
print(components)
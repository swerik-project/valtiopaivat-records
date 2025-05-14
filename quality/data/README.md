# Quality Estimation data

## Goldstandard files

Goldstandard files contain samples of the corpus manually annotated by experts.

File naming conventions:

		goldstandard_<name>_<strata>_<number per stratum>_<seed>.csv

### goldstandard_note-seg_year-estate_3_20250514-113663.csv

Used for `quality/estimate-note-seg.py` Note vs. seg (utterance) annotation.

sep=";"

columns:

	- path: pdf page
	- n_paragraphs: number of paragraphs on the page
	- selected_paragraph: randomly (with seed) selected paragraph from range
	- paragraph_classification: "note" or "seg"
	- first_words: first two or three words (exactly with punctuation) to differentiate selected paragraphs from other paragraphs on the page
	- last_words: last two or three words (exactly with punctuation) to differentiate selected paragraphs from other paragraphs on the page
# Segmentation Classification Accuracy

## Summary

Each segment in the records belongs, according to the Parla-Clarin schema, to one type of text. This dimension estimate the proportion of correctly classified text segment.


## What is the problem

Each segment in the protocols belongs, according to the Parla-Clarin schema, to one type of text. First, we seperate the text into what is called body text (the main text that continues over pages) and margin notes (that is not part of the main text). We currently distinguish two different segment classes.


### transcribed speech/utterance (u/seg)

The transcription of somebody speaking in the parliament, in Swedish often called “anförande” or “yttrande”. Written speeches that are read in the parliament also fall under this, although if an  administrative matter is read out loud, then it is not an utterance. 

However, sometimes when the speaker of the house is speaking it is not always clear if there is a description or the speaker. In these cases, it should be classified as a note (see below).


### note

Everything else.


## Estimation procedure

This is a stratified simple random sample, where each paragraph of the original is a unit.


### Sampling plan 

To estimate segmentation classification errors, we take a stratified sample of three paragraphs per year and document type (i.e. three for each estate) and annotate them manually.

__File__: `quality/data/goldstandard_year-estate_3_20250514-113633.csv`


### Annotation guidelines 

__Round 1__: You receive a CSV file with randomly selected pages according to the sampling plan. For each page, indicate the number of paragraphs in the `n_paragraphs` column. A paragraph that started on the previous page counts as 1. A paragraph that starts on this page and continues to the next page counts as one.

Once the number of paragraphs is annotated, one paragraph for each page will be selected at random, using the same seed that generated the page sample

__Round 2__: Open the page again, find the selected paragraph. Indicate `note` or `seg` in the classification column. Provide the first few and the last few words in the selected paragrap so we can identify the text in the xml programatically.

With the exception of speaker introduction + speech, if a paragraph consists of multiple different types of classes, it should be labelled with all of them. This sometimes happens when two paragraphs are accidentally merged in the XML file (i.e. due to segmentation errors).

If it is impossible to know what category the paragraph falls under, label it 'unknown'. This might be the case when the text is corrupted, or only a few words are visible.


## The code

The code for speaker-mapping accuracy estimation is a script that runs through several functions.




#!/usr/bin/env python3

from valtiopy.utils import (
    parse_tei,
)
from torchmetrics.text import WordErrorRate
from tqdm import tqdm
import nltk
import os
import pandas as pd
import unittest

class OCRQualityEstimation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.objective_reality = pd.read_csv("quality/data/goldstandard_ocr_year-estate_3_20251212-113404.tsv", encoding='utf-8', sep="\t")
        cls.most_probable_lines = pd.DataFrame()
        cls.match_errors = []
        cls.wer_fn = WordErrorRate()
        cls.file_mapping = {}


    @classmethod
    def tearDownClass(cls):
        cls.most_probable_lines.to_csv("quality/estimates/ocr-estimate.tsv", index=False, sep="\t")
        err_df = pd.DataFrame(cls.match_errors, columns=["pdf", "xml", "annotation"])
        err_df.to_csv("quality/estimates/ocr-estimate-mismatched-annotations.tsv", index=False, sep="\t")


    def test_estimate_ocr_quality(self):

        def _text_from_range(root, ns, facs):
            text = ""
            start_pb = root.xpath(f".//tei:pb[contains(@facs, '{facs}')]", namespaces={"tei": ns["tei_ns"][1:-1]})
            if len(start_pb) != 1 :
                for e in root.find(f".//{ns['tei_ns']}body").iter():
                    if e.text is not None:
                        text += f" {' '.join([_.strip() for _ in e.text.splitlines() if _.strip() != ''])}"
            else:
                start_pb = start_pb[0]
                start = False
                for e in root.iter():
                    if start and e.tag.endswith("}pb"):
                        start = False
                        break
                    if e == start_pb:
                        start = True
                    if start:
                        if e.text is not None:
                            text += f" {' '.join([_.strip() for _ in e.text.splitlines() if _.strip() != ''])}"
            return text

        def _mk_string_list(l, text):
            """
            make a list of strings of len == len(annotation)
            """
            str_list = []
            start = 0
            while True:
                str_list.append(text[start:start+l+1])
                start += 1
                if start + l + 1 == len(text):
                    break
            return str_list

        def _get_most_probable_line(annotation, text):
            most_probable_line = None
            prob = None
            l = len(annotation)

            for start in range(0, len(text) - l):
                s = text[start:start + l + 1]
                lev = nltk.edit_distance(annotation.lower().strip(), s.lower().strip())

                if prob is None or lev < prob:
                    prob = lev
                    most_probable_line = s
                    # early exit conditions
                    #if prob == 0:
                        #print("early exit 1")
                        #break
                    if prob == 1 and annotation.endswith('-') and not s.endswith('-'):
                        #print("early exit 2")
                        break
            return most_probable_line, prob

        rows = []
        cols = [
            "record",
            "parliament_year",
            "estate",
            "annotation",
            "most_probable_line",
            "lev",
            "wer",
            "cer"
        ]
        print(len(self.objective_reality))
        print(self.file_mapping)
        for record in tqdm([_ for _ in self.objective_reality["path"].unique()]):
            print(record)
            facs = record.split("-")[-1][:-4]  # just getting the page number
            xml_file = f"data/{'/'.join(record.split('/')[-3:-1])}.xml"
            annotations = [_ for _ in self.objective_reality.loc[self.objective_reality["path"] == record, "line_text"].tolist() if pd.notnull(_)]
            py = record.split('/')[-3]
            estate = record.split('/')[-2].split("_")[2]
            root, ns = parse_tei(xml_file)
            candidate_text = _text_from_range(root, ns, facs)

            for annotation in annotations:
                if annotation is None:
                    continue
                most_probable_line, lev = _get_most_probable_line(annotation, candidate_text)
                if most_probable_line is None:
                    self.match_errors.append([motion, xml_file, annotation])
                    continue
                wer = float(self.wer_fn(annotation, most_probable_line))
                cer = lev/len(annotation)
                rows.append([
                    xml_file,
                    py,
                    estate,
                    annotation,
                    most_probable_line,
                    lev,
                    wer,
                    cer
                ])
                print(xml_file, lev, wer, cer)
        type(self).most_probable_lines = pd.DataFrame(rows, columns = cols)




if __name__ == '__main__':
    unittest.main()

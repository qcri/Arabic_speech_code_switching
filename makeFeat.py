#! /usr/bin/env python

# Copyright 2018  QCRI (Authors: Ahmed Ali)
# Apache 2.0.

"""
Script to combine phoneme and words ctms
"""

from __future__ import print_function
from __future__ import division
import argparse
import collections
import logging
from operator import itemgetter

from collections import defaultdict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s [%(pathname)s:%(lineno)s - '
    '%(funcName)s - %(levelname)s ] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_args():
    """gets command line arguments"""

    usage = """ Python script to combine words and phoneme ctms """
    parser = argparse.ArgumentParser(usage)
    parser.add_argument('ctm_phone_words', type=argparse.FileType('r'),
                        help='input_phone_ctm_file')
    parser.add_argument('cs_labels_1', type=argparse.FileType('r'),
                        help='input_cs_1')
    parser.add_argument('cs_labels_2', type=argparse.FileType('r'),
                        help='input_cs_2')
    parser.add_argument('cs_labels_3', type=argparse.FileType('r'),
                        help='input_cs_3')
    parser.add_argument('feat_out', type=argparse.FileType('w'),
                        help='output_feats')
    parser.add_argument('--wordindex', action="store_true", default=False,
                        help='get the word index from the word ctm')
    parser.add_argument('--verbose', type=int, default=0,
                        help="Higher value for more verbose logging.")
    args = parser.parse_args()

    if args.verbose > 2:
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)

    return args

    

def read_labels (label_file1,label_file2,label_file3): 
    labels1 = {} 
    for line in label_file1:
        id = line.split()[0]
        labels1[id]= line.split()[1:]
    label_file1.close()
    
    labels2 = {} 
    for line in label_file2:
        id = line.split()[0]
        labels2[id]= line.split()[1:]
    label_file2.close()
    
    labels3 = {} 
    for line in label_file3:
        id = line.split()[0]
        labels3[id]= line.split()[1:]
    label_file3.close()
        
    return labels1, labels2, labels3

def get_label (word,word_with_label):
    parts = word_with_label.split('_')
    if len(parts) == 2 and word == parts[0]: 
            return parts[1]
    return "NULL"
    
def merge_combine_ctm_labels (combine_ctm_file,labels1,labels2,labels3,_keep_word_index):
    num_lines = 0
    feats = []
    for line in combine_ctm_file:
        if line.startswith("#"):
            feats.append(line.strip() + " label1 label2 label3")
            continue
        id = line.split() [0]
        index = int (line.split() [1])
        
        word = line.split() [2]
        if _keep_word_index: word = line.split() [3]
        l1=get_label (word, labels1[id][index-1])
        l2=get_label (word, labels2[id][index-1])
        l3=get_label (word, labels3[id][index-1])
        feats.append(line.strip()+ " " + l1 + " " + l2 + " " +l3)
    return feats


def write_feats(feats_lines, out_file):
    """Writes CTM lines stored in a list to file."""
    for line in feats_lines:
        print(line, file=out_file)



def main():
    """The main function which parses arguments and call run()."""
    args = get_args()
    (labels1, labels2, labels3) = read_labels (args.cs_labels_1, args.cs_labels_2, args.cs_labels_3)
    feats = merge_combine_ctm_labels (args.ctm_phone_words,labels1,labels2,labels3, args.wordindex)
    
    write_feats(feats, args.feat_out)
    args.feat_out.close()
    logger.info("Wrote Feats for %d recordings.", len(feats))
    

if __name__ == "__main__":
    main()

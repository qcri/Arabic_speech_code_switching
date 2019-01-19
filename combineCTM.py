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
    parser.add_argument('ctm_in_words', type=argparse.FileType('r'),
                        help='input_word_ctm_file')
    parser.add_argument('ctm_in_phonemes', type=argparse.FileType('r'),
                        help='input_phoneme_ctm_file')
    parser.add_argument('ctm_out', type=argparse.FileType('w'),
                        help='output_ctm_file')
    parser.add_argument('--wordindex', action="store_true", default=False,
                        help='get the word index from the word ctm')
    parser.add_argument('--verbose', type=int, default=0,
                        help="Higher value for more verbose logging.")
    args = parser.parse_args()

    if args.verbose > 2:
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)

    return args

    
  
def read_ctm(ctm_file, _keep_word_index):
    """Read CTM from ctm_file into a dictionary of values indexed by the
    utterance.
    It is assumed to be sorted by the utterance-id.

    Returns a dictionary {recording : ctm_lines}
        where ctm_lines is a list of lines of CTM corresponding to the
        utterances in the recording.
        The format is as follows:
        [[(utteranceA, channelA, start_time1, duration1, hyp_word1, conf1),
          (utteranceA, channelA, start_time2, duration2, hyp_word2, conf2),
          ...
          (utteranceA, channelA, start_timeN, durationN, hyp_wordN, confN)],
         [(utteranceB, channelB, start_time1, duration1, hyp_word1, conf1),
          (utteranceB, channelB, start_time2, duration2, hyp_word2, conf2),
          ...],
         ...
         [...
          (utteranceZ, channelZ, start_timeN, durationN, hyp_wordN, confN)]
        ]
    """
    ctms = {}

    num_lines = 0
    for line in ctm_file:
        num_lines += 1
        parts = line.split()

        utt = parts[0]
        confidence = float (parts[1])
        start = float(parts[2])
        duration = float(parts[3])
        end = start+duration
        word = parts[4:]
        
        if utt not in ctms: ctms[utt] = []
        
        if  _keep_word_index : word.insert(0,   str(num_lines))
        
            
        ctms[utt].append([utt, confidence, start, end, duration] + word)

    logger.info("Read %d lines from CTM %s", num_lines, ctm_file.name)

    ctm_file.close()
    return ctms

def compare (word, word_start, word_end, phone, phone_start, phone_end):
    if phone_start > word_end or phone_end < word_start:
        #print (word, phone, phone_start, phone_end, word_start, word_end, 'False')
        return False
    else:
        #print (word, phone, phone_start, phone_end, word_start, word_end, 'True')
        return True

    
def merge_ctm (_wordctm, _phonectm, _keep_word_index):
    if _keep_word_index:
        ctm_lines = ["#id word_index_in_sentence word_index_in_word_ctm word word_conf word_start word_duration word_end phone phone_conf phone_start phone_duration phone_end"] 
    else: 
        ctm_lines = ["#id word_index_in_sentence word word_conf word_start word_duration word_end phone phone_conf phone_start phone_duration phone_end"] 
    for idx, id in enumerate(_wordctm):
        
        _wordctm[id].sort(key=itemgetter(2))
        _phonectm[id].sort(key=itemgetter(2))
        for idx2, val2 in enumerate(_wordctm [id]):
            word_phone_overlap=False
            #print(idx2, val2)
            
            if  _keep_word_index: word = val2 [-2] + ' ' + val2 [-1]
            word_start = val2 [2]
            word_end = val2 [3]
            word_conf = val2 [1]
            word_duration = word_end - word_start
            
            for idx3, val3 in enumerate(_phonectm [id]):
                
                phone = val3 [-1]
                phone_start = val3 [2]
                phone_end = val3 [3]
                phone_conf = val3 [1]
                phone_duration = phone_end - phone_start
                
                
                # ignore phonemes that ended before word begins.
                if phone_end < word_start: 
                    _phonectm [id].pop(idx3)
                    continue
                if (compare (word, word_start, word_end, phone, phone_start, phone_end)):
                    combied_line = id, idx2+1, word, word_conf, word_start, word_duration, word_end, phone, phone_conf, phone_start, phone_duration, phone_end
                    #print (combied_line)
                    ctm_lines.append(" ".join(map(str,combied_line)))
                    word_phone_overlap=True
                    #print (" ".join(map(str,combied_line)))
                    #_phonectm [id].pop(idx3)
                if word_end < phone_start: break 
            if not word_phone_overlap:
                combied_line = id, idx2+1, word, word_conf, word_start, word_duration, word_end, "NULL", 0, 0, 0, 0
                ctm_lines.append(" ".join(map(str,combied_line)))
        #sys.exit()
    return ctm_lines

def write_ctm(ctm_lines, out_file):
    """Writes CTM lines stored in a list to file."""
    for line in ctm_lines:
        print(line, file=out_file)



def main():
    """The main function which parses arguments and call run()."""
    args = get_args()
    word_ctm = read_ctm(args.ctm_in_words,args.wordindex)
    phoneme_ctm = read_ctm(args.ctm_in_phonemes,False)
    combine_ctm = merge_ctm (word_ctm, phoneme_ctm,args.wordindex)
    write_ctm(combine_ctm, args.ctm_out)
    args.ctm_out.close()
    logger.info("Wrote CTM for %d recordings.", len(phoneme_ctm))
    

if __name__ == "__main__":
    main()

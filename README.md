<!-- # Dialectal-Arabic-Code-Switching-Dataset-->

# Dialectal Arabic Code-Switching Dataset.

This release includes the annotated two-hours Egyptian dataset from the ADI-5 development split in the MGB-3 challenge [1].
The released MGB-3 data includes speech features and textual features extracted from ASR transcription.

Unlike MGB-3:EGY, this dataset is *manually segmented* to the audio into smaller utterances (with 500 msec silence or more) and *transcribed* the speech verbatim by a lay native Egyptian speaker.

The transcribed data is then annotated for word-level Code-Switching (CS) information by 3 annotators. Using the guideline mentioned in the paper,
the annotators were asked to classify the words into one of the following four categories:
(i) *MSA*: MSA word with MSA pronunciations; (ii) *EGY*: Egyptian word; (iii) *MIX*: MSA word with dialectal pronunciations and (iv) *FRN*: Foreign word, i.e., not Arabic.
In addition, a 'NULL' tag was assigned in case the word is unintelligible or cannot be categorised to one of the four labels.

More details in paper:

```
@inproceedings{chowdhury2020cs,
  title={Effects of Dialectal Code-Switching on Speech Modules: A Study using Egyptian Arabic Broadcast Speech},
  author={Chowdhury, Shammur Absar  and Samih, Younes and Eldesouki, Mohamed and Ali, Ahmed},
  booktitle={INTERSPEECH},
  year={2020}
}
```

also available in [Paper](http://www.interspeech2020.org/uploadfile/pdf/Wed-1-10-5.pdf)

## Data Format
*DACS_word_level.feat*
The input file -- containing words and corresponding labels, are presented in `DACS_word_level.feat`. The file contains the following fields (space seperated), including
`#id word_index_in_sentence word word_start word_duration word_end label1 label2 label3`

where
`#id` is the corresponding wav id

`word_index_in_sentence` indicates the position of the word in the utterance.

`word` manually transcribed word (in Buckwalter transliteration format)

`word_start` start time of the word in secs.

`word_duration` duration of the word in secs.

`word_end` end time of the word in secs.

`phone phone_conf phone_start phone_duration phone_end` same info for phone (forced aligned)

`label[1-3]` annotation label provided by annotator [1-3]

*segments_dacs*
The file include information of the manually segmented MGB-3:EGY to utterances. The file includes:
`segmented_id audio_id segment_start segment_end`

where
`segmented_id` is the wav id of the utterance

`audio_id` is the id of original audio file from MGB-3:EGY.

`segment_start/end` the start and the end time of the segmented utterances.

*mgb3_audio_list.txt*
A list of audio files (MGB-3:EGY) used for this dataset. Can be directly downloaded given the url of the audio.




[1] Ali, Ahmed, Stephan Vogel, and Steve Renals. "Speech recognition challenge in the wild: Arabic MGB-3." 2017 IEEE Automatic Speech Recognition and Understanding Workshop (ASRU). IEEE, 2017.


<!-- booktitle={Proceedings of the International Conference on Language Resources and Evaluation (LREC'20)}, -->

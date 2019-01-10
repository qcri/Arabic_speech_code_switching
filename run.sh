python combineCTM.py data/txt/words_QATS.ctm data/txt/phoneme_HU.ctm words_HU.ctm
python makeFeat.py words_HU.ctm data/txt/{E,K,S}.txt.bw words_HU_data.feat

python combineCTM.py data/txt/words_QATS.ctm data/txt/phoneme_CZ.ctm words_CZ.ctm
python makeFeat.py words_CZ.ctm data/txt/{E,K,S}.txt.bw words_CZ_data.feat

python combineCTM.py data/txt/words_QATS.ctm data/txt/phoneme_RU.ctm words_RU.ctm
python makeFeat.py words_RU.ctm data/txt/{E,K,S}.txt.bw words_RU_data.feat

rm words_??.ctm


for phoneme in HU RU CZ; do
    python combineCTM.py --wordindex data/txt/words_QATS.ctm data/txt/phoneme_${phoneme}.ctm words_${phoneme}.ctm
    python makeFeat.py --wordindex words_${phoneme}.ctm data/txt/{E,K,S}.txt.bw words_${phoneme}_data.feat
done 
rm words_??.ctm

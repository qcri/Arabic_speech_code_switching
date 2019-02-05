for phoneme in HU RU CZ; do
    python combineCTM.py --wordindex data/MGB3_EGY/txt/words_QATS.ctm data/MGB3_EGY/txt/phoneme_${phoneme}.ctm words_${phoneme}.ctm
    python makeFeat.py --wordindex words_${phoneme}.ctm data/MGB3_EGY/txt/{E,K,S}.txt.bw data/MGB3_EGY/txt/words_${phoneme}_data.feat
done 
rm words_??.ctm


for phoneme in HU RU CZ; do
    python combineCTM.py --wordindex data/GALE/txt/words_QATS.ctm data/GALE/txt/phoneme_${phoneme}.ctm words_${phoneme}.ctm
    python makeFeat.py --wordindex words_${phoneme}.ctm data/GALE/txt/{text.bw.labels,text.bw.labels,text.bw.labels} data/GALE/txt/words_${phoneme}_data.feat$$
    awk 'NF{NF-=2};1' < data/GALE/txt/words_${phoneme}_data.feat$$ > data/GALE/txt/words_${phoneme}_data.feat
    rm -fr data/GALE/txt/words_${phoneme}_data.feat$$
done 
rm words_??.ctm


#!/bin/bash
set -e

simulate_data=

num_ch=6

prefix=MTG_t1t2
# aug_affix=_NOTSOFAR_noise
aug_affix=_MUSAN_noise
# aug_data_dir=css-datasets
aug_data_dir=musan_noise

. path.sh
. utils/parse_options.sh

data=$(basename $simulate_data)
# mkdir -p data/$data

echo $prefix $aug_affix $aug_data_dir $simulate_data  

# find $simulate_data/wav | grep -v source | grep -v rir | grep -v noise | grep "\.wav" | awk -F "[./]" -v var=$prefix '{print var$(NF-1)"_CH1","sox",$0,"-t wav - remix 1 |"}' > data/$data/wav.scp

# awk '{print $1,$1}' data/$data/wav.scp > data/$data/utt2spk
# utils/fix_data_dir.sh data/$data
utils/data/get_reco2dur.sh --nj 32 $simulate_data
mkdir -p data/${data}$aug_affix
awk '{$1=$1"_noise"; print $0}' $simulate_data/wav.scp > data/${data}$aug_affix/wav.scp
cp $simulate_data/reco2dur data/${data}$aug_affix/reco2dur

# for ch in `seq 1 $num_ch`;
# do
#     echo $ch
#     awk -v ch=$ch '{$(NF-1)=ch;print $0}' $simulate_data/wav.scp | sed "s/CH0/CH$ch/g" >> data/${data}_tmp/wav.scp
#     cat $simulate_data/reco2dur | sed "s/CH1/CH$ch/g" >> data/${data}_tmp/reco2dur
# done
# exit
# rm -rf data/${data}
# mv data/${data}_tmp data/${data}
awk '{print $1,$1}' data/${data}$aug_affix/wav.scp > data/${data}$aug_affix/utt2spk
cp data/${data}$aug_affix/utt2spk data/${data}$aug_affix/spk2utt
cp $simulate_data/oracle.rttm data/${data}$aug_affix/oracle.rttm
utils/fix_data_dir.sh data/${data}$aug_affix

python local/augment_data_multi_channel_dir.py --utt-suffix "noise" --bg-snrs "5:4:3:2:1:0:-1:-2:-3:-4:-5" --bg-noise-dir "data/${aug_data_dir}" $simulate_data data/${data}$aug_affix
# python steps/data/augment_data_dir_random.py --utt-suffix "mixer6_noise" --bg-snrs "5:4:3:2:1:0:-1:-2:-3:-4:-5" --bg-noise-dir "data/mixer6_train_noise" data/${data} data/${data}_Mixer6Noise

# python local/gen_mixspec_rttm_ctm.py $simulate_data/mixspec.json 

# cat $simulate_data/rttm/* | awk -v var=$prefix '{$2=var$2;print $0}' > data/${data}/oracle.rttm

# for ch in `seq 1 $num_ch`;
# do
#     # awk -v ch=$ch '{$2=$2"_CH"ch"_mixer6_noise";print $0}' data/${data}_Mixer6Noise/oracle.rttm >> data/${data}_Mixer6Noise/rttm
#     awk -v ch=$ch '{$2=$2"_CH"ch;print $0}' data/${data}/oracle.rttm >> data/${data}/diarized.allrttm
# done
# aug_data=$(realpath data/${data})
aug_data=$(realpath data/${data}${aug_affix})
cd /train33/sppro/permanent/gbyang/code/NSD-MS2S/data

ln -s $aug_data 
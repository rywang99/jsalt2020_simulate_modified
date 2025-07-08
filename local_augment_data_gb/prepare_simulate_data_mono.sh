#!/bin/bash
set -e
simulate_data=$1

num_ch=1

data=$(basename $simulate_data)

mkdir -p data/$data

find $simulate_data/wav | grep -v source | grep -v rir | grep -v noise | grep "\.wav" | awk -F "[./]" '{print "SimuLibri_DEV_reverb_"$(NF-1),$0}' > data/$data/wav.scp
awk '{print $1,$1}' data/$data/wav.scp > utt2spk
utils/fix_data_dir.sh data/$data
utils/data/get_reco2dur.sh --nj 32 data/$data
mkdir data/${data}_tmp
cp data/$data/wav.scp data/${data}_tmp/wav.scp
cp data/$data/reco2dur data/${data}_tmp/reco2dur
# for ch in `seq 2 $num_ch`;
# do
#     echo $ch
#     awk -v ch=$ch '{$(NF-1)=ch;print $0}' data/$data/wav.scp | sed "s/CH1/CH$ch/g" >> data/${data}_tmp/wav.scp
#     cat data/$data/reco2dur | sed "s/CH1/CH$ch/g" >> data/${data}_tmp/reco2dur
# done
rm -rf data/${data}
mv data/${data}_tmp data/${data}
awk '{print $1,$1}' data/${data}/wav.scp > data/${data}/utt2spk
utils/fix_data_dir.sh data/${data}
exit
# python steps/data/augment_data_multi_channel_dir.py --utt-suffix "noise" --bg-snrs "5:4:3:2:1:0:-1:-2:-3:-4:-5" --bg-noise-dir "data/chime6_noise_final" data/${data} data/${data}_CHiME6Noise
python steps/data/augment_data_dir.py --utt-suffix "mixer6_noise" --bg-snrs "5:4:3:2:1:0:-1:-2:-3:-4:-5" --bg-noise-dir "data/mixer6_train_noise" data/${data} data/${data}_Mixer6Noise

python local/gen_mixspec_rttm_ctm.py $simulate_data/mixspec.json

cat $simulate_data/rttm/* | awk '{$2="SimuLibri_DEV_reverb_"$2;print $0}' > data/${data}_Mixer6Noise/oracle.rttm
# for ch in `seq 1 $num_ch`;
# do
#     awk -v ch=$ch '{$2=$2"_CH"ch"_mixer6_noise";print $0}' data/${data}_Mixer6Noise/oracle.rttm >> data/${data}_Mixer6Noise/rttm
# done
aug_data=$(realpath data/${data}_Mixer6Noise)

# cd ../mamse/data

# ln -s $aug_data
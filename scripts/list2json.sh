# Import $EXPROOT. 
ROOTDIR=`dirname $0`/..
ROOTDIR=`realpath $ROOTDIR`
source $ROOTDIR/path.sh

# Subset of Kaldi utils
KALDI_UTILS=$ROOTDIR/tools/kaldi_utils

# Environment
export PATH=${KALDI_UTILS}:${PATH}
. $ROOTDIR/configs/cmd.sh

datalist=/train33/sppro/permanent/gbyang/code/jsalt2020_simulate/librispeech_all.list_suf2
nj=32
set=all
# Split datalist for parallel processing
splitdir=simulate_data/librispeech_clean_all_suf2
mkdir -p ${splitdir}/log
split_scp.pl ${datalist} $(for j in $(seq ${nj}); do echo ${splitdir}/${set}.${j}.list; done)

# Create a JSON file for the source data set. (~10 min with nj=32)
datajson=simulate_data/librispeech_clean_all_suf2/${set}.json
run.pl JOB=1:${nj} ${splitdir}/log/list2json.JOB.log \
        python tools/list2json_librispeech.py --input_list ${splitdir}/${set}.JOB.list --novad --output_file ${splitdir}/${set}.JOB.json
python tools/mergejsons.py $(for j in $(seq ${nj}); do echo ${splitdir}/${set}.${j}.json; done) > $datajson

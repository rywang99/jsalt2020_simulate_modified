set -e
name=close_talk_reb
extend=true
# # path=/train33/sppro/permanent/gbyang/code/NSD-MS2S/local_gb/$name
# path=/train33/sppro/permanent/gbyang/code/NSD-MS2S/exp/gss_base/MTG2_dev_mc-close_talk/enhanced
# find $path -type f >  /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/$name.list

if $extend; then
    # cp /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/$name.list /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/$name.cp.list
    # for i in {1..4}; do cat /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/$name.list >> /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/$name.cp.list; done
    # shuf /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/$name.cp.list -o /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/${name}_extend5_new.list
    name=${name}_extend5_new
    echo $name
fi


bash /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/scripts/list2json.sh --name $name

rm -rf /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/simulate_data/data/MTG_$name/
bash /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/scripts/run_meetings_revb_chime8_MTG_t1_t2_wpe_gb.sh --datajson /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/simulate_data/$name/all.json MTG_$name train

# python /train33/sppro/permanent/gbyang/code/augment_data/local/gen_mixspec_rttm_utt.py /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/simulate_data/data/MTG_$name/mixspec.json

# python /train33/sppro/permanent/gbyang/code/NSD-MS2S/local_gb/statis_overlap_rate.py /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/simulate_data/data/MTG_$name/rttm_utt/

# bash /train33/sppro/permanent/gbyang/code/NSD-MS2S/local_gb/cal_time.sh --folder_path /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/simulate_data/data/MTG_$name/wav

bash /train33/sppro/permanent/gbyang/code/augment_data/local/prepare_simulate_data2.sh --prefix MTG_$name --simulate_data /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/simulate_data/data/MTG_$name/
cd /train33/sppro/permanent/gbyang/code/NSD-MS2S/
cp /train33/sppro/permanent/gbyang/code/NSD-MS2S/data/MTG_$name/oracle.rttm data/MTG_$name/diarized.all.rttm

bash /train33/sppro/permanent/gbyang/code/NSD-MS2S/local_gb/extract_Simu_muti_CH_training_data.sh --stage 1 --data MTG_$name


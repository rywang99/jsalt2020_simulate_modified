set -e
# cd /train33/sppro/permanent/gbyang/code/jsalt2020_simulate
nj=16
# prefix=Simu_libri_clean_all_config6
# aug_affix=_NOTSOFAR_noise
# aug_data_dir=css-datasets

# simu_data_dir=Simu_libri_clean_all_config6
# simu_data_dir=MTG_close_talk_reb_extend25_new
simu_data_dir=mutichannel_rir_data_t1+t2
simu_data_dir=MTG_dev1_close_talk_reb_extend25_new
simu_data_dir=MTG_dev2_close_talk_reb_extend25_new
bash scripts/run_meetings_revb_chime8_MTG_t1_t2_wpe_gb.sh --split $nj $simu_data_dir train

# cd /train33/sppro/permanent/gbyang/code/augment_data
# bash local/prepare_simulate_data.sh --simulate_data /train33/sppro/permanent/gbyang/code/jsalt2020_simulate/simulate_data/data/$simu_data_dir   --prefix $prefix --aug_affix $aug_affix --aug_data_dir $aug_data_dir

# cd /train33/sppro/permanent/gbyang/code/NSD-MS2S
# bash local_gb/extract_Simu_muti_CH_training_data.sh --data ${simu_data_dir}$aug_affix
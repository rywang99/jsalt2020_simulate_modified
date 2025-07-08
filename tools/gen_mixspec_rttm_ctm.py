import json
import numpy as np
import os,glob


# ctm_file = ["/train8/sppro/mkhe/data/LibriSpeech/librispeech_ctm/train_clean_100.ctm", 
#             "/train8/sppro/mkhe/data/LibriSpeech/librispeech_ctm/train_clean_360.ctm",
#             "/train8/sppro/mkhe/data/LibriSpeech/librispeech_ctm/train_other_500.ctm",
#             ]

ctm_file = glob.glob("/train33/sppro/permanent/gbyang/data/LibriSpeech/librispeech_ctm/*.ctm")
# max_dur = 0
# for ctm in ctm_file:
#     with open(ctm) as IN:
#         for l in IN:
#             utt, _, start, dur, _ = l.split()
#             max_dur = max(max_dur, float(start) + float(dur))
# max_dur = int(max_dur) + 2
max_dur=36
print('max_dur of utt is ', max_dur)

utt2label = {}
def write_rttm(session_label, output_path, min_segments=0):
    with open(output_path, "w") as OUT:
        for session in session_label.keys():
            for spk in session_label[session].keys():
                labels = session_label[session][spk]
                to_split = np.nonzero(labels[1:] != labels[:-1])[0]
                to_split += 1
                if labels[-1] == 1:
                    to_split = np.r_[to_split, len(labels)+1]
                if labels[0] == 1:
                    to_split = np.r_[0, to_split]
                for l in to_split.reshape(-1, 2):
                    #print(l)
                    #break
                    if (l[1]-l[0])/100. < min_segments:
                        continue
                    OUT.write("SPEAKER {} 1 {:.2f} {:.2f} <NA> <NA> {} <NA> <NA>\n".format(session, l[0]/1000., (l[1]-l[0])/1000., spk))


for ctm in ctm_file:
    with open(ctm) as IN:
        for l in IN:
            utt, _, start, dur, _ = l.split()
            if utt not in utt2label.keys():
                utt2label[utt] = np.zeros(max_dur * 1000)
            utt2label[utt][ int(float(start)*1000) : int(float(start)*1000+float(dur)*1000) ] = 1
        print('finished ', ctm)

mixspec = "/train33/sppro/permanent/gbyang/code/jsalt2020_simulate/simulate_data/data/librispeech_all_revb_4channel_4-8/mixspec.json"
with open(mixspec) as IN:
    mixs = json.load(IN)

os.makedirs(os.path.dirname(mixspec)+"/rttm", exist_ok=True)

for mix in mixs:
    session = os.path.basename(mix["output"].split(".")[0])
    rttm = {}
    rttm[session] = {}
    for spk in mix["speakers"]:
        rttm[session][spk] = np.zeros(1800 * 1000)
    for utt in mix["inputs"]:
        try:
            rttm[session][utt["speaker_id"]][ int(utt["offset"]*1000) : int(utt["offset"]*1000)+int(utt["length_in_seconds"]*1000) ] = utt2label[utt["utterance_id"]][:int(utt["length_in_seconds"]*1000)]
        except:
            print(mix["output"], utt["path"], session, utt["speaker_id"], utt["offset"]*1000, utt["length_in_seconds"]*1000, len(utt2label[utt["utterance_id"]]))
            exit()
    write_rttm(rttm, f"{os.path.dirname(mixspec)}/rttm/{session}.rttm")

import json
import numpy as np
import os
import sys


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

# mixspec = "simulate_data/data/Simu_LibriSpeech_dev_4spk_4channel_reverb_dipco/mixspec.json"
mixspec = sys.argv[1]
with open(mixspec) as IN:
    mixs = json.load(IN)

os.makedirs(os.path.dirname(mixspec)+"/rttm_utt", exist_ok=True)

for mix in mixs:
    session = os.path.basename(mix["output"].split(".")[0])
    rttm = {}
    rttm[session] = {}
    for spk in mix["speakers"]:
        rttm[session][spk] = np.zeros(1800 * 1000)
    for utt in mix["inputs"]:
        rttm[session][utt["speaker_id"]][ int(utt["offset"]*1000) : int(utt["offset"]*1000)+int(utt["length_in_seconds"]*1000) ] = 1
    write_rttm(rttm, f"{os.path.dirname(mixspec)}/rttm_utt/{session}.rttm")

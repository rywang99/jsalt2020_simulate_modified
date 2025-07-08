import json
import numpy as np
import os




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


utt2label = {}
with open("../data/LibriSpeech/librispeech_ctm/train_clean_100.ctm") as IN:
    for l in IN:
        utt, _, start, dur, _ = l.split()
        if utt not in utt2label.keys():
            utt2label[utt] = np.zeros(35 * 1000)
        utt2label[utt][ int(float(start)*1000) : int(float(start)*1000+float(dur)*1000) ] = 1
print("Finish load 100")
with open("../data/LibriSpeech/librispeech_ctm/train_clean_360.ctm") as IN:
    for l in IN:
        utt, _, start, dur, _ = l.split()
        if utt not in utt2label.keys():
            utt2label[utt] = np.zeros(35 * 1000)
        utt2label[utt][ int(float(start)*1000) : int(float(start)*1000+float(dur)*1000) ] = 1
with open("../data/LibriSpeech/librispeech_ctm/train_other_500.ctm") as IN:
    for l in IN:
        utt, _, start, dur, _ = l.split()
        if utt not in utt2label.keys():
            utt2label[utt] = np.zeros(35 * 1000)
        utt2label[utt][ int(float(start)*1000) : int(float(start)*1000+float(dur)*1000) ] = 1

file = 'Simu_LibriSpeech_train_4spk_clean_SP'
with open("simulate_data/data/{}/mixspec.json".format(file)) as IN:
    mixs = json.load(IN)
from tqdm import tqdm
os.makedirs("simulate_data/data/{}/rttm".format(file), exist_ok=True)
for mix in tqdm(mixs):
    session = os.path.basename(mix["output"]).split('.')[0]
    if os.path.isfile(f"simulate_data/data/{file}/rttm/{session}.rttm"):
        continue
    # print(f"Processing {session}")
    rttm = {}
    rttm[session] = {}
    for spk in mix["speakers"]:
        rttm[session][spk] = np.zeros(1800 * 1000)
    for utt in mix["inputs"]:
        rttm[session][utt["speaker_id"]][ int(utt["offset"]*1000) : int(utt["offset"]*1000) + int(utt["length_in_seconds"]*1000) ] = utt2label[utt["utterance_id"]][:int(utt["length_in_seconds"]*1000)]
    write_rttm(rttm, f"simulate_data/data/{file}/rttm/{session}.rttm")
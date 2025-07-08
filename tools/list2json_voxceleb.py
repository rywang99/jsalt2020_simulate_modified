#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, os, sys, re, json, wave
from collections import OrderedDict



def main(args):
    # Create an empty corpus.    
    corpus = []

    # Count the number of lines.
    nlines = 0
    with open(args.input_list) as input_strm:
        for l in input_strm:
            nlines += 1

    # Read each line and get file names. 
    nlines_done = 0
    with open(args.input_list) as input_strm:
        for l in input_strm:
            # path, utterance ID
            path = l.rstrip()
            #/train8/sppro/hszhou2/chime7/data/VoxCeleb/voxceleb1/vox1_dev_wav/wav/id11235/aaebCc11h2I/00006.wav
            spkrid, url, utt = path.split("/")[-3:]
            uttid = "-".join([spkrid, url, utt.split('.')[0]])

            try:
                with wave.open(path) as wf:
                    nsamples = wf.getnframes()
                    sr = wf.getframerate()
                    dur = nsamples / sr
            except:
                print(path)
                continue
            # Generate segment info for the current file. 
            seg_info = OrderedDict([('utterance_id', uttid),
                                    ('path', path),
                                    ('speaker_id', spkrid),
                                    ('number_of_samples', nsamples),
                                    ('sampling_rate', sr),
                                    ('length_in_seconds', dur)])
            
            corpus.append(seg_info)
            
            # Print a progress report. 
            nlines_done += 1
            if nlines_done % 100 == 0:
                print('{:.2f}% [{}/{}]'.format(nlines_done/nlines * 100, nlines_done, nlines), flush=True)


    # Generate the output corpus file. 
    with open(args.output_file, 'w') as f:
        json.dump(corpus, f, indent=2)

        

def make_argparse():
    # Set up an argument parser. 
    parser = argparse.ArgumentParser(description='Create a JSON file for LibriSpeech.')
    parser.add_argument('--input_list', required=True, 
                        help='Wav file list.')
    parser.add_argument('--output_file', required=True,
                        help='Output JSON file name.')
    parser.add_argument('--novad', action='store_true', 
                        help='File name pattern for the no-VAD (i.e., the original LibriSpeech) data.')
                        
    return parser
    
    
if __name__ == '__main__':
    parser = make_argparse()
    args = parser.parse_args()
    main(args)
    


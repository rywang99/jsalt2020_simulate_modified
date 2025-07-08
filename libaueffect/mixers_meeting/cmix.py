# -*- coding: utf-8 -*-
import libaueffect

import os
from collections import OrderedDict
import numpy as np
import copy

import re


class CleanMixMeeting(object):
    def __init__(self, gain_range=[-5, 5]):
        self._gain_range = gain_range

        print('Instantiating CleanMixMeeting')
        print('Gain range in dB: ({}, {})'.format(self._gain_range[0], self._gain_range[1]))
        print('', flush=True)



    def substitute_generators(self, generator_pool):
        pass


    def __call__(self, inputs, offsets, speaker_labels, to_return=()):
        ylen = np.amax([len(dt) + offset for dt, offset in zip(inputs, offsets)])
        # return_source = True

        spkrs = sorted(list(set(speaker_labels)))
        nspkrs = len(spkrs)
        s = np.zeros((nspkrs, ylen))
        spkr2idx = {spkr: i for i, spkr in enumerate(spkrs)}

        y = np.zeros(ylen)
        for dt, offset, spkr in zip(inputs, offsets, speaker_labels):
            gain = np.random.uniform(self._gain_range[0], self._gain_range[1])
            scale = 10**(gain / 20)
            s[spkr2idx[spkr], offset : offset + len(dt)] += scale * dt
            y[offset : offset + len(dt)] += scale * dt

        # description of the mixing process
        params = [('mixer', self.__class__.__name__),
                  ('implementation', __name__)]

        data = {}
        wanted = 'source'
        interm = {}
        for spkr in spkrs:
            name = f'{wanted}{spkr}'
            data[name] = s[spkr2idx[spkr]]
        interm[wanted] = data

        return y, OrderedDict(params), interm

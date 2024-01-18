# Ekstakcja cech rozpoznawanie mowy
from python_speech_features import logfbank
import scipy.io.wavfile  as wav
import numpy as np
import os
from pathlib import Path

def ekstrakcja_cech():
    paths = []
    labels = []
    labels_categorial = []
    root = 'Dataset_wav/';
    #root = 'SpeechDataset/'
    # utórz katalog 'SpeechDataset/'

    new_path = os.path
    print(new_path)

    for ind, subdir in enumerate(os.listdir(root)):
        for file in os.listdir(os.path.join(root,subdir))[:100]:
            filepath = os.path.join(root, subdir, file)
            paths.append(filepath)
            labels.append(ind)
            labels_categorial.append(subdir)

    logfbank_feats = []
    for signal_path in paths:
        fs,sig = wav.read(signal_path)
        fbank_feat = logfbank(sig, samplerate=fs)
        logfbank_feats.append(fbank_feat)


    lenghts = []
    for i in logfbank_feats:
        lenghts.append(i.shape[0])
    max_len = np.max(lenghts)

    #(max_len)

    padded_feats = np.zeros((len(lenghts), max_len, logfbank_feats[0].shape[1]))
    ## zastosowałem z numpy intc nie int
    for i, feats in enumerate(padded_feats):
        padded_feats[i,:,:] = np.pad(feats, ((np.intc(np.floor((max_len - feats.shape[0])/2)), np.intc(np.ceil((max_len - feats.shape[0]) / 2))), (0, 0)))

    # Macierz cech  i wektor etykiet zapisywany do plików
    np.save('npy_files/KL/logfbank_feats.npy',padded_feats)
    np.save('npy_files/KL/labels.npy', labels)
    np.save('npy_files/KL/labels_categorial.npy', labels_categorial)
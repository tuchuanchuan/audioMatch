# coding: utf-8
import traceback

import os
import json
from collections import defaultdict


def get_pairs(allp):
    allp = sorted(allp, key=lambda x: x[0])
    all_pair = list()
    count = 0
    for i1, p1 in enumerate(allp):
        for p2 in allp[i1+1: ]:
            if abs(p1[0]-p2[0]) < 5:
                if p1[0] > p2[0]:
                    pair = [str(p1[1]), str(p1[0]-p2[0]), str(p1[1]-p2[1]), p1[0], p2[0]]
                else:
                    pair = [str(p2[1]), str(p2[0]-p1[0]), str(p2[1]-p1[1]), p2[0], p1[0]]
                all_pair.append(pair)
            else:
                break
        count += 1
    return all_pair


def get_peaks(f):
    allp = list()
    for l in f:
        if not l.strip():
            continue
        l = l.strip().split('=')
        p = (int(l[0]), int(l[1]))
        allp.append(p)
    return allp


def read_hash_table(f):
    hash_table = defaultdict(list)
    tracks = set()
    for l in f:
        l = l.decode('gbk').strip().split("####")
        key = l[0]
        for item in l[1:]:
            hash_table[key].append(item.split('###'))
        for track in hash_table[key]:
            tracks.add(track[0])
    f.close()
    return hash_table, tracks


def main():
    if os.path.isfile("D:\\wav\\fingerprint\\hash_table"):
        hash_table, tracks = read_hash_table(open('D:\\wav\\fingerprint\\hash_table'))
    else:
        hash_table, tracks = defaultdict(list), []
    count = 0
    print tracks
    for index, (dirname, dirnames, filenames) in enumerate(os.walk('D:\\wav\\fingerprint')):
        for filename in filenames:
            if filename == 'hash_table':
                continue
            if filename in ['blackbox-20s', 'Rock This-20s']:
                continue
            if filename.decode('gbk') in tracks:
                continue
            file_path = os.path.join(dirname, filename)
            print file_path
            try:
                allp = get_peaks(open(file_path))
                all_pair = get_pairs(allp)
                print 'pairs: {}'.format(len(all_pair))
                for pair in all_pair:
                    hash_table[','.join(pair[:-2])].append([filename.decode('gbk'), ] + map(str, pair[-2:]))
                count += 1
                if count > 10:
                    break
            except Exception as e:
                traceback.print_exc()
    f = open('D:\\wav\\fingerprint\\hash_table', 'w')
    for key, value in hash_table.items():
        f.write(key)
        for item in value:
            f.write('####')
            f.write((u'###'.join(item)).encode('gbk'))
        f.write('\n')
    f.close()


if __name__ == '__main__':
    main()
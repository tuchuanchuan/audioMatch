# coding: utf-8
import plotly as py
from plotly.graph_objs import Scatter, Layout

from collections import defaultdict
import json


def read_hash_table(f):
    hash_table = defaultdict(list)
    tracks = set()
    for l in f:
        l = l.decode('gbk').strip().split("####")
        key = l[0]
        for item in l[1:]:
            hash_table[key].append(item.split('###'))
            tracks.add(item.split('###')[0])
    print 'tracks: ', len(tracks), tracks
    f.close()
    return hash_table


def get_peaks(f):
    allp = list()
    for l in f:
        l = l.strip().split('=')
        p = (int(l[0]), int(l[1]))
        allp.append(p)
    return allp

def get_pairs(allp):
    allp = sorted(allp, key=lambda x: x[0])
    all_pair = list()
    time_list = list()
    count = 0
    for i1, p1 in enumerate(allp):
        for p2 in allp[i1+1: ]:
            if abs(p1[0]-p2[0]) < 5:
                if p1[0] > p2[0]:
                    pair = p1[1], p1[0]-p2[0], p1[1]-p2[1]
                    t = p1[0], p2[0]
                else:
                    pair = p2[1], p2[0]-p1[0], p2[1]-p1[1]
                    t = p2[0], p1[0]
                all_pair.append(pair)
                time_list.append(t)
            else:
                break
        count += 1
    return all_pair, time_list

def plot_matched(matched_pair, size, color):
    x_list = []
    y_list = []
    for pair in matched_pair:
        p2 = pair[3], pair[0]
        p1 = pair[4],  pair[0]-pair[2]
        x_list.append(p1[0])
        x_list.append(p2[0])
        y_list.append(p1[1])
        y_list.append(p2[1])
    trace = Scatter(x=x_list, y=y_list, mode="markers", marker=dict(size=size, line=dict(width=1), color=color,))
    return trace


color_list = ['22ad48', 'ff0000']
size_list = [7, 4]


def get_peak_density(l, size):
    l = sorted(map(int, l))
    s = e = 0
    max_count = 0
    max_s = max_e = 0
    while e < len(l):
        if l[e] - l[s] < size:
            e += 1
        else:
            if e-s > max_count:
                max_count = e-s
                max_s, max_e = s, e
            s += 1
    return l[max_s], l[max_e], max_count


def main():
    allp = sorted(get_peaks(open(u'D:\\wav\\fingerprint\\白色情人节歌单-30%'.encode('gbk'))), key=lambda x: x[0])
    hash_table = read_hash_table(open('D:\\wav\\fingerprint\\hash_table'))
    allp_list = []
    r = 863 
    for step in range(32026/r):
        allp_list.append(filter(lambda x: x[0] < (step+1)*r and x[0] > step*r, allp))
    for index, ap in enumerate(allp_list):
        # if index > 1:
        #     break
        pairs, times = get_pairs(ap)
        title_dict = defaultdict(list)
        print index*10, len(pairs)
        matched_pair = defaultdict(list)
        for i, pair in enumerate(pairs):
            key = ','.join(map(str, pair))
            if key in hash_table:
                for title, t1, t2 in hash_table[key]:
                    title_dict[title].append(t2)
                    matched_pair[title].append(pair + (t1, t2))

        # for title, value in sorted(title_dict.items(), key=lambda x: -x[1])[:10]:
        #     print title.encode('gbk'), value
        peak_title_dict = dict()
        for title, t_list in title_dict.items():
            peak_title_dict[title] = get_peak_density(t_list, r)
        for title, value in sorted(peak_title_dict.items(), key=lambda x: -x[1][2])[:5]:
            print title.encode('gbk'), value
        # if index == 1:
        #     count = 0
        #     trace_list = []
        #     for title, value in sorted(peak_title_dict.items(), key=lambda x: -x[1][2])[:2]:
        #         trace_list.append(plot_matched(matched_pair[title], size_list[count], color_list[count]))
        #         count += 1
        #     py.offline.plot({'data': trace_list, })

if __name__ == '__main__':
    main()
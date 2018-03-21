#!/usr/bin/env python
# -*- coding:utf-8 -*-

from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

def load_data(filename):
    datas = []
    with open(filename, "r") as f:
        for i in f.readlines():
            d = float(i.replace("\r\n", ""))
            datas.append(d)
    return datas

def normal_distribution(x, mu, sigma):
    return 1.0/np.sqrt(2*np.pi*sigma**2)*np.exp(-((x-mu)**2)/(2*sigma**2))

def main():
    datas = load_data("gauss-mle.txt")
    # サンプル平均の計算
    ave = sum(datas) / len(datas)
    # サンプル分散の計算
    vari = sum(map(lambda x:(x-ave)**2, datas)) / len(datas)
    
    sigma = sqrt(vari)
    # 描画するx軸の範囲. 3シグマ範囲とする.
    x_min, x_max = ave-3*sigma, ave+3*sigma
    x_range = np.linspace(x_min, x_max, 1000)
    # yの値を計算し,描画するy軸の範囲を決める.
    y_plot = normal_distribution(x_range, ave, sqrt(vari))
    y_min, y_max = min(y_plot)-0.1, max(y_plot)+0.1

    plt.xlabel("x")
    plt.ylabel("p(x)")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.vlines(ave, y_min, y_max, colors="b", linestyles="dashed")
    plt.grid(True)
    plt.plot(x_range, y_plot, label="$\\mu={:.5f}, \\sigma={:.5f}$".format(ave, sigma))
    plt.legend()
    plt.savefig("./likehood.eps")

if __name__=='__main__':
    main()
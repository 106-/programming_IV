#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math
from matrix import matrix
import matplotlib.pyplot as plt
import numpy as np

# ファイルからxのリストとtのリストをつくる
def load_plot(filename):
    x_points = []
    t_points = []
    with open(filename, "r") as f:
        for i in f.readlines():
            data = i.replace("\r\n","").split(" ")
            x_points.append(float(data[0]))
            t_points.append(float(data[1]))
    return x_points, t_points

# 最小二乗法を行う
def least_square(x_points, t_points, order):
    # Aijの値を返す関数
    def A(x_points, i, j):
        sum = 0
        for xn in x_points:
            sum += xn**(i+j)
        return sum
    # Tiの値を返す関数
    def T(x_points, t_points, i):
        sum = 0
        for xn, tn in zip(x_points, t_points):
            sum += xn**i*tn
        return sum
    m_A = matrix([[A(x_points, i, j) for j in range(order+1)] for i in range(order+1)])
    m_T = matrix([[T(x_points, t_points, i) for i in range(order+1)]])
    m_W = m_A.inverse()*m_T.transpose()
    return m_W.transpose().values[0]

# 得られた関数
def func(x, w_points):
    sum = 0
    for i,w in enumerate(w_points):
        sum += w*x**i
    return sum

def main():
    # ファイルの読み込み
    x_points, t_points = load_plot("curv-fit.txt")

    # 計算したい次元のリスト
    M_list = [1,2,3,4,9]
    
    # グラフを並べる数 1行に2つずつとする
    col = 2
    row = int(math.ceil(len(M_list) / col))

    fig, axes = plt.subplots(nrows=row,ncols=col,figsize=(4*col,3.5*row))
    fig.subplots_adjust(wspace=0.3, hspace=0.4)
    
    # 空白の部分は描画されないようにする
    if len(M_list)%2 != 0:
        axes[row-1][col-1].axis('off')

    for i,M in enumerate(M_list):
        # 係数の計算
        w_points = least_square(x_points, t_points, M)

        x_range = np.linspace(-0.1, 1.1, 1000)
        y_plot = func(x_range, w_points)

        # グラフの設定
        ax = axes[int(i/2)][i%2]
        ax.set_xlim([-0.1,1.1])
        ax.set_ylim([-1.2,1.2])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Least Square Method (M={})".format(M))
        ax.scatter(x_points, t_points, label="data")
        ax.plot(x_range, y_plot, label="M={}".format(M))
        ax.legend()
        ax.grid(True)
    fig.savefig("./least_square.eps")

if __name__=='__main__':
    main()
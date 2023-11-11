#!/usr/bin/env python3
"""
IZV cast1 projektu
Autor: Daria Dmitriievich /xdmitr00

Detailni zadani projektu je v samostatnem projektu e-learningu.
Nezapomente na to, ze python soubory maji dane formatovani.

Muzete pouzit libovolnou vestavenou knihovnu a knihovny predstavene na prednasce
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
from typing import List, Callable, Dict, Any


def integrate(f: Callable[[NDArray], NDArray], a: float, b: float, steps=1000) -> float:
    x = np.linspace(a, b, steps + 1)
    delta_x = (b - a) / steps
    mid = (x[:-1] + x[1:]) / 2
    integral_approximation = delta_x * np.sum(f(mid))
    return float(integral_approximation)


def calculate_integral(x_values, y_values):
    integral = np.trapz(y_values, x_values)
    return integral


def generate_graph(a, show_figure=True, save_path=None):
    x = np.linspace(-3, 3, 200)
    values_a = np.array(a)
    results = np.outer(np.power(values_a, 2), np.power(x, 3) * np.sin(x))
    plt.figure(figsize=(9, 5))
    for i, a in enumerate(values_a):
        plt.plot(x, results[i], label=f'$Y_{{{a}}}(x)$')
        plt.fill_between(x, 0, results[i], alpha=0.2)

    plt.xlabel('$x$')
    plt.ylabel('$f_a(x)$')
    plt.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.2, 0.2, 0.5, 0.9))

    values = [calculate_integral(x, results[i]) for i in range(len(values_a))]
    for i, integral in enumerate(values):
        last_x = float(x[-1])
        last_y = float(results[i][-1])
        plt.annotate(f'$\\int f_{{{values_a[i]}}}(x)dx={integral:.2f}$', (last_x, last_y))

    plt.ylim(0, 40)
    plt.xlim(-3, 5)
    x_ticks = range(-3, 4)
    plt.xticks(x_ticks)

    if show_figure:
        plt.show()

    if save_path:
        plt.savefig(save_path, format='png')


def generate_sinus(show_figure: bool = False, save_path: str | None = None):
    t = np.linspace(0, 100, 1000)

    f1 = 0.5 * np.cos(np.pi * t / 50)
    f2 = 0.25 * (np.sin(np.pi * t) + np.sin(1.5 * np.pi * t))

    y_sum = f1 + f2
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 14))
    fig.subplots_adjust(hspace=0.3)

    ax1.plot(t, f1, color='b')
    ax1.set_ylabel('$f_1(t)$')

    ax2.plot(t, f2, color='b')
    ax2.set_ylabel('$f_2(t)$')

    ax3.fill_between(t, y_sum, f1, where=(y_sum > f1), color='green', alpha=0.6)
    ax3.fill_between(t, y_sum, f1, where=(y_sum <= f1), color='red', alpha=0.6)

    for ax in [ax1, ax2, ax3]:
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.8, 0.8)
        ax.set_yticks([-0.8, -0.4, 0, 0.4, 0.8])
        ax.set_xlabel('t')

    if save_path:
        plt.savefig(save_path)

    if show_figure:
        plt.show()


def download_data() -> List[Dict[str, Any]]:
    station_records = []
    url = "https://ehw.fit.vutbr.cz/izv/st_zemepis_cz.html"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Nepodarilo se nacist stranku!")
    encoding = 'UTF8'

    soup = BeautifulSoup(response.content, "html.parser", from_encoding=encoding)
    table = soup.find_all("tr", attrs={'class': 'nezvyraznit'})
    for row in table:
        td_element = row.find_all("td")
        if len(td_element) >= 7:
            data = [td.text.strip() for td in td_element]
            position, lat_text, long_text, height_text = data[0], data[2][:-1], data[4][:-1], data[6]
            lat = lat_text.replace(',', '.')
            long = long_text.replace(',', '.')
            height = height_text.replace(',', '.')

            record = {
                'position': position,
                'lat': float(lat),
                'long': float(long),
                'height': float(height)
            }
            station_records.append(record)
    return station_records

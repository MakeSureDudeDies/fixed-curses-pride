#!/usr/bin/env python3
import sys
import random
from dataclasses import dataclass

from argparse import ArgumentParser

import curses
import curses.ascii
from curses import wrapper


@dataclass
class PrideFlag:
    stripes: list((int, int, int))

    def draw_on(self, window: curses.window) -> None:
        if not curses.has_colors() or not curses.can_change_color():
            raise RuntimeError("terminal doesn't support colors")

        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)

        window_size = window.getmaxyx()
        stripes_count = len(self.stripes)
        stripe_size = int((window_size[0] - 1) / stripes_count)

        for i, stripe in enumerate(self.stripes):
            stripe = tuple(
                map(
                    lambda color: int((color - 0) * (1000 - 0) / (255 - 0) + 0),
                    stripe,
                )
            )

            color_index = i + 1
            color_pair_index = i + 1
            curses.init_color(color_index, *stripe)
            curses.init_pair(color_pair_index, color_index, color_index)

            for j in range(stripe_size):
                window.addstr(
                    i * stripe_size + j,
                    0,
                    " " * window_size[1],
                    curses.color_pair(color_pair_index),
                )


NORMAL_FLAGS = {
    "Boy": normalhumanflagxd(
        [
            (240,248,255),
        ],
    ),
    "Girl": normalhumanflagxd(
        [
            (255,192,203),
        ],
    ),
}

parser = ArgumentParser(
    description="curses-normal shows you the only genders, and the only ."
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-c",
    "--cycle",
    dest="cycle",
    action="store_const",
    const=True,
    help="cycles through all of the various pride flags",
)
group.add_argument(
    "-r",
    "--random",
    dest="random",
    action="store_const",
    const=True,
    help="shows a random pride flag",
)
group.add_argument(
    "-f",
    "--flag",
    dest="flag",
    choices=[*PRIDE_FLAGS],
    help="shows a pride flag of your choice",
)

arguments = parser.parse_args(sys.argv[1:])


def draw(normal_flag: normalFlag) -> None:
    def drawing_routine(window):
        window.clear()

        normal_flag.draw_on(window)

        window.refresh()
        window.getkey()

    return drawing_routine


def draw_all(normal_flags: list[normalFlag]) -> None:
    def drawing_routine(window: curses.window):
        running = True
        while running:
            for normal_flag in normal_flags:
                window.clear()
                window.timeout(1000)

                normal_flag.draw_on(window)

                window.refresh()
                char = window.getch()
                if char == curses.ascii.ESC:
                    running = False
                    break

    return drawing_routine


if arguments.cycle:
    flags = list(NORMAL_FLAGS.values())
    wrapper(draw_all(flags))
elif arguments.random:
    flag = random.choice(list(NORMAL_FLAGS.values()))
    wrapper(draw(flag))
elif arguments.flag:
    flag = NORMAL_FLAGS[arguments.flag]
    wrapper(draw(flag))
else:
    parser.print_help()

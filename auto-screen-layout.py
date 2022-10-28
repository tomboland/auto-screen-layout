#!/bin/env python

from sh import xrandr, grep
from funcy import first, cat
from typing import Mapping, Any, Iterable, FrozenSet, Optional


def split_on_space(s): return s.split(' ')
def get_first_word(s): return first(split_on_space(s))


display_combinations: Mapping[FrozenSet, Mapping[str, Any]] = {
    frozenset(['DP-2']): {
        'DP-2': {'mode': '1920x1080', 'pos': '0x0', 'primary': True}
    },
    frozenset(['HDMI-0', 'DP-0', 'DP-2']): {
        'DP-0': {'mode': '3840x2160', 'pos': '2560x0', 'primary': True},
        'HDMI-0': {'mode': '2560x1440', 'pos': '0x0'},
        'DP-2': None
    },
    frozenset(['HDMI-0', 'DP-2']): {
        'HDMI-0': {'mode': '2560x1440', 'pos': '0x0', 'primary': True},
        'DP-2': None
    },
    frozenset(['DP-5', 'DP-2', 'HDMI-0']): {
        'DP-5': {'mode': '3840x2160', 'pos': '2560x0', 'primary': True},
        'HDMI-0': {'mode': '2560x1440', 'pos': '0x0'},
        'DP-2': None
    },
    frozenset(['eDP-1', 'HDMI-1', 'DP-2']): {
        'DP-2': {'mode': '3840x2160', 'pos': '2560x0', 'primary': True},
        'HDMI-1': {'mode': '2560x1440', 'pos': '0x0'},
        'eDP-1': None
    }
}


def construct_xrandr_display_args(display: str, display_args: Optional[Mapping[str, Any]]) -> Iterable[str]:
    if not display_args:
        return ['--output', display, '--off']
    return filter(None, [
        '--output', display,
        '--primary' if display_args.get('primary') else None,
        '--mode', display_args.get('mode'),
        '--pos', display_args.get('pos')
    ])


if __name__ == "__main__":
    display_info = grep(xrandr(), ' connected')
    display_names = frozenset(map(get_first_word, display_info))
    print(display_names)
    xrandr_args = list(cat([construct_xrandr_display_args(k, v)
                            for k, v in display_combinations[display_names].items()]))
    print(xrandr_args)
    xrandr('-s', '0')
    xrandr(xrandr_args)

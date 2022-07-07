from __future__ import annotations

from typing import Tuple

import yaml

from .config import c, Config


def wrapper() -> Config:
    """
    map config.yaml to config class
    """

    type_mapper = {
        str: 'str',
        float: 'float',
        int: 'int',
        dict: 'dict',
        tuple: 'tuple',
        bool: 'bool',
    }

    def parser(
        parameter: str, key: str, value: Tuple[str, dict], class_types: dict
    ):

        if isinstance(value, (str, int, float, bool)):
            exec(f'{parameter} = {type_mapper[class_types]}("{value}")')
        else:
            # class_types = class_types[key].__annotations__

            for k, v in value.items():
                new_parameter = parameter + f'.{k}'
                if eval(f'class_types["{k}"]') in type_mapper.keys():
                    new_class_types = eval(f'class_types["{k}"]')
                else:
                    new_class_types = eval(
                        f'class_types["{k}"].__annotations__'
                    )

                parser(
                    parameter=new_parameter,
                    key=k,
                    value=v,
                    class_types=new_class_types,
                )

    try:
        with open('config.yaml', 'r') as file:
            config_map = yaml.safe_load(file)
    except Exception:
        with open('example-config.yaml', 'r') as file:
            config_map = yaml.safe_load(file)

    for k, v in config_map['config'].items():
        class_types = Config.__annotations__
        if eval(f'class_types["{k}"]') in type_mapper.keys():
            class_types = eval(f'class_types["{k}"]')
        else:
            class_types = eval(f'class_types["{k}"].__annotations__')

        parameter = f'c.{k}'
        parser(
            parameter=parameter,
            key=k,
            value=v,
            class_types=class_types,
        )

    return c

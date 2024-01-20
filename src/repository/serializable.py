from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Type


class Serializable:
    def __init__(self) -> None:
        pass
    
    def serialize(self) -> dict[str, Any]:
        serialized: dict[str, Any] = {}
        
        for key, value in self.__dict__.items():
            if isinstance(value, str):
                serialized[key] = value
                continue
            
            if self._is_iterable(value):
                new_values: list[Any] = []
                for item in value:
                    if issubclass(item.__class__, Serializable):
                        new_values.append(item.serialize())
                    else:
                        new_values.append(item)
                        
                serialized[key] = new_values
                continue
            try:
                serialized[key] = value.serialize()
            except Exception as error:                
                serialized[key] = value

        return serialized
    
    def _is_iterable(self, value: Any) -> bool:
        try:
            iter(value)
            return True
        except TypeError:
            return False

# @dataclass
# class C(Serializable):
#     c: list[int]    
# @dataclass
# class B(Serializable):
#     c: C

# @dataclass  
# class A(Serializable):
#     b: B


# a = A(
#     B(
#         C([1, 2])
#         )
#     )
# print(a.serialize())
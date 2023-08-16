from typing import Dict, List, Optional, Set, Tuple, Union

from compiler.protobuf import Proto, ProtoMessage


class Element:
    def __init__(self, name: str, sql: Tuple[str, str], protomsg: ProtoMessage):
        self.name = name
        self.sql = sql
        self.protomsg = protomsg
        self.prev: List[Element] = []
        self.next: List[Element] = []

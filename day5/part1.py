from dataclasses import dataclass
from typing import List


@dataclass
class RangeMapEntry:
    dest_start: int
    source_start: int
    length: int

    @staticmethod
    def read(line: str):
        [dest, source, length] = [int(part) for part in line.strip().split(" ")]

        return RangeMapEntry(dest, source, length)


@dataclass
class Segment:
    start: int
    length: int


class RangeMap:
    def __init__(self, name: str, entries: List[RangeMapEntry]):
        # seed-to-soil map
        mapping = name.split(" ")[0]
        [from_entity, _, to_entity] = mapping.split("-")

        self.from_entity = from_entity
        self.to_entity = to_entity
        self.name = name
        self.entries = entries
        self.entries.sort(key=lambda entry: entry.source_start)

    def map(self, source: int) -> int:
        for entry in self.entries:
            if (
                source >= entry.source_start
                and source < entry.source_start + entry.length
            ):
                return entry.dest_start + source - entry.source_start

        return source

    def find_hit(self, source: int) -> RangeMapEntry:
        for entry in self.entries:
            if (
                source >= entry.source_start
                and source < entry.source_start + entry.length
            ):
                return entry

        return None

    def find_next_hit(self, source: int) -> RangeMapEntry:
        for entry in self.entries:
            if source < entry.source_start:
                return entry

        return None

    def map_segment(self, segment: Segment) -> List[Segment]:
        segments = []

        while segment.length > 0:
            entry = self.find_hit(segment.start)
            # there is no hit
            if entry is None:
                # find the next hit
                next_entry = self.find_next_hit(segment.start)

                # there is no next hit
                if next_entry is None:
                    # the segment corresponds to itself
                    segments.append(segment)
                    break

                # the segment corresponds to the gap between the current hit and the next hit
                to_add = Segment(
                    segment.start,
                    next_entry.source_start - segment.start,
                )
                segments.append(to_add)
                # cut off the segment
                segment = Segment(
                    segment.start + to_add.length,
                    segment.length - to_add.length,
                )
                continue

            # segment is entirely within the hit
            if segment.start + segment.length <= entry.source_start + entry.length:
                segments.append(
                    Segment(
                        entry.dest_start + segment.start - entry.source_start,
                        segment.length,
                    )
                )
                break

            # segment is partially within the hit
            to_add = Segment(
                entry.dest_start + segment.start - entry.source_start,
                entry.source_start + entry.length - segment.start,
            )
            segments.append(to_add)

            segment = Segment(
                segment.start + to_add.length,
                segment.length - to_add.length,
            )

        return segments

    def ordered_entries(self) -> List[RangeMapEntry]:
        return sorted(self.entries, key=lambda entry: entry.dest_start)

    @staticmethod
    def read(name: str, lines: List[str]) -> "RangeMap":
        entries = [RangeMapEntry.read(line) for line in lines]
        return RangeMap(name, entries)


@dataclass
class Almanac:
    maps: List[RangeMap]

    def map(self, source: int) -> int:
        for map in self.maps:
            source = map.map(source)

        return source


def read_seeds(file: str) -> List[int]:
    with open(file) as f:
        line = f.readline()

    return [int(part) for part in line[7:].strip().split(" ")]


def read_file(file: str) -> Almanac:
    with open(file) as f:
        current_group = []
        group_name = None
        maps: List[RangeMap] = []

        for line in f:
            if line.strip() == "" or line.startswith("seeds:"):
                continue

            if line.strip().endswith(":"):
                if len(current_group) > 0:
                    maps.append(RangeMap.read(group_name, current_group))

                current_group = []
                group_name = line.strip()[:-1]
                continue

            current_group.append(line)

        if len(current_group) > 0:
            maps.append(RangeMap.read(group_name, current_group))

    return Almanac(maps)


def main(file: str):
    almanac = read_file(file)
    seeds = read_seeds(file)
    locations = [almanac.map(seed) for seed in seeds]
    print(min(locations))


if __name__ == "__main__":
    main("day5/almanac.txt")

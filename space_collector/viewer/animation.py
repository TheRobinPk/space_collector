from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Iterable


class Animation:
    def __init__(
        self,
        start_value: int,
        end_value: int,
        duration: float = 1.0,
        start_time: float | None = None,
    ) -> None:
        self.duration = duration
        if start_time is None:
            self.start_time = perf_counter()
        else:
            self.start_time = start_time
        self.start_value = start_value
        self.end_value = end_value

    @property
    def end_time(self) -> float:
        return self.start_time + self.duration

    def value(self, time: float) -> int:
        factor = (time - self.start_time) / self.duration
        return int(self.start_value + (self.end_value - self.start_value) * factor)


@dataclass
class Step:
    duration: float
    value: float


class AnimatedValue:
    def __init__(self, initial_value: int = 0) -> None:
        self._animations: list[Animation] = []
        self._last_value = initial_value

    @property
    def value(self) -> int:
        current_time = perf_counter()
        to_be_removed = []
        for animation in self._animations:
            if animation.end_time < current_time:
                self._last_value = animation.end_value
                to_be_removed.append(animation)  # already finished
                continue
            if animation.start_time > current_time:
                continue  # not yet started
            self._last_value = animation.value(current_time)
        for animation in to_be_removed:
            self._animations.remove(animation)
        return self._last_value

    def add_animation(self, animation: Animation) -> None:
        self._animations.append(animation)

    def add_animations(
        self,
        initial_value: float,
        steps: Iterable[Step],
        start_time: float | None = None,
    ) -> None:
        if not steps:
            return
        self._animations.append(
            Animation(
                start_value=initial_value,
                start_time=start_time,
                end_value=steps[0].value,
                duration=steps[0].duration,
            )
        )
        for step in steps[1:]:
            last_animation = self._animations[-1]
            self._animations.append(
                Animation(
                    start_value=last_animation.end_value,
                    start_time=last_animation.end_time,
                    end_value=step.value,
                    duration=step.duration,
                )
            )

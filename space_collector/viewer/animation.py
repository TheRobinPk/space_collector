from __future__ import annotations

from time import perf_counter


class Animation:
    def __init__(
        self,
        start_value: float,
        end_value: float,
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
                to_be_removed.append(animation)  # already finished
            if animation.start_time > current_time:
                continue  # not yet started
            self._last_value = animation.value(current_time)
        for animation in to_be_removed:
            self._animations.remove(animation)
        return self._last_value

    def add_animation(self, animation: Animation) -> None:
        self._animations.append(animation)

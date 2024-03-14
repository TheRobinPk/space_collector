# Space collector

Space collector game

## TODO

- tracer les planetes puis les vaisseaux (pas par joueur, mais globalement)
- limiter dans la fréquence des radars
- Planet destruction with high energy attack?
- Des points si on tire sur quelqu'un ?
- When a team has collected all its planets, the game stops
- When the game ran 5 minutes, the game stops
- Limiter le rayon des radars pour les vaisseaux ennemis

## Rules

- Square 20 000 x 20 000 kms
- Random number of planets (between 2 and 8) and positions of planets, central symmetry
  so that every team "see" the same map
- Collect your planets with your collector
  - Slow speed
- Attack enemies with your five attackers
  - Fast speed
  - High energy attack < 5 000 kms
    - choose angle
    - 1 second to wait between fires of an attacker
- Explore with your explorer
  - Normal speed
  - See its planets and its spaceships
  - See enemy spaceships around him < 5 000 kms
- When a unit is touched by a high energy attack
  - Must return to its base to be repaired
    - Attacker can't attack
    - Explorators can't use their radar to see enemy spaceships
    - Collectors can't collect planets, they loose the collected planets (left in place)
- When a team has collected all its planets, the game stops
- When the game ran 5 minutes, the game stops

## Commands

### General syntax

`COMMAND {ship_id} {parameters}`

- `{ship_id}`: identifier of the spaceship
  - 1, 2, 3, 4, 5: attackers
  - 6, 7: explorers
  - 8, 9: collectors
- `{parameters}`: parameters of the command
  - `{angle}`: integer, degrees, between 0 and 359, counter clockwise, 0 pointing right
  - `{speed}`: integer in kms/s

Each command returns a response, made with:

- `{planet_id}` is between 0 and 65535
- `{ship_id}` is between 1 and 9
- `{abscissa}` and `{ordinate}` are between 0 and 19 999 ((0, 0) is the top left corner)

### Move

`MOVE {ship_id} {angle} {speed}`

Changes the speed and angle of the spaceship.

Maximum speed:

- 1 000 kms/s for collectors
- 2 000 kms/s for explorers
- 3 000 kms/s for attackers

Response is `OK`.

If a collector is less than 200 kms far from one of its planets, it collects the planet if it is not yet carrying a planet and it is not broken.

### Fire

`FIRE {ship_id} {angle}`

Fire a high energy attack, at `{angle}` angle. Length of the attack is 5 000 kms.

Any enemy spaceship less than 200 kms far from the high enery attack is now broken.

This command is only valid for an attacker.

Response is `OK` (even if the fire rate is not respected, and in this case the command is ignored).

### Radar

`RADAR {ship_id}`

Starts the radar of an explorer.

Response is a one line string. It is composed of several elements, separated by commas. The elements are:

- `P {planet_id} {abscissa} {ordinate} {ship_id} {saved}`: one of your not yet collected planets, at a given position, the `ship_id` is the ID of the collector that collected the plane, or -1 if not collected, `saved` is 1 when planet is at base station, otherwise 0
- `S {team} {ship_id} {abscissa} {ordinate} {broken}`: a spaceship, team 0 is yours, team 1 to 3 are opponents, broken is 0 or 1, 1 meaning that the ship was targeted by a high energy attack (your spaceships are always present even if the explorer is broken)
- `B {abscissa} {ordinate}`: your base station's position (always present in radar information)

If an explorer is broken, it can't see enemy spaceships. If not, it can see enemy spaceships less than 5 000 kms far from the explorer.

## Commands

### Installation

```shell
python3.11 -m venv venv
. venv/bin/activate
pip install --upgrade space_collector  # to play
pip install --upgrade space_collector[dev]  # to get dev dependencies
```

### Kill all clients and server

```shell
# For Linux and Mac
python -m space_collector.killall
```

### Install git hook

```shell
pre-commit install
```

### Lint

```shell
flake8
```

### Launch test

```shell
pytest
```

### Publish

```shell
python -m build
python3 -m twine upload dist/*
```

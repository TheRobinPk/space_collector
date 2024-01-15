# Space collector

Space collector game

## TODO

- tracer les planetes puis les vaisseaux (pas par joueur, mais globalement)

## Rules

- Square 20 000 x 20 000 kms
- Collect your planets with your collector
  - Slow speed
- Attack enemies with your three attackers
  - Fast speed
  - High energy attack < 5 000 kms
    - choose angle
    - 1 second to wait between fires
- Explore with your explorer
  - Normal speed
  - See its planets and all spaceships around him < 5 000 kms
- When a unit is touched by a high energy attack
  - Must return to its base to be repaired
    - Attacker can't attack
    - Explorators can't use their radar
    - Collectors can't collect planets, they loose the collected planets (left in place)
- Planet destruction with high energy attack?

## Commands

### General syntax

`COMMAND {ship_id} {parameters}`

- `{ship_id}`: identifier of the spaceship
  - 1, 2, 3, 4, 5: attackers
  - 6, 7: explorers
  - 8, 9: collectors
- `{parameters}`: parameters of the command
  - `{angle}`: integer, degrees, between 0 and 359, counter clockwise, 0 pointing right
  - `{speed}`: integer, between 0 and 2 000 kms/s

### Move

`MOVE {ship_id} {angle} {speed}`

Changes the speed and angle of the spaceship.

### Fire

`Fire {ship_id} {angle}`

Fire a high energy attack, at `{angle}` angle. Length of the attack is 5 000 kms.

## Commands

### Install git hook

```
hatch run pre-commit install
```

### Lint

```
hatch run pre-commit run --all-files
```

### Launch test

```
hatch run test
```

<div align="center">
  <h1>Sand</h1>

  <p>
    <strong>Sand pile simulation</strong>
  </p>

  <hr />
</div>

## About

Sand piles have been shown to exhibit [power-law](https://en.wikipedia.org/wiki/Power_law) dynamics, with small avalanches being extremely common and large avalanches extremely rare.

## Installation

Install using [Poetry](https://python-poetry.org/)

```bash
poetry install
```

## Usage

```bash
sand simulate --info --seed 42 --steps 1000 --size 20 --stability-threshold 4
```

## Output

As output you should see a 2D representation of the sand pile:

```txt
 [[ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
  [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
  [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
  [ 0  0  0  0  0  0  0  0  0  1  2  0  0  0  0  0  0  0  0  0]
  [ 0  0  0  0  0  0  1  1  2  4  5  2  0  0  0  0  0  0  0  0]
  [ 0  0  0  0  0  0  0  4  6  8  9  6  3  1  0  0  0  0  0  0]
  [ 0  0  0  0  0  3  4  7 10 12 12  9  6  3  0  0  0  0  0  0]
  [ 0  0  0  0  2  5  7 10 13 16 16 12 10  6  3  0  0  0  0  0]
  [ 0  0  0  0  3  6 10 13 16 20 19 17 13  9  6  3  0  0  0  0]
  [ 0  0  0  2  5  9 13 16 20 23 22 19 16 12  8  4  1  0  0  0]
  [ 0  0  1  0  3  7 11 15 19 22 24 20 16 12  8  4  1  0  0  0]
  [ 0  0  0  0  1  5  8 11 15 18 20 16 12  9  5  1  0  0  0  0]
  [ 0  0  0  1  3  2  5  8 11 14 16 12  9  5  2  1  0  0  0  0]
  [ 0  0  0  0  0  2  2  5  7 10 12  9  5  2  2  2  0  0  0  0]
  [ 0  0  0  0  0  0  0  3  4  6  8  5  2  2  0  0  0  0  0  0]
  [ 0  0  0  0  0  0  1  1  0  3  4  1  0  1  0  0  0  0  0  0]
  [ 0  0  0  0  0  0  0  0  0  0  1  1  0  0  0  0  0  0  0  0]
  [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
  [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]
  [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]]
```

as well as a frequency histogram of cascade sizes:

```txt
1: 156
2: 100
3: 41
4: 26
5: 13
6: 4
7: 1
9: 1
10: 1
```

Note that at each cascade size the frequency approximately halves. By updating the parameters of the simulation, you can change this coefficient. This is [scale-free](https://en.wikipedia.org/wiki/Scale-free_network)!

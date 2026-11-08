# Lotto frequency app

Find the seven most frequent numbers in the bundled NY Lotto CSV. Requires Python 3.8 or newer; no packages to install.

```sh
python lotto.py
```

By default, only the six values in `Winning Numbers` are counted. To include the separate bonus number:

```sh
python lotto.py --include-bonus
```

You can also supply another CSV with the same column names:

```sh
python lotto.py path/to/draws.csv
```

The app prints seven numbers in descending frequency, with occurrence counts and the total number of draws analyzed. Ties are resolved by smaller number first. `Draw Date` and `Extra #` are excluded. Invalid rows produce an error with the CSV line number.

Historical frequency does not predict future lottery results.

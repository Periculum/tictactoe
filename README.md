# tictactoe
This project was developed as part of an article that appeared in c't magazine and on heise+ to show the algorithms Minimax, Negamax and Minimax with Alpha-Beta Pruning on the example of TicTacToe.


## Run

You need [Python](https://www.python.org/downloads/) and [Pipenv](https://pipenv.pypa.io/en/latest/installation.html) to run the Code. 

### Linux, macOS, Windows

Install dependencies (PyGame):

```bash
pipenv install
```

Run:

```bash
pipenv run python tictactoe.py
```

Additional you have the following parameters:
```
-c, --computer        Let the computer make the first move instead of the player.
-m {random,minimax,minimax-ab,negamax}, --mode {random,minimax,minimax-ab,negamax} Select the algorithm the computer will use to make moves.
```

## Copyright

Copyright ©️ 2025 Wilhelm Drehling, Heise Medien GmbH & Co. KG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

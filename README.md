# Matrix Game - Original

This is an original pattern-matching game developed with python. The game includes a replay feature by which games and their replays are stored in a MySQL database.

The project demonstrates knowledge and application of matrix operations, MySQL, UI, and solver development.

## Requirements:
- #### python 3.x
- #### Tkinter 8.6
- #### numpy 1.26.2
- #### mysql-connector-python 8.2
- #### protobuf



## Setup:

1. Create a virtual environment using the latest release of virtualenv:

``` bash
> pip install virtualenv --upgrade
> virtualenv venv
```

_If there are problems with installing tkinter:_
- Install tkinter package. Ex: Homebrew:
``` bash
> brew install python-tk
```
- Then create the virtual environment as follows:
```
> virtualenv venv --system-site-packages
```

2. Access the virtual environment `./venv`
``` bash
> source ./venv/bin/activate
```

3. Install the requirements:
```bash
> pip install -r requirements.txt
```

4. Run `./initDB.sql` in MySQL to setup the database.

5. Save MySQL credentials (host, user, passwd) in `.env`:

Ex:
``` env
host=localhost
user=root
passwd=password
```


## Execution:

#### 

#### To run the game, execute the following command:

``` bash
> python3 main.py
```

## How to Play:

#### Detect ABBA-patterns:

_an ABBA pattern is a group of four cells in the matrix that form a rectangle such that the diagonally opposite cells display the same shape._

#### 3-to-1 rule:

_ABBA patterns must be colored such that exactly three of the cells share the same color (red/blue) while the fourth has the opposite color._

#### Objective:

_When the matrix has been fully colored, click the `check` button_

**There is only one solution!**

### ***Watch your replays, and strive for faster plays!***


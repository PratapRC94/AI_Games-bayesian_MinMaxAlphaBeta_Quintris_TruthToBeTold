# Part 1: Raichu

Raichu is a popular childhood game played on an n x n grid (where n >= 8 is an even number) with three kinds of pieces (Pichus, Pikachus, and Raichus) of two different colors (black and white). Initially the board starts empty, except for a row of white Pikachus on the 2nd row of the board, a row of white Pichus on the 3rd row of the board, and a row of black Pichus on row n - 2 and a row of black Pikachus on row n - 1.

Two players alternate turns, with White going first.
In any given turn, a player can choose a single piece of their color and move it according to the rules of that piece.

**A Pichu** can move in one of two ways:
* one square forward diagonally, if that square is empty.
* "jump" over a single Pichu of the opposite color by moving two squares forward diagonally, if that square is empty. The jumped piece is removed from the board as soon as it is jumped.

**A Pikachu** can move in one of two ways:
* 1 or 2 squares either forward, left, or right (but not diagonally) to an empty square, as long as all squares in between are also empty.
* "jump" over a single Pichu/Pikachu of the opposite color by moving 2 or 3 squares forward, left or right (not diagonally), as long as all of the squares between the Pikachu's start position and jumped piece are empty and all the squares between the jumped piece and the ending position are empty. The jumped piece is removed as soon as it is jumped.

**A Raichu** is created when a Pichu or Pikachu reaches the opposite side of the board (i.e. when a Black Pichu or Pikachu reaches row 1 or a white Pichu or Pikachu reaches row n). When this happens, the Pichu or Pikachu is removed from the board and subsituted with a Raichu. Raichus can move as follows:
* any number of squares forward/backward, left, right or diagonally, to an empty square, as long as all squares in between are also empty.
* "jump" over a single Pichu/Pikachu/Raichu of the opposite color and landing any number of squares forward/backward, left, right or diagonally, as long as all of the squares between the Raichu's start position and jumped piece are empty and all the squares between the jumped piece and the ending position are empty. The jumped piece is removed as soon as it is jumped.


Note the hierarchy: Pichus can only capture Pichus, Pikachus can capture Pichus or Pikachus, while Raichus can capture any piece. The winner is the player who first captures all of the other player's pieces.

Your task is to write a Python program that plays Raichu well. Your program should accept a command line argument that gives the current state of the board as a string of .'s, w's, W's, b's, B's, @'s, and $'s, which indicate which squares have no piece, a white Pichu, a white Pikachu, a black Pichu, a black Pikachu, a white Raichu and a black Raichu respectively, in row-major order. For example, if n = 8, then the encoding of the start state of the game would be: **........W.W.W.W..w.w.w.w................b.b.b.b..B.B.B.B........**

More precisely, your program will be called with four command line parameters: (1) the value of n, (2) the current player (w or b), (3) the state of the board, encoded as above, and (4) a time limit in seconds. Your program should then decide a recommended single move for the given player with the given current board state, and display the new state of the board after making that move. Displaying multiple lines of output is fine as long as the last line has the recommended board state. The time limit is the amount of time that your program should expect to have to make its decision; our testing code will kill your program at that point, and will use whichever was the last move your program recommended. For example, a sample run of your program might look like:

```
prataprc94@Prataps-MacBook-Pro part1 % python3 raichu.py 8 w '........W.W.W.W..w.w.w.w................b.b.b.b..B.B.B.B........' 10

Searching for best move for w from board state:
........
W.W.W.W.
.w.w.w.w
........
........
b.b.b.b.
.B.B.B.B
........
Here's what I decided:
..........W.W.W..w.w.w.wW...............b.b.b.b..B.B.B.B........
```
Your program should work for any reasonable value of n and reasonable time limit, although we plan to test it only for values of n close to 8 and time limits around 10-30 seconds.

## Solution

* The goal of this problem is to find the next best possible move by the max player and return a new board configuration given the initial board configuration.

### Strategy

* Since there are 3 different kind of pieces of white and black colours - pichu, pikachu and raichu and each of these has different moving and attacking criteria as mentioned in the problem statement, we need to build functions for each of those moves which will be considered as the **successor states** of any particular board configuration.
* Due to the involvement of 3 different kind of pieces and a board of n>=8,the game tree can grow very long and so to evaluate the utility of the board for any given state, we created a Utility calculation function **get _Utility** whether it favors black or white. So, if the max player is white then the utility should be positive for white so that it is likely to win. That prevents the game to dig down to the terminal state and it traverse to a specific depth to calculate the utility value and returns back which selects the best possible move for the max player using the minimax algorithm.
* The Minimax algorithm is developed with alpha beta pruning technique which will basically prune the parts of the tree for which alpha is greater than equal to beta.

### Algorithm

1. There are 3 different characters of white and black colours - thus 6 different functions are defined to find the all possible moves by each of these characters.

* **white_pichu_move(board,N)** - This function finds all possible movements and attacks by a white pichu (w) and has the following 4 conditions: *white pichu moves forward diagonally-left, white pichu moves forward diagonally-right, white pichu attacks forward diagonally-left, white pichu attacks forward diagonally-right*.

* **black_pichu_move(board,N)** - This function finds all possible movements and attacks by a black pichu (b) and has the following 4 conditions: *black pichu moves forward diagonally-left, black pichu moves forward diagonally-right, black pichu attacks forward diagonally-left, black pichu attacks forward diagonally-right*.

* **white_pikachu_move(board,N)** - This function finds all possible movements and attacks by a white pikachu (W) and has the following 6 conditions: *white pikachu moves forward 1 or 2 squares, white pikachu moves left 1 or 2 squares, white pikachu moves right 1 or 2 squares, white pikachu attacks forward and moves 2 or 3 squares, white pikachu attacks left and moves 2 or 3 squares, white pikachu attacks right and moves 2 or 3 squares*.

* **black_pikachu_move(board,N)** - This function finds all possible movements and attacks by a black pikachu (B) and has the following 6 conditions: *black pikachu moves forward 1 or 2 squares, black pikachu moves left 1 or 2 squares, black pikachu moves right 1 or 2 squares, black pikachu attacks forward and moves 2 or 3 squares, black pikachu attacks left and moves 2 or 3 squares, black pikachu attacks right and moves 2 or 3 squares*.

* **white_raichu_move(board,N)** - This function finds all possible movements and attacks by a white raichu (@) and has the following 12 conditions: *white raichu moves forward any number of squares, white raichu moves forward diagonally-left any number of squares, white raichu moves forward diagonally-right any number of squares, white raichu moves backwards any number of squares, white raichu moves left any number of squares, white raichu moves right any number of squares, white raichu attacks forward and moves any number of squares beyond opponent, white raichu attacks forward diagonally-left and moves any number of squares beyond opponent, white raichu attacks forward diagonally-right and moves any number of squares beyond opponent, white raichu attacks backward and moves any number of squares beyond opponent, white raichu attacks left and moves any number of squares beyond opponent, white raichu attacks right and moves any number of squares beyond opponent*.

* **black_raichu_move(board,N)** - This function finds all possible movements and attacks by a black raichu ($) and has the following 12 conditions: *black raichu moves forward any number of squares, black raichu moves forward diagonally-left any number of squares, black raichu moves forward diagonally-right any number of squares, black raichu moves backwards any number of squares, black raichu moves left any number of squares, black raichu moves right any number of squares, black raichu attacks forward and moves any number of squares beyond opponent, black raichu attacks forward diagonally-left and moves any number of squares beyond opponent, black raichu attacks forward diagonally-right and moves any number of squares beyond opponent, black raichu attacks backward and moves any number of squares beyond opponent, black raichu attacks left and moves any number of squares beyond opponent, black raichu attacks right and moves any number of squares beyond opponent*.

2. Calculate the utility value for a particular depth of the game tree using **get_Utility(board,max_player,N)** - Calculates the utility value for a particular board and the given max player. The utility value will change depending on the max player. 
3. Check for the terminal state using **get_Terminal_State(board,max_player)** if count of pichu,pikachu and raichu of white colour is 0 and the black colour one is max player, then black is the the winner and returns True. Similarly, if count of pichu,pikachu and raichu of black colour is 0 and the white colour one is max player, then white is the the winner and returns True. otherwise return False.
4. The successor function **get_Successors(board, player,N)** - if the player is white, then it calls for all the possible moves by a white pichu, pikachu and raichu and then combines all the board configurations from the moves to return the successors of a particular board configuration. for example, if the player is white, then it returns *white_pichu_move(board,N)+white_pikachu_move(board,N)+white_raichu_move(board,N)*. Similarly it does for black player.
5. For a basic run within 2-3 minutes, the main function calls the **find_best_move(board,N,player,timelimit,depth)** iteratively for a depth ranging from 2 to 5. It returns the best possible moves at each depths.
6. The find_best_move(board,N,player,timelimit,depth) basically declares the max and min player based on the user input for player and calls *alpha_beta_pruning(board,N,max_player,min_player,depth)*
7. **alpha_beta_pruning(board,N,max_player,min_player,depth)** sets the alpha and beta value as -inf and inf respectively and calls the *min_state(board, max_player, min_player, alpha, beta, depth, N)* and tries to maximize the value it returns.
8. **min_state(board, max_player, min_player, alpha, beta, depth, N)** - it first checks if the board has depth = 0 or reached terminal state otherwise calls the *max_state(board, max_player, min_player, alpha, beta, depth, N)* which returns the value for which the maximum is taken and stored in val. The alpha beta check is applied and if alpha is greater than or equal to beta then the branch is pruned.
9. **max_state(board, max_player, min_player, alpha, beta, depth, N)** - it first checks if the board has depth = 0 or reached terminal state otherwise calls the *min_state(board, max_player, min_player, alpha, beta, depth, N)* which returns the value for which the minimum is taken and stored in val. The alpha beta check is applied and if alpha is greater than or equal to beta then the branch is pruned.

### **Sample Output**

```
prataprc94@Prataps-MacBook-Pro part1 % python3 raichu.py 8 w '........W.W.W.W..w.w.w.w................b.b.b.b..B.B.B.B........' 10
Searching for best move for w from board state: 
........
W.W.W.W.
.w.w.w.w
........
........
b.b.b.b.
.B.B.B.B
........
Here's what I decided:
Best move for w till depth: 2
..........W.W.W..w.w.w.wW...............b.b.b.b..B.B.B.B........
Best move for w till depth: 3
........W.W.WW...w.w.w.w................b.b.b.b..B.B.B.B........
Best move for w till depth: 4
........W.W.W....w.w.w.w......W.........b.b.b.b..B.B.B.B........
Run time :  105.926
```


# Part 2: The Game of Quintris

The game of Quintris will likely seem familiar. It starts off with a blank board. One by one, random pieces
(each consisting of 5 blocks arranged in different shapes) fall from the top of the board to the bottom. As
each piece falls, the player can change the shape by rotating it or flipping it horizontally, and can change its
position by moving it left or right. It stops whenever it hits the ground or another fallen piece. If the piece
completes an entire row, the row disappears and the player receives a point. The goal is for the player to
score as many points before the board fills up.

Your goal is to write a computer player for this game that scores as high as possible. We've provided a really
simple automatic player that can be run using the command line options computer animated and computer
simple. The code for this is in tetris.py, whereas the other python files contain the “back end" code that
runs the game. You should not modify the other source code files.
We'd recommend starting with the simple version as opposed to the animated version. In the simple version,
your program issues a sequence of commands which are then executed immediately before the piece begins to
fall. This is simpler but prevents your program from making complicated moves (like moving left and right
as the piece falls to try to wedge a piece into an awkward spot in the board). Then, consider the animated
version, which also introduces an implicit time limit (since your decisions have to be made before the piece
reaches the bottom of the board.)

This version of Tetris has one twist which you may want to use to get as high a score as possible: the falling
pieces are not chosen uniformly at random but based on some distribution which your program is not allowed
to know ahead of time. However, it may be able to estimate the distribution as it plays, which may let it
make better decisions over time.

## Solution:
The goal here is to get the highest score possible while having the AI play the game.

I defined a function **successor()** to generate all the successor function. Taking help of code from the **QuintrisGame.py** file for rotating a piece, flipping horizontally, checking for collision and placing a piece at a particular point, I build the successor functions such that it tries to fit in the current piece, and all its orientations, into all suitable spaces on the board. Along with this I also added to it the moves it needs to make, in order to reach that particular state, and stored it as a tuple.

Next I defined a heuristic function **heuristic()** which takes in the board as an input and outputs the calculated heuristic function. To calculate the heuristic I have taken a few parameters into consideration. 
1. **Holes**: This is the number of holes created in a particular board. As we know, the lesser holes the better.
2. **Lines Cleared**: This is the number of full lines that the particular board creates. We will want to maximize this value.
I assigned weights to each parameter making sure the holes are negatively weighted and the lines cleared are positively weighted.

The function returns the weighted sum of the parameters.

I implemented the logic for the AI using a normal fringe. I store the successor functions for the current board and given piece in the fringe, and calculate the heuristic for each board. 
The moves from the board that has the best heuristic function is returned by the **get_moves()** function.

# Part 3:

Many practical problems involve classifying textual objects — documents, emails, sentences, tweets, etc. — into two specific categories — spam vs nonspam, important vs unimportant, acceptable vs inappropriate, etc. Naive Bayes classifiers are often used for such problems. They often use a bag-of-words model, which means that each object is represented as just an unordered “bag” of words, with no information about the grammatical structure or order of words in the document. Suppose there are classes A and B.
Using the Naive Bayes assumption, the odds ratio can be factored into P(A), P(B), and terms of the form P(wi|A) and P(wi|B). These are the parameters of the Naive Bayes model.
As a specific use case for this assignment, we’ve given you a dataset of user-generated reviews. User-generated reviews are transforming competition in the hospitality industry, because they are valuable for both the guest and the hotel owner. For the potential guest, it’s a valuable resource during the search for an overnight stay. For the hotelier, it’s a way to increase visibility and improve customer contact. So it really affects both the business and guest if people fake the reviews and try to either defame a good hotel or promote a bad one. Your task is to classify reviews into faked or legitimate, for 20 hotels in Chicago.

## Solution:
The goal is to find if the review is truthful or deceptive.
With given training data and test data, accuracy = 82.50% ( Used Naive Bayes and Laplace Smoothing )

We are providing a training data with sample deceptive and truthful reviews, on basis of which we can find the probabilities of occurence of a word in the review class.
Based on the naive bias algorithm, we can compute posterior for both class of reviews, i.e.
    P(Y=truthful| w1, w2,... ,wn) = ( P( w1, w2,... ,wn|Y="truthful") P(Y="truthful") ) / P(w1,..,wn)
    P(Y=deceptive| w1, w2,... ,wn) = ( P( w1, w2,... ,wn|Y="deceptive") P(Y="deceptive") ) / P(w1,..,wn)
where, 
    w1, w2,..,wn = words in the review sentence
    Y="truthful" = Probability of review being truthful ( from training data )
    y="deceptive" = Probability of review being deceptive ( from training data )
termed as,
    P( w1, w2,... ,wn|Y="truthful") = likelihood
    P( w1, w2,... ,wn|Y="deceptive") = likelihood
    P(w1,..,wn) = prior
    P(Y="deceptive") = prior
    P(Y="truthful") = prior
    P(Y=truthful| w1, w2,... ,wn) = posterior
    P(Y=deceptive| w1, w2,... ,wn) = posterior

Then, we compare both the posteriors, and one with high value, gets classified into that class.

Here, we can ignore denominator as both the posteriors have same denominator.

In Naive Bayes, we can assume conditional independence among calculating likelihood, which results in : 
    P( w1, w2,... ,wn|Y="truthful") = P(w1|Y="truthful")*P(w2|Y="truthful")*...*P(w3|Y="truthful") 
    P( w1, w2,... ,wn|Y="deceptive") = P(w1|Y="deceptive")*P(w2|Y="deceptive")*...*P(w3|Y="deceptive")

We are using here,
Laplace Smoothing, to handle the cases where word doesnt exists in the training data. It is used to control high bias and variance. It gives a small non-zero probability to words not existing in training set, so the posterior probability doesnt suddenly drops to 0.
It allows non-zero probabilities of the word which do not exists in the training data.
Using it, we can represent:
    P(word|Y="truthful") = (Count of Y="truthful" containing word + smoothingParameter) / ( Number of Y="truthful" + numberOfdataFeatures )

    (word|Y="deceptive") = (Count of Y="deceptive" containing word + smoothingParameter) / ( Number of Y="deceptive" + numberOfdataFeatures )

### Coding Steps:
resulList = []
1. Prepare training data by categorizing words in training reviews, and keeping count of reviews containing them of eeach class
2. Iterating through every review in test data :
        1. Cacluate likelihood ( using naive bias, assuming conditioning probability )
        2. Using Laplase smoothening, so, to handle the cases of words not existing in training set
        3. Considering smootheningParameter =1 
            ( Here, we are ignoring calculating denominator, as both posteriors have common denominator).
3. Matching posteriors for both classes, and one with highest values, get pushed in resultList.
4. return resultList

### **Sample Output**
Classification accuracy = 82.50%







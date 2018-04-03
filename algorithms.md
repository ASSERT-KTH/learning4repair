# All algorithm

Here are descriptions of all algorithm implemented:

1. [guessFirst.py](#guessfirst)
2. [guessMiddle.py](#guessmiddle)
3. [guessLast.py](#guesslast)
4. [randomGuess.py](#randomguess)
5. [maximumError.py](#maximumerror)
6. [maxLcsDistance.py](#maxlcsdistance)
7. [minEditDistance.py](#mineditdistance)
8. [minAvgEmbed.py](#minavgembed)
9. [minSumEmbed.py](#minsumembed)
10. [minEmbedDistance.py](#minembeddistance)
11. [minEmbedAndEditDistance.py](#minembedandeditdistance)
12. [tfidf_javalang.py](#tfidf_javalang)
13. [tfidf_split.py](#tfidf_split)

## guessFirst
Always predict the first line

## guessMiddle
Always predict the line in the middle

## guessLast
Always predict the last line

## randomGuess
Predict random lines

## maximumError
Predict the farthest line from the solution

## maxLcsDistance
Used the idea from https://en.wikipedia.org/wiki/Longest_common_subsequence_problem.
Problems with this approach:
* Order matters! dis("ab", "ba")=1

## minEditDistance
Used the idea from https://en.wikipedia.org/wiki/Edit_distance.
Problem with this approach:
* Too slow
* Order matters! dis("ab", "ba")=2

## minAvgEmbed
Use generated embeddings from word2vec, take the average word embedding and use cosine similarity.
Problem with this approach:
* Depends on the learned embeddings

## minSumEmbed
Use generated embeddings from word2vec, take the sum of all word embedding and use cosine similarity.
Problem with this approach:
* Depends on the learned embeddings

## minEmbedDistance
Used the idea from http://proceedings.mlr.press/v37/kusnerb15.pdf
Problem with this approach:
* Depends on the learned embeddings
* Cannot handle 'UNK'

## minEmbedAndEditDistance
Used the idea from http://proceedings.mlr.press/v37/kusnerb15.pdf and tried to solve the 'UNK' problem by incorporating edit distance between 'UNK' 
Problem with this approach:
* Depends on the learned embeddings
* How to combine minimum cumlative embedding distance and edit distance

## tfidf_javalang
Generate TF-IDF vector for each line. We see each line of code as a document. The whole program is tokenized by javalang. We used cosine similarity to compare.
Problem with this appraoch:
* javalang ignores all comments

## tfidf_split
Generate TF-IDF vector for each line. We see each line of code as a document. The whole program is tokenized by split(), right now we split with "[,.();{}_\[\]\+\-\*\/&|\t\n\r ]". We used cosine similarity to compare.
Problem with this appraoch:
* Some tokens might be useful but we ignore them.


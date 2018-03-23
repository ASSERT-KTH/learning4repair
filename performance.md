## Performance of baseline algorithms

Here are the performance of each baseline algorithms. Observe that different algorithms have different number of files, the reason can be 1) exception 2) speed of algorithm. e.g. minEditDistance is too slow to process all files.

|       Type        | Algorithm | Performance on icse15-1LineRep |
| ----------------- | --------- | ----------- |
| Replaced one line | maximumError | Total files: 4454<br>Cumulative line error: 4453.99989692 (the lower, the better)<br>Top 1 accuracy: 0.0 (the higher, the better) |
| | minEditDistance | Total files: 100<br>Cumulative line error: 7.28478246779 (the lower, the better)<br>Top 5 accuracy: 0.92 (the higher, the better) |
| | tfidf_javalang | Total files: 4444<br>Cumulative line error: 340.280612305 (the lower, the better)<br>Top 5 accuracy: 0.921917191719 (the higher, the better) |
| | tfidf_split | Total files: 4454<br>Cumulative line error: 188.373463108 (the lower, the better)<br>Top 5 accuracy: 0.956668163449 (the higher, the better) |
| | minAvgEmbed (50000 files, 200 vol) | Total files: 4425<br>Cumulative line error: 1120.2679289 (the lower, the better)<br>Top 5 accuracy: 0.740790960452 (the higher, the better) |
| | minAvgEmbed (100000 files, 500 vol) | Total files: 4425<br>Cumulative line error: 997.53704855 (the lower, the better)<br>Top 5 accuracy: 0.766553672316 (the higher, the better) |
| | minAvgEmbed (100000 files, 10000 vol) | Total files: 4425<br>Cumulative line error: 648.657417465 (the lower, the better)<br>Top 5 accuracy: 0.849039548023 (the higher, the better) |
| | minAvgEmbed (100000 files, 50000 vol) | Total files: 4425<br>Cumulative line error: 1026.05325866 (the lower, the better)<br>Top 5 accuracy: 0.760677966102 (the higher, the better) |
| | minSumEmbed (100000 files, 10000 vol) | Total files: 4425<br>Cumulative line error: 648.657417465 (the lower, the better)<br>Top 5 accuracy: 0.849039548023 (the higher, the better) |
| | minEmbedDistance (100000 files, 500 vol) | Total files: 4418<br>Cumulative line error: 961.688155817 (the lower, the better)<br>Top 5 accuracy: 0.77931190584 (the higher, the better) |
| | minEmbedDistance (100000 files, 10000 vol) | Total files: 4420<br>Cumulative line error: 646.443742894 (the lower, the better)<br>Top 5 accuracy: 0.850904977376 (the higher, the better) |
| | minEmbedAndEditDistance (100000 files, 10000 vol) | Total files: 4425<br>Cumulative line error: 393.993823742 (the lower, the better)<br>Top 5 accuracy: 0.908926553672 (the higher, the better) |
| | minEmbedAndEditDistance (100000 files, 10000 vol, split) | Total files: 4425<br>Cumulative line error: 330.4746716 (the lower, the better)<br>Top 5 accuracy: 0.922937853107 (the higher, the better) |
| | randomGuess | Total files: 4454<br>Cumulative line error: 4254.41643804 (the lower, the better)<br>Top 5 accuracy: 0.0289627301302 (the higher, the better) | Total files: 4425<br>Cumulative line error: 648.657417465 (the lower, the better)<br>Top 5 accuracy: 0.849039548023 (the higher, the better) |
| Replaced one hunk | minAvgEmbed (50000 files, 200 vol) | Total files: 8970<br>Top 5 accuracy: 0.439687848384 |
| | minAvgEmbed (100000 files, 500 vol) | Total files: 8970<br>Top 5 accuracy: 0.46220735786 |
| | randomGuess.py | Total files: 9504<br>Top 5 accuracy: 0.0133627946128 |
| | tfidf_javalang | Total files: 9306<br>Top 5 accuracy: 0.538899634644 |
| | tfidf_split | Total files: 9504<br>Top 5 accuracy: 0.645728114478 |

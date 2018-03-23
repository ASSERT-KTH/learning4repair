* March 6 2018
  * Edit distance is too slow
  * Tfidf+cosine achieves 80% perfect predictions on the replacement benchmark with 4454 tasks)!
  
* March 23 2018
  * naive split is better than languageg tokenizer
  * WMD distance works well on icse15-1LineRep
  * WMD-distance combined wit hedit distance in a pseudo geometric mean works even better on icse15-1LineRep
  * Decision: move from cumulative loss to average loss (resulting in loss in [0,1] thanks to tanh)
  * Decision: when an algorithm fails to output something, we take the worst case loss, which is one
 

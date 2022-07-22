(declare-fun x () String)
(declare-fun y () String)
(declare-fun z () String)

(assert (= x x))
(assert (= "AA" "BB"))
(assert (str.contains (str.replace x y) (str.++ x y)))
(assert (= (str.++ x y) (str.replace x y)))
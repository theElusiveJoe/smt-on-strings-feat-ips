(declare-fun x () String)
(declare-fun y () String)
(declare-fun z () String)

(assert (not (= x y)))
(assert (not (str.contains x y)))
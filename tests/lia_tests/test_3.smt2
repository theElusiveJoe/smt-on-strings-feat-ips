(declare-fun x () String)
(declare-fun y () String)
(declare-fun z () String)
(declare-fun t () String)

(assert (= x y ))
(assert (not (str.contains x y)))
(assert (str.contains z t))

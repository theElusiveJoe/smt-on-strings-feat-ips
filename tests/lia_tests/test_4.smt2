(declare-fun x () String)
(declare-fun y () String)
(declare-fun z () String)
(declare-fun t () String)

(assert (or (= x y ) (= y z)))
(assert (or (not (= z t)) (str.contains z t)))

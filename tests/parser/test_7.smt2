(declare-fun x () String)
(declare-fun y () String)
(declare-fun z () String)

(assert (= (str.++ x y) z))
(assert (or (= (str.++ x y) z) (= y z)))
(assert (not (str.contains (str.++ x y) z)))


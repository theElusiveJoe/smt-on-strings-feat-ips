(declare-fun x () String)
(declare-fun y () String)
(declare-fun z () String)
(declare-fun t () String)

(assert (or 
    (= z (str.++ x y))
    (= t (str.++ x z))
))
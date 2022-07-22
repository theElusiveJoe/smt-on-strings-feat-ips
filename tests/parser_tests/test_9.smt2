вложенные or
(declare-fun x () String)
(declare-fun y () String)
(declare-fun z () String)
(declare-fun t () String)

(assert (or (or (= x y) (= x z)) (not (= z y))))
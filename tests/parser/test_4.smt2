(declare-fun x () String)
(declare-fun y () String)
(declare-fun z () String)
(declare-fun t () String)

(assert ( =
    (str.++ x y)
    (str.replace_all y (str.++ x z "ABC") "TTT")
))
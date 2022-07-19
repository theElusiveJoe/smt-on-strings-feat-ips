два одинаковых литерала не должны повторяться
(declare-fun x () String)
(declare-fun y () String)
(declare-fun z () String)
(declare-fun t () String)

(assert (= x y))
(assert (= y z))
(assert (or (= z t) (not(= x y))))
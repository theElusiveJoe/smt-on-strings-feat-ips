;два одинаковых клоза и предиката не должны повторяться
(declare-fun x () String)
(declare-fun y () String)
(declare-fun z () String)
(declare-fun t () String)

(assert (not (= (str.++ x y) z)))
(assert (str.contains (str.++ x y) t ))
(assert (= (str.replace (str.replace_all "AAAA" "BBB" "CCC") x y) z))
(assert (not (= (str.++ x y) z)))
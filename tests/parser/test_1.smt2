(declare-fun x () String)
(declare-fun y1 () 


            String)
(declare-fun y2 () String)
(declare-fun y3 () String)
(declare-fun z1 () String)
(declare-fun z2 () String)
(declare-fun z3 () String)
(assert (or 
    (= x (str.++ y1 "A" y2 "B" y3)) 
(= x (str.++ z1 "B" z2 "A" z3))))
              
                 (assert                     (or 
(not (str.contains x "A")) (not (str.contains x "B"))))
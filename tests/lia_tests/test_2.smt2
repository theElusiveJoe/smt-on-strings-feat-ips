(declare-fun x () String)
(declare-fun y () String)
(declare-fun z () String)
(declare-fun t () String)

(assert 
        (=    
            "ABC"   
            (str.++ (str.replace_all x y z) "AB")
        )
)

(assert 
        (str.contains     
            (str.++ (str.replace_all x y z) "AB")
            
            (str.++ (str.replace (str.replace t z y) x y) "ADC" z) 
            ))

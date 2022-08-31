; CONFIG:  constant_min_len : 3
; CONFIG:  constant_max_len : 7
; CONFIG:  variables_number_low_limit : 3
; CONFIG:  variables_number_high_limit : 5
; CONFIG:  max_string_depth : 2
; CONFIG:  max_concat_number : 4
; CONFIG:  atoms_number_low_limit : 10
; CONFIG:  atoms_number_high_limit : 30
; CONFIG:  asserts_number : 30
; CONFIG:  literals_in_assert_low_limit : 2
; CONFIG:  literals_in_assert_high_limit : 4

(set-logic QF_SLIA)
(declare-fun z () String)
(declare-fun y () String)
(declare-fun x () String)
(declare-fun w () String)

(assert (or
    (not (str.contains y (str.++ z x z)))
    (= (str.++ "ABAB" y x) z)
    (not (= w x))
    (= x (str.++ "ACCCBBA" y y))
  )
)
(assert (or
    (not (= (str.++ w y x) y))
    (not (str.contains y (str.++ "BCBB" "AABB" x)))
    (= z (str.++ w w z))
    (str.contains y "ABB")
  )
)
(assert (or
    (str.contains y w)
    (= (str.++ w z "ABBB") x)
    (= w (str.++ y "ACAABB" x))
    (= (str.++ x "AAA" "CBAAA") "AACAAAA")
  )
)
(assert (or
    (= (str.++ "BBBAA" x x) (str.++ x w z))
    (= (str.++ "BBBB" "BABC" "BACB") (str.++ z "BAABBAC" "BBACBB"))
    (str.contains "ABBB" (str.++ x "AABB" "AAA"))
    (= x "ABABCAB")
  )
)
(assert (or
    (not (= (str.++ x x "BBAA") (str.++ "BABCBCB" "BBB" "BBABBB")))
    (str.contains z (str.++ z x "ABCB"))
    (= "BAAB" x)
  )
)
(assert (or
    (= (str.++ "ACB" w "BABC") (str.++ x w "AAACA"))
    (= y (str.++ "BABBA" x z))
    (= y (str.++ "BABBA" x z))
  )
)
(assert (or
    (str.contains y (str.++ "BCBB" "AABB" x))
    (= (str.++ "BBBAA" x x) (str.++ x w z))
    (str.contains y w)
    (str.contains "ABBB" (str.++ x "AABB" "AAA"))
  )
)
(assert (or
    (not (= (str.++ "BBBB" "BABC" "BACB") (str.++ z "BAABBAC" "BBACBB")))
    (= (str.++ "ABAB" y x) z)
    (str.contains y "ABB")
    (= x (str.++ "ACCCBBA" y y))
  )
)
(assert (or
    (= (str.++ x x "BBAA") (str.++ "BABCBCB" "BBB" "BBABBB"))
    (= w x)
    (not (str.contains z (str.++ z x "ABCB")))
  )
)
(assert (or
    (str.contains y (str.++ z x z))
    (= z (str.++ w w z))
    (= (str.++ w y x) y)
    (= w (str.++ y "ACAABB" x))
  )
)
(assert (or
    (not (= (str.++ w z "ABBB") x))
    (= (str.++ "ACB" w "BABC") (str.++ x w "AAACA"))
  )
)
(assert (or
    (not (= x "ABABCAB"))
    (not (= "BAAB" x))
  )
)
(assert (or
    (not (= (str.++ x "AAA" "CBAAA") "AACAAAA"))
    (= x (str.++ "ACCCBBA" y y))
    (not (= (str.++ x "AAA" "CBAAA") "AACAAAA"))
    (str.contains y (str.++ "BCBB" "AABB" x))
  )
)
(assert (or
    (= (str.++ "ACB" w "BABC") (str.++ x w "AAACA"))
    (not (str.contains y "ABB"))
    (str.contains y (str.++ z x z))
  )
)
(assert (or
    (not (= (str.++ "ABAB" y x) z))
    (= z (str.++ w w z))
    (not (= (str.++ "BBBB" "BABC" "BACB") (str.++ z "BAABBAC" "BBACBB")))
  )
)
(assert (or
    (str.contains "ABBB" (str.++ x "AABB" "AAA"))
    (= y (str.++ "BABBA" x z))
  )
)
(assert (or
    (= (str.++ w z "ABBB") x)
    (= w x)
    (not (= "BAAB" x))
  )
)
(assert (or
    (str.contains y w)
    (= (str.++ x x "BBAA") (str.++ "BABCBCB" "BBB" "BBABBB"))
  )
)
(assert (or
    (= w (str.++ y "ACAABB" x))
    (not (= (str.++ "BBBAA" x x) (str.++ x w z)))
    (not (str.contains z (str.++ z x "ABCB")))
    (= (str.++ w y x) y)
  )
)
(assert (or
    (= x "ABABCAB")
    (not (str.contains "ABBB" (str.++ x "AABB" "AAA")))
    (= (str.++ "BBBAA" x x) (str.++ x w z))
    (not (= x (str.++ "ACCCBBA" y y)))
  )
)
(assert (or
    (= (str.++ x x "BBAA") (str.++ "BABCBCB" "BBB" "BBABBB"))
    (not (= (str.++ "BBBB" "BABC" "BACB") (str.++ z "BAABBAC" "BBACBB")))
  )
)
(assert (or
    (not (= x "ABABCAB"))
    (str.contains z (str.++ z x "ABCB"))
  )
)
(assert (or
    (str.contains y (str.++ z x z))
    (not (= (str.++ x "AAA" "CBAAA") "AACAAAA"))
  )
)
(assert (or
    (not (= (str.++ w y x) y))
    (not (str.contains y "ABB"))
  )
)
(assert (or
    (not (= (str.++ "ACB" w "BABC") (str.++ x w "AAACA")))
    (= "BAAB" x)
    (str.contains y (str.++ "BCBB" "AABB" x))
  )
)
(assert (or
    (not (= (str.++ w z "ABBB") x))
    (not (= (str.++ "ABAB" y x) z))
    (str.contains y w)
  )
)
(assert (or
    (not (= w x))
    (not (= w (str.++ y "ACAABB" x)))
  )
)
(assert (or
    (= y (str.++ "BABBA" x z))
    (not (= z (str.++ w w z)))
  )
)
(assert (or
    (not (= y (str.++ "BABBA" x z)))
    (not (= x "ABABCAB"))
  )
)
(assert (or
    (str.contains y "ABB")
    (not (str.contains y (str.++ z x z)))
    (not (str.contains "ABBB" (str.++ x "AABB" "AAA")))
  )
)
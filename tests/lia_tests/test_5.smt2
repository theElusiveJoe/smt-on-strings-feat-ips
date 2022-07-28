(declare-fun y String ())

(assert (or
    (= y (str.++ "ABABC" (str.replace_all y "BBABAB" y) "BCABB"))
  )
)
(assert (or
    (str.contains (str.replace_all y "BBABAB" y) y)
  )
)
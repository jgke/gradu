strcmp :: [Int] -> [Int] -> Int
strcmp (a:as) (b:bs) = if a == b
                       then strcmp as bs
                       else a - b
strcmp a b = head (a++[0]) - head (b++[0])

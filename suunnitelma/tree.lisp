(sysimport "stdio.h")

(deftype Tree
  value.int
  left.*Tree
  right.*Tree)

(defun print-tree (indent.int tree.*Tree)
    (if (nil? tree)
      (printf "%*cLeaf\n" indent ' ')
      (do
        (printf "%*c[Branch %d\n" indent ' ' tree)
        (print-tree (+ indent 2) (Tree:left tree))
        (print-tree (+ indent 2) (Tree:right tree))
        (printf "%*c]\n" n ' '))))

(defun main (argc.int argv.[const char])
  print-tree (quote
               (1
                nil
                (2
                 (5 nil nil)
                 (7
                  (3 nil nil)
                  nil)))))

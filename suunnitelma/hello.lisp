(sysimport "stdio.h")
(defun main (argc argv)
    (printf "Hello world!"))

; explicitly typed version
(sysimport "stdio.h")
(defun main (argc.int argv.[const char])
    (printf "Hello world!"))

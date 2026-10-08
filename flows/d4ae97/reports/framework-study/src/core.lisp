(defun main () (print (+ 1 2)) (terpri))
(sb-ext:save-lisp-and-die "hello-sbcl" :executable t :toplevel #'main)

(defun c:pdmscah   (/ AT:GetVertices strnum _dxf theobj fn thelist pref f)
;load the visual lisp extensions
(vl-load-com)   
        (defun AT:GetVertices  (e / p l)
            (if e
                  (if (eq (setq p (vlax-curve-getEndParam e))
                          (fix p))
                        (repeat (setq p (1+ (fix p)))
                              (setq l    (cons (vlax-curve-getPointAtParam
                                                     e
                                                     (setq p    (1- p)))
                                               l))
                              )
                        (list (vlax-curve-getStartPoint e)
                              (vlax-curve-getEndPoint e))
                        )
                  )
            )
      (defun strnum  (str val / p)
            (setq p " ")
            (repeat (- val (strlen str))
                  (setq p (strcat " " p)))
            (strcat str p))
      (defun _dxf (ent dx)(cdr (assoc dx (entget ent))))
      (vl-mkdir "c:/User121")
      (setq fn (open (setq f "c:/user121/infile") "w"))
      (prompt "\nSelect a Polyline: ")
      (while (and fn (setq theobj (ssget '((0 . "*LINE")))))  
            (setq thelist (if (eq (_dxf (setq e (ssname theobj 0)) 0) "LINE")
                               (progn (setq pref '("NEW SCTN poss" "pose")) (list (_dxf e 10)(_dxf e 11)))
    (AT:GetVertices e)))                       
            (redraw e 3)
   (write-line "Polyline" fn)
            (foreach 
                   itm  thelist
                  (write-line
                        (strcat (if pref
                                    (strcat "                 " (car pref) "  X  ")
                                    "          at point  X  ")
                                (strnum (rtos (Car itm) 2 4) 10)
                                "Y  "
                                (strnum (rtos (Cadr itm) 2 4) 10)
                                "Z  "
                                (strnum (rtos (last itm) 2 4) 10))
                        fn)
                  (setq pref (cdr pref))
                  )
            )
      
      (close fn)
      (startapp "notepad" f)
      (vla-regen (vla-get-ActiveDocument (vlax-get-acad-object)) acActiveViewport)
            (princ)
      ) 
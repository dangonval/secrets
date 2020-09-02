:;exec emacs -batch -l "$0" -f main "$@"

;; the above is a "sesquicolon" which allows running emacs scripts as a side-effect of running a bash script. See here: https://www.emacswiki.org/emacs/EmacsScripts

;; this emacs script will extract the given table from the orgfile, in the selected format

;; org-table tblname orgfile lisp|csv|tab

(defun export-org-table ()

  (let ((tblname (pop command-line-args-left))
	(org-file (pop command-line-args-left))
	(format)
	(table)
	(content))
    (when command-line-args-left
      (setq format (pop command-line-args-left)))
    (find-file org-file)
    (setq table 
	  (org-element-map (org-element-parse-buffer) 'table 
	    (lambda (element)
	      (when (string= tblname (org-element-property :name element))
		element))
	    nil ;info
	    t )) ; first-match

    (unless table
      (error "no table found for %s" tblname))

    (when table
      (goto-char (org-element-property :contents-begin table))
      (let ((contents (org-table-to-lisp)))
	(if (string= format "lisp")
	    (print contents)
					;else      
	  (dolist (row contents)
	    (unless (eq row 'hline)
	      (cond
	       ((string= format "csv")
		(princ (mapconcat 'identity row "§")))
	       ((string= format "tab")
		(princ (mapconcat 'identity row "\t")))
	       (t
		(error "unsupported format: %s" format)))
	      (princ "\n"))))))))


(defun main ()
  (export-org-table)
  )

;; Local Variables:
;; mode: emacs-lisp
;; End:

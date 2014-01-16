(ns clearley-calc.core
  (:gen-class))

(use 'clearley.core 'clearley.match 'clearley.lib)

(defn emit ([op a b] (conj '() b a op))
  ([op a] (conj '() a op)))


(def whitespace '(:star (:or \space \tab \newline \return)))

(def digit-symb (char-range \0 \9 identity))

(def letter-symb `(:or ~(char-range \a \z identity) ~(char-range \A \Z identity)))

(def ident-tail `(:star (:or digit-symb letter-symb)))

(defn merge-ident-tail ([builder] builder)
  ([builder c] (.append builder c)))

(defmatch ident-name
  [letter-symb ident-tail]
  (str letter-symb
       (reduce merge-ident-tail
               (conj ident-tail (java.lang.StringBuilder.)))))

(defn level-of-number [x]
  (defn level [x l]
    (if (> (/ x l) 1)
      (level x (* l 10))
      l))
  (level x 10))

(defmatch float-part
  ([\. natnum] (let [x natnum] (/ x (level-of-number x)))))

(defmatch float-num
  ([natnum float-part] (+ natnum float-part))
  natnum)

(defmatch sum
  ([sum whitespace \+ whitespace term] (emit + sum term))
  ([sum whitespace \- whitespace term] (emit - sum term))
  term)

(defmatch term
  ([term whitespace \* whitespace fact] (emit * term fact))
  ([term whitespace \/ whitespace fact] (emit / term fact))
  fact)

(defmatch fact
  ([\- fact] (emit - fact))
  ([\( whitespace sum whitespace \)] sum)
  ([ident-name] (symbol ident-name))
  float-num)

(defmatch top-level-expr
  ([whitespace sum whitespace] sum)
  ([whitespace ident-name whitespace \= whitespace sum whitespace]
   (emit (symbol "def") (symbol ident-name) sum))
  ([whitespace] ""))

(def my-calculator (build-parser top-level-expr))

(defn calc [inp]  (execute my-calculator inp))

;(eval (calc "1 + 2"))
;(eval (calc " -(1 + (7-5) * -3) + -0.1"))
;(eval (calc "testValue = -(1 + (7-5) * -3) + -0.1"))

(defn do-calc [line func]
  (println (eval (calc line)))
  (func))

(defn process[]
  (let [line (read-line)]
    (if (not= line "quit") (do-calc line process))))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Input `quit` to exit\n")
  (process))
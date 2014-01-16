(ns clearley-calc.core-test
  (:require [clojure.test :refer :all]
            [clearley-calc.core :refer :all]))

(eval (calc "testValue = 3"))

(deftest a-test
  (testing "FIXME, I fail."
    (is (= (eval (calc "1 + 2")) 3))
    (is (= (eval (calc " -(1 + (7-5) * -3) + -0.1")) (/ 49 10)))
    (is (= testValue 3))))

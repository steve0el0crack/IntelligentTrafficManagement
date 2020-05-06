(ns IntelligentTrafficLightManagement.core)

;;The idea is to take advantage of the concepts of ASYNCHRONY. Threads, promises, atoms, refs and much more. For the autos and Traffic light "agents"... these are te only valuable things our programm must be able to manage properly with a certain direction.

;;;;;;;;;;;;;;;;;;;;;;;;;;;;basic world;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(def world-data
  {:xdim 3
   :ydim 3
   :xstreets 2
   :ystreets 2
   :autosnum 2
   :tlnum 2})

;; (apply map (assoc worlddata key val) [sys.input])

(def dirs
  {:A {:x -1 :y 0}
   :D {:x 1 :y 0}
   :W {:x 0 :y 1}
   :S {:x 0 :y -1}})

(defstruct street :x :y :street) ;;may also have other :auto :tl :display
(def world 
  (for [y (range (:ydim world-data))
        x (range (:xdim world-data))]
    (struct street x y [])))

(defn setdirinworld
  [key
   index
   dir
   inputworld]
  (map (fn [place]
         (if (= (key place) index)
           (update place :street (fn [oldvalue] (conj oldvalue dir)))
           place))
       inputworld))

(defstruct streetindex :x :y)
(def streetindex-ready
  (struct streetindex
          (for [i (range (:xstreets world-data))] (rand-int (- (:xdim world-data) 1)))
          (for [i (range (:ystreets world-data))] (rand-int (- (:ydim world-data) 1)))))


;;There is a problem when no x or y streets are asked, when destructuring in the loop
(nth [] 0)
;;And when only [0] one street is asked, when returning the end-value of the function
(= 0 (- (count [1]) 1))

(defn extract
  [array
   n]
  (if (or (= (count array) 0) (> n (- (count array) 1)))
    nil
    (nth array n)))

(def insert-streets-in
  (fn [axis 
       inputworld]
    (loop [counter 0 
           currentworld inputworld
           index (extract (axis streetindex-ready) counter)]
      (if (= index nil)
        currentworld
        (recur (+ counter 1)
               (setdirinworld axis index (rand-nth (keys dirs)) currentworld)
               (extract (axis streetindex-ready) (+ counter 1)))))))

(defn -main []
  (->> world
       (insert-streets-in :x)
       (insert-streets-in :y))
  )


(define (problem frozen-lake-4x4)
  (:domain frozen-lake)
  
  (:objects
    loc-0-0 loc-0-1 loc-0-2 loc-0-3
    loc-1-0 loc-1-1 loc-1-2 loc-1-3
    loc-2-0 loc-2-1 loc-2-2 loc-2-3
    loc-3-0 loc-3-1 loc-3-2 loc-3-3 - location
  )
  
  (:init
    ; Define the starting position
    (at loc-0-0)
    
    ; Define the goal
    (is-goal loc-3-3)
    
    ; Define the holes
    (is-hole loc-1-1)
    (is-hole loc-1-3)
    (is-hole loc-2-3)
    (is-hole loc-3-0)
    
    ; Define safe locations (all non-hole locations)
    (is-safe loc-0-0) (is-safe loc-0-1) (is-safe loc-0-2) (is-safe loc-0-3)
    (is-safe loc-1-0) (is-safe loc-1-2)
    (is-safe loc-2-0) (is-safe loc-2-1) (is-safe loc-2-2)
    (is-safe loc-3-1) (is-safe loc-3-2) (is-safe loc-3-3)
    
    ; Define directional relationships
    (up loc-1-0 loc-0-0) (down loc-0-0 loc-1-0)
    (up loc-1-1 loc-0-1) (down loc-0-1 loc-1-1)
    (up loc-1-2 loc-0-2) (down loc-0-2 loc-1-2)
    (up loc-1-3 loc-0-3) (down loc-0-3 loc-1-3)
    (up loc-2-0 loc-1-0) (down loc-1-0 loc-2-0)
    (up loc-2-1 loc-1-1) (down loc-1-1 loc-2-1)
    (up loc-2-2 loc-1-2) (down loc-1-2 loc-2-2)
    (up loc-2-3 loc-1-3) (down loc-1-3 loc-2-3)
    (up loc-3-0 loc-2-0) (down loc-2-0 loc-3-0)
    (up loc-3-1 loc-2-1) (down loc-2-1 loc-3-1)
    (up loc-3-2 loc-2-2) (down loc-2-2 loc-3-2)
    (up loc-3-3 loc-2-3) (down loc-2-3 loc-3-3)
    
    (left loc-0-1 loc-0-0) (right loc-0-0 loc-0-1)
    (left loc-0-2 loc-0-1) (right loc-0-1 loc-0-2)
    (left loc-0-3 loc-0-2) (right loc-0-2 loc-0-3)
    (left loc-1-1 loc-1-0) (right loc-1-0 loc-1-1)
    (left loc-1-2 loc-1-1) (right loc-1-1 loc-1-2)
    (left loc-1-3 loc-1-2) (right loc-1-2 loc-1-3)
    (left loc-2-1 loc-2-0) (right loc-2-0 loc-2-1)
    (left loc-2-2 loc-2-1) (right loc-2-1 loc-2-2)
    (left loc-2-3 loc-2-2) (right loc-2-2 loc-2-3)
    (left loc-3-1 loc-3-0) (right loc-3-0 loc-3-1)
    (left loc-3-2 loc-3-1) (right loc-3-1 loc-3-2)
    (left loc-3-3 loc-3-2) (right loc-3-2 loc-3-3)
  )
  
  (:goal (at loc-3-3))
)

(define (domain frozen-lake)
  (:requirements :typing :strips :probabilistic-effects)
  
  (:types
    location - object
  )
  
  (:predicates
    (at ?loc - location)
    (up ?from ?to - location)
    (down ?from ?to - location)
    (left ?from ?to - location)
    (right ?from ?to - location)
    (is-hole ?loc - location)
    (is-goal ?loc - location)
    (is-start ?loc - location)
  )

  (:functions
    (reward)
  )
  
  (:action move-up
    :parameters (?from ?to - location)
    :precondition (and
       (at ?from)
      (up ?from ?to)
    )
    :effect (and
      (not (at ?from))
      (probabilistic 0.33333 (at ?to)
                     0.33333 (and (when (left ?from ?leftloc) (at ?leftloc)))
                     0.33333 (and (when (right ?from ?rightloc) (at ?rightloc))))
      (when (is-hole ?to) (decrease (reward) 1))
      (when (is-goal ?to) (increase (reward) 1))
    )
  )

  (:action move-down
    :parameters (?from ?to - location)
    :precondition (and
       (at ?from)
      (down ?from ?to)
    )
    :effect (and
      (not (at ?from))
      (probabilistic 0.33333 (at ?to)
                     0.33333 (and (when (left ?from ?leftloc) (at ?leftloc)))
                     0.33333 (and (when (right ?from ?rightloc) (at ?rightloc))))
      (when (is-hole ?to) (decrease (reward) 1))
      (when (is-goal ?to) (increase (reward) 1))
    )
  )

  (:action move-left
    :parameters (?from ?to - location)
    :precondition (and
       (at ?from)
      (left ?from ?to)
    )
    :effect (and
      (not (at ?from))
      (probabilistic 0.33333 (at ?to)
                     0.33333 (and (when (up ?from ?uploc) (at ?uploc)))
                     0.33333 (and (when (down ?from ?downloc) (at ?downloc))))
      (when (is-hole ?to) (decrease (reward) 1))
      (when (is-goal ?to) (increase (reward) 1))
    )
  )

  (:action move-right
    :parameters (?from ?to - location)
    :precondition (and
       (at ?from)
      (right ?from ?to)
    )
    :effect (and
      (not (at ?from))
      (probabilistic 0.33333 (at ?to)
                     0.33333 (and (when (up ?from ?uploc) (at ?uploc)))
                     0.33333 (and (when (down ?from ?downloc) (at ?downloc))))
      (when (is-hole ?to) (decrease (reward) 1))
      (when (is-goal ?to) (increase (reward) 1))
    )
  )
)
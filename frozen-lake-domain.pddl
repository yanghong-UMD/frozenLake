(define (domain frozen-lake)
  (:requirements :strips :typing)
  
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
    (is-safe ?loc - location)

  )
  
    (:action move-up
        :parameters (?from ?to - location)
        :precondition (and 
            (at ?from)
            (up ?from ?to)
            (is-safe ?to)
        )
        :effect (and
            (not (at ?from))
            (at ?to)
        )
    )

    (:action move-down
        :parameters (?from ?to - location)
        :precondition (and 
            (at ?from)
            (down ?from ?to)
            (is-safe ?to)
        )
        :effect (and
            (not (at ?from))
            (at ?to)
        )
    )

    (:action move-left
        :parameters (?from ?to - location)
        :precondition (and 
            (at ?from)
            (left ?from ?to)
            (is-safe ?to)
        )
        :effect (and
            (not (at ?from))
            (at ?to)
        )
    )

    (:action move-right
        :parameters (?from ?to - location)
        :precondition (and 
            (at ?from)
            (right ?from ?to)
            (is-safe ?to)
        )
        :effect (and
            (not (at ?from))
            (at ?to)
        )
    )

)
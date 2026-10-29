(define (domain lunar)
    (:requirements :strips :typing)

    (:types
        rover lander waypoint sample - object
        data - object
        image scan - data
    )

    (:predicates
        ; Fixed relationships and map facts.
        (assigned ?r - rover ?l - lander)
        (connected ?from - waypoint ?to - waypoint)
        (data-at ?d - data ?w - waypoint)
        (sample-at ?s - sample ?w - waypoint)

        ; Vehicle and lander state.
        (aboard ?r - rover ?l - lander)
        (deployed ?r - rover)
        (rover-at ?r - rover ?w - waypoint)
        (lander-at ?l - lander ?w - waypoint)

        ; Data memory has capacity one per rover.
        (memory-free ?r - rover)
        (carrying-data ?r - rover ?d - data)
        (transmitted ?d - data ?l - lander)

        ; A rover carries at most one sample and a lander stores at most one.
        (sample-space-free ?r - rover)
        (carrying-sample ?r - rover ?s - sample)
        (lander-space-free ?l - lander)
        (stored ?s - sample ?l - lander)
    )

    (:action deploy
        :parameters (?r - rover ?l - lander ?w - waypoint)
        :precondition (and
            (assigned ?r ?l)
            (aboard ?r ?l)
            (lander-at ?l ?w)
        )
        :effect (and
            (deployed ?r)
            (rover-at ?r ?w)
            (not (aboard ?r ?l))
        )
    )

    (:action move
        :parameters (?r - rover ?from - waypoint ?to - waypoint)
        :precondition (and
            (deployed ?r)
            (rover-at ?r ?from)
            (connected ?from ?to)
        )
        :effect (and
            (rover-at ?r ?to)
            (not (rover-at ?r ?from))
        )
    )

    (:action capture-image
        :parameters (?r - rover ?i - image ?w - waypoint)
        :precondition (and
            (deployed ?r)
            (rover-at ?r ?w)
            (data-at ?i ?w)
            (memory-free ?r)
        )
        :effect (and
            (carrying-data ?r ?i)
            (not (memory-free ?r))
        )
    )

    (:action perform-scan
        :parameters (?r - rover ?s - scan ?w - waypoint)
        :precondition (and
            (deployed ?r)
            (rover-at ?r ?w)
            (data-at ?s ?w)
            (memory-free ?r)
        )
        :effect (and
            (carrying-data ?r ?s)
            (not (memory-free ?r))
        )
    )

    (:action transmit-data
        :parameters (?r - rover ?l - lander ?d - data)
        :precondition (and
            (deployed ?r)
            (assigned ?r ?l)
            (carrying-data ?r ?d)
        )
        :effect (and
            (transmitted ?d ?l)
            (memory-free ?r)
            (not (carrying-data ?r ?d))
        )
    )

    (:action collect-sample
        :parameters (?r - rover ?s - sample ?w - waypoint)
        :precondition (and
            (deployed ?r)
            (rover-at ?r ?w)
            (sample-at ?s ?w)
            (sample-space-free ?r)
        )
        :effect (and
            (carrying-sample ?r ?s)
            (not (sample-space-free ?r))
            (not (sample-at ?s ?w))
        )
    )

    (:action store-sample
        :parameters (?r - rover ?l - lander ?s - sample ?w - waypoint)
        :precondition (and
            (deployed ?r)
            (assigned ?r ?l)
            (rover-at ?r ?w)
            (lander-at ?l ?w)
            (carrying-sample ?r ?s)
            (lander-space-free ?l)
        )
        :effect (and
            (stored ?s ?l)
            (sample-space-free ?r)
            (not (carrying-sample ?r ?s))
            (not (lander-space-free ?l))
        )
    )
)

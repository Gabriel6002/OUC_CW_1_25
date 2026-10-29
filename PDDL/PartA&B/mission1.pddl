(define (problem lunar-mission-1)
    (:domain lunar)

    (:objects
        rover1 - rover
        lander1 - lander
        wp1 wp2 wp3 wp4 wp5 - waypoint
        image-wp5 - image
        scan-wp3 - scan
        sample-wp1 - sample
    )

    (:init
        (assigned rover1 lander1)
        (aboard rover1 lander1)
        (lander-at lander1 wp1)
        (memory-free rover1)
        (sample-space-free rover1)
        (lander-space-free lander1)

        ; Figure 2 directions are represented exactly as arrows.
        (connected wp5 wp1)
        (connected wp1 wp2)
        (connected wp2 wp3)
        (connected wp3 wp5)
        (connected wp1 wp4)
        (connected wp4 wp3)

        (data-at image-wp5 wp5)
        (data-at scan-wp3 wp3)
        (sample-at sample-wp1 wp1)
    )

    (:goal
        (and
            (transmitted image-wp5 lander1)
            (transmitted scan-wp3 lander1)
            (stored sample-wp1 lander1)
        )
    )
)

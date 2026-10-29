(define (problem lunar-mission-2)
    (:domain lunar)

    (:objects
        rover1 rover2 - rover
        lander1 lander2 - lander
        wp1 wp2 wp3 wp4 wp5 wp6 - waypoint
        image-wp3 image-wp2 - image
        scan-wp4 scan-wp6 - scan
        sample-wp5 sample-wp1 - sample
    )

    (:init
        (assigned rover1 lander1)
        (assigned rover2 lander2)

        (deployed rover1)
        (rover-at rover1 wp2)
        (lander-at lander1 wp2)

        (aboard rover2 lander2)
        (lander-at lander2 wp1)

        (memory-free rover1)
        (memory-free rover2)
        (sample-space-free rover1)
        (sample-space-free rover2)
        (lander-space-free lander1)
        (lander-space-free lander2)

        ; Figure 3 directions.
        (connected wp1 wp2)
        (connected wp2 wp1)
        (connected wp2 wp3)
        (connected wp2 wp4)
        (connected wp4 wp2)
        (connected wp3 wp5)
        (connected wp5 wp3)
        (connected wp5 wp6)
        (connected wp6 wp4)

        (data-at image-wp3 wp3)
        (data-at scan-wp4 wp4)
        (data-at image-wp2 wp2)
        (data-at scan-wp6 wp6)
        (sample-at sample-wp5 wp5)
        (sample-at sample-wp1 wp1)
    )

    (:goal
        (and
            (transmitted image-wp3 lander1)
            (transmitted scan-wp4 lander2)
            (transmitted image-wp2 lander2)
            (transmitted scan-wp6 lander1)
            (stored sample-wp5 lander1)
            (stored sample-wp1 lander2)
        )
    )
)

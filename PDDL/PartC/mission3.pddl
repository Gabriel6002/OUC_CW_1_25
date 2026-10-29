(define (problem lunar-mission-3)
    (:domain lunar-extended)

    (:objects
        rover1 rover2 - rover
        lander1 lander2 - lander
        wp1 wp2 wp3 wp4 wp5 wp6 - waypoint
        image-wp3 image-wp2 - image
        scan-wp4 scan-wp6 - scan
        sample-wp5 sample-wp1 - sample
        alice bob - astronaut
        control1 control2 - control-room
        dock1 dock2 - docking-bay
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

        (astronaut-assigned alice lander1)
        (astronaut-assigned bob lander2)
        (area-in control1 lander1)
        (area-in dock1 lander1)
        (area-in control2 lander2)
        (area-in dock2 lander2)
        (room-connected control1 dock1)
        (room-connected dock1 control1)
        (room-connected control2 dock2)
        (room-connected dock2 control2)
        (astronaut-at alice dock1)
        (astronaut-at bob control2)
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

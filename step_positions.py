def step_positions(t0_position):
    # Format: (delay relative to t0 in fs, number of cycles for the delay).
    # If number of cycles is -1, it will use the value set in the GUI at the start of the run.
    delay_and_cylcles = [
            (-500, -1),
            (-400, -1),
            (-300, -1),
            (-250, -1),
            (-200, -1),
            (-150, -1),
            (-100, -1),
            (-50, -1),
            (0, -1),
            (50, -1),
            (100, -1),
            (150, -1),
            (200, -1),
            (250, -1),
            (300, -1),
            (350, -1),
            (400, -1),
            (450, -1),
            (500, -1),
            (550, -1),
            (600, -1),
            (650, -1),
            (700, -1),
            (750, -1),
            (800, -1),
            (850, -1),
            (900, -1),
            (950, -1),
            (1000, -1),
            (1100, -1),
            (1200, -1),
            (1300, -1),
            (1400, -1),
            (1500, -1),
            (1600, -1),
            (1700, -1),
            (1800, -1),
            (1900, -1),
            (2000, -1),
        ]
    
    # Separate out the delay and number of cycles, convert delay in fs to stage position in mm
    delays = [t0_position + (i[0] / 6671.2819) for i in delay_and_cylcles]
    cycles = [i[1] for i in delay_and_cylcles]

    return delays, cycles
from app.database import db


class SingleChartRecord(db.Model):
    __tablename__ = "single_chart_records"

    id = db.Column(db.Uuid, db.ForeignKey("chart_records.id"), primary_key=True)
    chart = db.relationship("ChartRecord", back_populates="single_chart", uselist=False)

    # Timing / BPM
    length_seconds = db.Column(db.Float)
    display_bpm_min = db.Column(db.Float)
    display_bpm_max = db.Column(db.Float)
    true_bpm_min = db.Column(db.Float)
    true_bpm_max = db.Column(db.Float)
    bpm_changes = db.Column(db.Integer)
    stops = db.Column(db.Integer)

    # Basic info
    artist = db.Column(db.String)

    # Step stats
    steps = db.Column(db.Integer)
    jumps = db.Column(db.Integer)
    holds = db.Column(db.Integer)
    shock_arrows = db.Column(db.Integer)
    hands = db.Column(db.Integer)
    crossovers = db.Column(db.Integer)
    footswitches = db.Column(db.Integer)
    sideswitches = db.Column(db.Integer)
    jacks = db.Column(db.Integer)
    brackets = db.Column(db.Integer)
    total_stream = db.Column(db.Integer)
    max_nps = db.Column(db.Float)

    # BPM diffs
    display_bpm_diff = db.Column(db.Float)
    true_bpm_diff = db.Column(db.Float)
    bpm_min_diff = db.Column(db.Float)
    bpm_max_diff = db.Column(db.Float)
    bpm_total_diff = db.Column(db.Float)

    # Derived counts
    bpm_changes_plus_stops = db.Column(db.Integer)
    steps_plus_jumps = db.Column(db.Integer)
    jumps_minus_brackets = db.Column(db.Integer)
    steps_plus_jumps_minus_brackets = db.Column(db.Integer)

    # Percentages
    jumps_per_steps = db.Column(db.Float)
    brackets_per_jumps = db.Column(db.Float)
    jumps_minus_brackets_per_steps = db.Column(db.Float)
    holds_per_steps = db.Column(db.Float)
    shock_arrows_per_step = db.Column(db.Float)
    hands_per_steps = db.Column(db.Float)
    crossovers_per_steps = db.Column(db.Float)
    footswitches_per_steps = db.Column(db.Float)
    sideswitches_per_steps = db.Column(db.Float)
    jacks_per_steps = db.Column(db.Float)

    # Per-second metrics
    bpm_changes_per_second = db.Column(db.Float)
    stops_per_second = db.Column(db.Float)
    bpm_changes_plus_stops_per_second = db.Column(db.Float)
    steps_per_second = db.Column(db.Float)
    jumps_per_second = db.Column(db.Float)
    steps_plus_jumps_per_second = db.Column(db.Float)
    brackets_per_second = db.Column(db.Float)
    jumps_minus_brackets_per_second = db.Column(db.Float)
    steps_plus_jumps_minus_brackets_per_second = db.Column(db.Float)
    holds_per_second = db.Column(db.Float)
    shock_arrows_per_second = db.Column(db.Float)
    hands_per_second = db.Column(db.Float)
    crossovers_per_second = db.Column(db.Float)
    footswitches_per_second = db.Column(db.Float)
    sideswitches_per_second = db.Column(db.Float)
    jacks_per_second = db.Column(db.Float)

    # Combined measures
    footswitches_minus_sideswitches = db.Column(db.Integer)
    footswitches_minus_sideswitches_per_steps = db.Column(db.Float)
    footswitches_minus_sideswitches_per_second = db.Column(db.Float)
    crossovers_plus_footswitches = db.Column(db.Integer)
    crossovers_plus_footswitches_plus_jacks = db.Column(db.Integer)
    crossovers_plus_footswitches_per_steps = db.Column(db.Float)
    crossovers_plus_footswitches_plus_jacks_per_steps = db.Column(db.Float)
    crossovers_plus_footswitches_per_second = db.Column(db.Float)
    crossovers_plus_footswitches_plus_jacks_per_second = db.Column(db.Float)

    jumps_holds_shocks_cross_foots_jacks = db.Column(db.Integer)
    jumps_holds_shocks_cross_foots_jacks_per_step = db.Column(db.Float)
    jumps_holds_shocks_cross_foots_jacks_per_second = db.Column(db.Float)

    full_obj_total = db.Column(db.Integer)
    full_obj_total_per_second = db.Column(db.Float)

    # Ratings
    estimate_difficulty = db.Column(db.Float)
    alt_estimate_difficulty = db.Column(db.Float)
    real_world_difficulty = db.Column(db.Float)
    folder_difficulty = db.Column(db.Float)
    spice_rating = db.Column(db.Float)

    # Scoring
    max_combo = db.Column(db.Integer)
    score_per_marv_ok = db.Column(db.Float)
    score_per_perf = db.Column(db.Float)
    score_per_great = db.Column(db.Float)
    score_per_good = db.Column(db.Float)
    max_ex_score = db.Column(db.Integer)
    lines_with_holds = db.Column(db.Integer)
    oks_total = db.Column(db.Integer)
    holds_ignored = db.Column(db.Integer)
    score_from_steps = db.Column(db.Integer)
    score_from_holds = db.Column(db.Integer)
    score_from_shocks = db.Column(db.Integer)
    score_from_oks = db.Column(db.Integer)

    # AA/AAA thresholds
    aa_min_precision = db.Column(db.Float)
    aa_min_judgment = db.Column(db.String)
    aa_max_misses = db.Column(db.Integer)
    aaa_min_precision = db.Column(db.Float)
    aaa_min_judgment = db.Column(db.String)
    aaa_max_misses = db.Column(db.Integer)

    # Normalized ratios
    combo_per_step = db.Column(db.Float)
    ex_score_per_step = db.Column(db.Float)
    lines_with_holds_per_step = db.Column(db.Float)
    oks_per_step = db.Column(db.Float)
    holds_ignored_per_hold = db.Column(db.Float)
    combo_per_second = db.Column(db.Float)
    ex_score_per_second = db.Column(db.Float)
    lines_with_holds_per_second = db.Column(db.Float)
    oks_per_second = db.Column(db.Float)
    holds_ignored_per_second = db.Column(db.Float)

    # Arrows by direction
    left_notes = db.Column(db.Integer)
    down_notes = db.Column(db.Integer)
    up_notes = db.Column(db.Integer)
    right_notes = db.Column(db.Integer)

    # Lopsidedness and bias
    lopsided_max = db.Column(db.Float)
    lopsided_mean = db.Column(db.Float)
    left_right_bias = db.Column(db.Float)
    down_up_bias = db.Column(db.Float)
    horiz_vert_bias = db.Column(db.Float)

    # Quantization breakdown
    notes_4th = db.Column(db.Integer)
    notes_8th = db.Column(db.Integer)
    notes_12th = db.Column(db.Integer)
    notes_16th = db.Column(db.Integer)
    notes_20th = db.Column(db.Integer)
    notes_24th = db.Column(db.Integer)
    notes_32nd = db.Column(db.Integer)
    notes_48th = db.Column(db.Integer)
    notes_64th = db.Column(db.Integer)
    notes_96th = db.Column(db.Integer)
    notes_192nd = db.Column(db.Integer)

    most_frequent_quantization = db.Column(db.String)
    finest_quantization = db.Column(db.String)
    mean_quantization = db.Column(db.Float)
    quantization_power_of_two_bias = db.Column(db.Float)
    quantization_variety = db.Column(db.Float)

    # Groove Radar (official + estimated)
    stream_official = db.Column(db.Float)
    voltage_official = db.Column(db.Float)
    air_official = db.Column(db.Float)
    freeze_official = db.Column(db.Float)
    chaos_official = db.Column(db.Float)
    radar_total_official = db.Column(db.Float)

    stream_official_pct = db.Column(db.Float)
    voltage_official_pct = db.Column(db.Float)
    air_official_pct = db.Column(db.Float)
    freeze_official_pct = db.Column(db.Float)
    chaos_official_pct = db.Column(db.Float)

    stream_estimated = db.Column(db.Float)
    voltage_estimated = db.Column(db.Float)
    air_estimated = db.Column(db.Float)
    freeze_estimated = db.Column(db.Float)
    chaos_estimated = db.Column(db.Float)
    radar_total_estimated = db.Column(db.Float)

    stream_estimated_pct = db.Column(db.Float)
    voltage_estimated_pct = db.Column(db.Float)
    air_estimated_pct = db.Column(db.Float)
    freeze_estimated_pct = db.Column(db.Float)
    chaos_estimated_pct = db.Column(db.Float)

    stream_diff = db.Column(db.Float)
    voltage_diff = db.Column(db.Float)
    air_diff = db.Column(db.Float)
    freeze_diff = db.Column(db.Float)
    chaos_diff = db.Column(db.Float)
    radar_total_diff = db.Column(db.Float)

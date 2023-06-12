def getTempoValue(BPM):
    # 0 - 79 Slow
    # 80- 129 Medium
    # 130+ Fast
    BPM=int(BPM)
    if (0 <= BPM <= 79): return 1
    if (80 <= BPM <= 100): return 2
    if (101 <= BPM <= 129): return 3
    if (BPM >= 130): return 4

def getPopularityValue(popularity):
    # 0-20 -> 1
    # 20-40 -> 2
    # 40-60 -> 3
    # 60-80 -> 4
    # 80-100 ->5
    popularity = int(popularity)
    if 0 <= popularity <= 20:
        return 1
    elif 20 < popularity <= 40:
        return 2
    elif 40 < popularity <= 60:
        return 3
    elif 60 < popularity <= 80:
        return 4
    elif 80 < popularity <= 100:
        return 5
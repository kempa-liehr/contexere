def last(timeline):
    events = list(timeline.keys())
    events.sort()
    latest = events[-1]
    return [project + latest + max(timeline[latest][project].keys()) for project in timeline[latest]]

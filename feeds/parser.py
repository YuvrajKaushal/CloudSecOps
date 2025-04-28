def parse_feed(feed_json):
    indicators = []
    for item in feed_json:
        indicators.append({
            "type": item.get("type"),
            "value": item.get("value"),
            "source": item.get("source")
        })
    return indicators
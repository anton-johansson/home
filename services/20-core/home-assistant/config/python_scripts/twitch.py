input = data.get('stream_name')
mediaPlayer = "media_player.tv"

if input:
    streamName = input.lower()

    streams = {
      "dando": "dandolol",
      "swedish rocket league": "svenskaraketligan",
      "rocket league": "rocketleague",
      "dota two ti": "dota2ti",
      "dota ti": "dota2ti",
      "dota the international": "dota2ti",
      "the international": "dota2ti"
    }

    if streamName in streams:
        stream = streams[streamName]
    else:
        stream = streamName

    stream = stream.replace(" ", "")

    location = "https://twitch.tv/" + stream
    logger.info("Streaming {} (from input '{}') on Twitch on Chromecast".format(stream, input))
    hass.services.call("media_extractor", "play_media", {"entity_id": mediaPlayer, "media_content_id": location, "media_content_type": "video"})
else:
    logger.error("No 'stream_name' was given")

from abc import ABC, abstractmethod


class IMediaPlayerAdpater(ABC):

    @abstractmethod
    def play(self, file_name, fformat):
        pass


class AdvancedPlayer:
    """Adaptee — third-party library with incompatible interface"""

    def play_mp4(self, file_name_with_format):
        if file_name_with_format[-4:].lower() != ".mp4":
            raise ValueError("Invalid file type, expected .mp4")
        print("AdvancedPlayer: playing " + file_name_with_format)

    def play_vlc(self, file_name_with_format):
        if file_name_with_format[-4:].lower() != ".vlc":
            raise ValueError("Invalid file type, expected .vlc")
        print("AdvancedPlayer: playing " + file_name_with_format)


class MediaAdapter(IMediaPlayerAdpater):
    """Adapter — translates IMediaPlayer.play() to AdvancedPlayer methods"""

    def __init__(self, ap: AdvancedPlayer):
        self.ap = ap

    def play(self, file_name, fformat):
        fmt = fformat.lower()
        if fmt == "mp4":
            self.ap.play_mp4(file_name + ".mp4")
        elif fmt == "vlc":
            self.ap.play_vlc(file_name + ".vlc")
        else:
            raise ValueError(f"Unsupported format: {fformat}")


class AudioPlayer:
    """Client — handles mp3 natively, delegates advanced formats to adapter"""

    def __init__(self, adapter: MediaAdapter):
        self.adapter = adapter

    def play(self, file_name, fformat):
        if fformat.lower() == "mp3":
            print(f"AudioPlayer: playing {file_name}.mp3")
        else:
            self.adapter.play(file_name, fformat)


# demo
adapter = MediaAdapter(AdvancedPlayer())
audio_player = AudioPlayer(adapter)

audio_player.play("song", "mp3")
audio_player.play("movie", "mp4")
audio_player.play("clip", "vlc")

print("\n-- unsupported format --")
try:
    audio_player.play("video", "mkv")
except ValueError as e:
    print(f"ValueError: {e}")

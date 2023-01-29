#Code by AkinoAlice@Tyrant_Rex


from pytube import YouTube, Playlist, Search

class Tool:
    def change_url(keywords: tuple) -> str:
        keywords = list(keywords)
        if "youtube.com/" in keywords[0] or "youtu.be/" in keywords[0]:
            keywords = keywords[0]
            if "list=" in keywords:
                _ =  len(Playlist(keywords))
                if _ == 0:
                    urls = [YouTube(keywords).watch_url]
                elif _ >= 75:
                    urls = list(Playlist(keywords))[:75]
                else:
                    urls = list(Playlist(keywords))
            else:
                urls = [YouTube(keywords).watch_url]
        else:
            urls = [Search(" ".join(keywords)).results[0].watch_url]
        return urls
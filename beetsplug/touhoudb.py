from beetsplug import vocadb


class TouhouDBPlugin(
    vocadb.VocaDBPlugin,
    instance_info=vocadb.InstanceInfo(
        name="TouhouDB",
        base_url="https://touhoudb.com/",
        api_url="https://touhoudb.com/api/",
        subcommand="tdbsync",
    ),
):
    def get_album_artist(
        self, release: vocadb.AlbumDict
    ) -> tuple[dict[str, dict[str, str]], str, bool]:
        artist_categories, artist, va = super().get_album_artist(release)
        _, is_support = self.get_artists_by_categories(
            release.get("artists", [])
        )
        circles = [
            name
            for name, artist_id in artist_categories["circles"].items()
            if not is_support.get(artist_id)
        ]
        if circles:
            return artist_categories, ", ".join(circles), False

        return artist_categories, artist, va

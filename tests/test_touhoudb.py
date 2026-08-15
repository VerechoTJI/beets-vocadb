from beetsplug.touhoudb import TouhouDBPlugin
from tests.test_vocadb import TestVocaDBPlugin


class TestTouhouDBPlugin(TestVocaDBPlugin, plugin=TouhouDBPlugin()):
    def test_single_circle_complements_various_artist_result(self) -> None:
        release = {
            "discType": "Fanmade",
            "artists": [
                {
                    "artist": {"id": 1, "name": "Circle A"},
                    "categories": "Circle",
                    "effectiveRoles": "Default",
                    "isSupport": False,
                    "name": "Circle A",
                },
                *[
                    {
                        "artist": {"id": artist_id, "name": name},
                        "categories": "Producer",
                        "effectiveRoles": "Default",
                        "isSupport": False,
                        "name": name,
                    }
                    for artist_id, name in enumerate(
                        [
                            "Producer A",
                            "Producer B",
                            "Producer C",
                            "Producer D",
                            "Producer E",
                            "Producer F",
                        ],
                        start=100,
                    )
                ],
            ],
        }

        _, artist, va = self.plugin.get_album_artist(release)

        self.assertEqual(artist, "Circle A")
        self.assertFalse(va)

    def test_multiple_circles_are_used_for_album_artist(self) -> None:
        release = {
            "discType": "Compilation",
            "artists": [
                {
                    "categories": "Circle",
                    "effectiveRoles": "Default",
                    "isSupport": False,
                    "name": "Circle A",
                },
                {
                    "categories": "Circle",
                    "effectiveRoles": "Default",
                    "isSupport": False,
                    "name": "Circle B",
                },
            ],
        }

        _, artist, va = self.plugin.get_album_artist(release)

        self.assertEqual(artist, "Circle A, Circle B")
        self.assertFalse(va)

    def test_support_circle_does_not_replace_various_artists(self) -> None:
        release = {
            "discType": "Compilation",
            "artists": [
                {
                    "categories": "Circle",
                    "effectiveRoles": "Default",
                    "isSupport": True,
                    "name": "Supporting Circle",
                }
            ],
        }

        _, artist, va = self.plugin.get_album_artist(release)

        self.assertEqual(artist, self.plugin.va_string)
        self.assertTrue(va)

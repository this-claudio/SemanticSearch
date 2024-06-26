mapping = {
    "mappings": {
        "properties": {
            "show_id": {"type": "text"},
            "type": {"type": "text"},
            "title": {"type": "text"},
            "director": {"type": "text"},
            "cast": {"type": "text"},
            "country": {"type": "text"},
            "date_added": {"type": "date", "format": "MMMM dd, yyyy"},
            "release_year": {"type": "integer"},
            "rating": {"type": "text"},
            "duration": {"type": "text"},
            "listed_in": {"type": "text"},
            "description": {"type": "text"},
            "descriptionVector": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "l2_norm",
            },
        }
    }
}

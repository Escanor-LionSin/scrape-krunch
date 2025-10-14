import json
import hashlib
import os
from typing import Dict, Set

class ArticleCache:
    def __init__(self, cache_file: str = "article_cache.json"):
        self.cache_file = cache_file
        self.cache: Dict[str, Set[str]] = self._load_cache()

    def _load_cache(self) -> Dict[str, Set[str]]:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                    return {k: set(v) for k, v in cache_data.items()}
            except json.JSONDecodeError:
                return {"urls": set(), "title_hashes": set()}
        return {"urls": set(), "title_hashes": set()}

    def _save_cache(self):
        cache_data = {k: list(v) for k, v in self.cache.items()}
        with open(self.cache_file, 'w') as f:
            json.dump(cache_data, f)

    def _hash_title(self, title: str) -> str:
        return hashlib.md5(title.lower().encode()).hexdigest()

    def is_article_processed(self, url: str, title: str) -> bool:
        title_hash = self._hash_title(title)
        return url in self.cache["urls"] or title_hash in self.cache["title_hashes"]

    def add_article(self, url: str, title: str):
        title_hash = self._hash_title(title)
        self.cache["urls"].add(url)
        self.cache["title_hashes"].add(title_hash)
        self._save_cache()

    def clear_cache(self):
        self.cache = {"urls": set(), "title_hashes": set()}
        self._save_cache()
import json
import sqlite3
from datetime import datetime
from typing import List

from src.domain.model.pair.pair import Pairs, PairsHistoryRepository


class Sqlite3PairsHistoryRepository(PairsHistoryRepository):
    db_name: str = 'database/pairpair.sqlite3'

    def __init__(self) -> None:
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def save(self, pairs: Pairs) -> None:
        self.cursor.execute(
            'INSERT INTO pairs(data, created_at) VALUES (?, ?)',
            (json.dumps(pairs.to_list()), str(datetime.now())))
        self.conn.commit()  # TODO: to control in application

    def load(self) -> List[Pairs]:
        return [
            Pairs.from_list(json.loads(l[0])) for l in list(
                self.cursor.execute(
                    'SELECT data FROM pairs ORDER BY created_at'))
        ]

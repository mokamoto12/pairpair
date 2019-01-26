import json
import sqlite3
from datetime import datetime
from typing import List
from uuid import uuid4

from src.domain.model.pair.history import (PairsHistory, PairsHistoryId,
                                           PairsHistoryRepository)
from src.domain.model.pair.pair import Pairs


class Sqlite3PairsHistoryRepository(PairsHistoryRepository):
    db_name: str = 'database/pairpair.sqlite3'

    def __init__(self) -> None:
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def next_identity(self) -> PairsHistoryId:
        return PairsHistoryId(uuid4().hex)

    def save(self, pairs_history: PairsHistory) -> None:
        self.cursor.execute(
            'INSERT INTO pairs(id, data, created_at) VALUES (?, ?, ?)',
            (pairs_history.identity.value,
             json.dumps(pairs_history.pairs.to_list()), str(datetime.now())))
        self.conn.commit()  # TODO: to control in application

    def load(self) -> List[PairsHistory]:
        return [
            PairsHistory(
                PairsHistoryId(l[0]), Pairs.from_list(json.loads(l[1])))
            for l in list(
                self.cursor.execute(
                    'SELECT id, data FROM pairs ORDER BY created_at'))
        ]

import sqlite3
import os

class DB:

    def __init__(self):
        self.db  = None

    def __enter__(self):
        self.db = sqlite3.connect(os.path.join(os.getcwd(), 'chinook.db'))
        return self.db.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.db.close()

if __name__ == "__main__":

    with DB() as cursor:
        res = cursor.execute("""
        SELECT t.Name AS Your_fav_tracks 
        FROM tracks t 
        INNER JOIN 
        genres g ON t.GenreId = g.GenreId
        INNER JOIN 
        media_types mt ON t.MediaTypeId = mt.MediaTypeId
        WHERE g.Name LIKE 'R%' AND mt.Name = 'AAC audio file'""").fetchall()
    print('\n' + '*' * 13 + 'TASK-1' + '*' * 13)
    print(res)

    with DB() as cursor:
        res = cursor.execute("""
        SELECT Name, MAX(Bytes) AS Bytes
        FROM tracks 
        WHERE Milliseconds > 200000""").fetchall()
    print('\n' + '*' * 13 + 'TASK-2' + '*' * 13)
    print(res)

    with DB() as cursor:
        res = cursor.execute("""
        SELECT t.name, a.Title
        FROM tracks t
        INNER JOIN 
        playlist_track pt ON t.TrackId = pt.TrackId 
        INNER JOIN 
        playlists p ON pt.PlaylistId = p.PlaylistId
        INNER JOIN 
        albums a ON t.AlbumId = a.AlbumId 
        WHERE p.Name = 'TV Shows'""").fetchall()
    print('\n' + '*' * 13 + 'TASK-3' + '*' * 13)
    print(res)

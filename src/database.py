import os
import uuid
import psycopg2
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize
from src.image import DatabaseImage

conn = None
cur = None


def insert_fraud_ad(website_name, url_link, display_url, image_data):
    global conn, cur
    cur.execute("""
        INSERT INTO fraud_advertisements (website_name, url_link, image_data)
        VALUES (%s, %s, %s)
    """, (website_name, url_link, image_data))
    conn.commit()


def create_tables():
    global conn, cur
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fraud_advertisements (
        id SERIAL PRIMARY KEY,
        website_name VARCHAR(255),
        url_link VARCHAR(255) UNIQUE,
        display_url VARCHAR(500),
        image_data BYTEA
        )
    """)
    conn.commit()


def get_fraud_ads_by_similarity(image_data):
    global conn, cur
    # Check image_data with all image_data in the database, if ssim is above 0.8 create 
    # list of DatabaseImage objects and return list

    cur.execute("SELECT website_name, url_link, display_url, image_data FROM fraud_advertisements")
    # cur.execute("SELECT website_name, url_link, image_data FROM fraud_advertisements")
    rows = cur.fetchall()

    similar_ads = []

    for row in rows:
        DIR = os.path.dirname(os.path.abspath(__file__))

        db_website_name, db_url_link, db_display_url, db_image_data = row
        cv2.imwrite(f"{DIR}/orig.jpg", np.frombuffer(image_data, np.uint8))
        cv2.imwrite(f'{DIR}/db.jpg', np.frombuffer(db_image_data, np.uint8))

        image_data = cv2.imdecode(np.frombuffer(image_data, np.uint8), 0)
        db_image_data = cv2.imdecode(np.frombuffer(db_image_data, np.uint8), 0)
        if image_data.shape[0] > db_image_data.shape[0]:
            db_image_data = resize(db_image_data, (image_data.shape[0], image_data.shape[1]), anti_aliasing=True, preserve_range=True)
        else:
            image_data = resize(image_data, (db_image_data.shape[0], db_image_data.shape[1]), anti_aliasing=True, preserve_range=True)
        
        sim = ssim(image_data, db_image_data, data_range=255)
        print(f"SSIM: {sim}")
        
        # if sim > 0.8:
        similar_ads.append(DatabaseImage(db_website_name, 
                                            db_url_link, 
                                            db_display_url, 
                                            db_image_data))
        
    return similar_ads

def drop_tables():
    global conn, cur
    cur.execute("DROP TABLE fraud_advertisements")
    conn.commit()

def connect():
    global conn, cur
    DATABASE_URL = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    return conn, cur


def close_connection():
    global conn, cur
    conn.commit()
    cur.close()


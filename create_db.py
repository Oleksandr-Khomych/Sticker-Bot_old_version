# -*- coding: utf-8 -*-
import sqlite3


def create_db(name):
    try:
        conn = sqlite3.connect(name)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE article
                          (name text, description text, file_id text, availability text, price text)
                        """)
        cursor.execute("""CREATE TABLE basket
                          (user_id text, article_name text, pack_size text, amount text, price text) 
                        """)
        cursor.execute("""CREATE TABLE orders
                            (user_id text, order_in_process text, delivery text, city text, delivery_address,
                             full_name text, phone text, order_id text)
                        """)
        cursor.execute("""CREATE TABLE order_generated
                            (user_id text, order_id text, status text, TTH text, article text,
                            delivery text, city text, delivery_addres text, full_name text, phone text)
                        """)
        conn.commit()
        cursor.close()
        conn.close()
        print('Database create')
    except:
        print('Database already exist')


if __name__ == '__main__':
    create_db('article.db')

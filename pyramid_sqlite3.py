#pythonでのsqlite3の書き込みです。
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import signal
import sqlite3
from contextlib import closing
dbname = 'ejdict.sqlite3'


def diary_world(request):
    print(request)
    print(request.params)
    in_data=request.params


    match_word = in_data["match_word"]


    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        create_table = '''create table items (item_id INTEGER PRIMARY KEY,word TEXT,mean TEXT,level INTEGER DEFAULT 0)'''
        try:
            c.execute(create_table)
        except:
            print("database already exist")


        #全レコード表示

        select_sql = 'select * from items where word = '+'"'+str(match_word)+'"'


        data=[]
        print (select_sql )
        try:

            for row in c.execute(select_sql):
                print(row)
                data.append(row)

                #ブラウザに改行を送付
                data.append("<br>")

            conn.commit()

        except:

            print("data not found")

    
    return Response(str(data))

    #実行処理  python サーバーを立てています
    
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    with Configurator() as config:
        config.add_route('diary', '/')
        config.add_view(diary_world, route_name='diary',renderer="jsonp")
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()

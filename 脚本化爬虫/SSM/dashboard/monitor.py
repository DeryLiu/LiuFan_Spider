#!/usr/bin/env python
# encoding=utf-8
from celery import Celery
from celery.result import AsyncResult
from dashboard.tasks import initial_category_children, test_task
import pymysql
import simplejson as json

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'port': 3306,
    'db': 'ssm',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

conn = pymysql.connect(**config)


def execute_sql(sql):
    with conn.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
    conn.commit()
    return data


def spider_monitor(app):
    print('spider_monitor started')
    state = app.events.State()

    def task_succeeded(event):
        print(event)
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK SUCCEEDED: %s[%s] %s' % (task.name, task.uuid, task.info(),))
        execute_sql('DELETE FROM dashboard_taskresult WHERE UUID="%s"' % task.uuid)
        # result = initial_category_leaf.chunks([[1], [2], [3], [4], [5]], 2)()
        # print(result)

    def task_failed(event):
        print(event)

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
            'task-succeeded': task_succeeded,
            'task-failed': task_failed
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

if __name__ == '__main__':
    print execute_sql('TRUNCATE TABLE dashboard_taskresult')
    app = Celery(broker='amqp://guest:guest@localhost//')
    spider_monitor(app)

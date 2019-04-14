#!/usr/bin/env python3
import datetime
import asyncio
from flask import Flask, request, jsonify
from src.config import MOVIE_SITES
from search import search

app = Flask('shawshank')


@app.route('/api/v1/search', methods=['GET', ])
def search_movie():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_date = datetime.datetime.now()
    keyword = request.args.get('keyword', '')
    results = []
    tasks = [search(item['name'], item['url'], keyword, item['selector']) for item in MOVIE_SITES]
    if tasks:
        results = loop.run_until_complete(asyncio.gather(*tasks))
    results = list(filter(lambda x: x, results))
    end_date = datetime.datetime.now()
    print('cost {}s.'.format((end_date - start_date).total_seconds()))
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5664, debug=True)
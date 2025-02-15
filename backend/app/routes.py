"""
Handles the different routes that are necessary for the experiment: Backend API retrieval & database updates
(the frontend is determined by the React app)
- homepage (currently no purpose)
- recommendation page for the different article_sets from which users choose
- single article page where users can read and rate an article
- Finish page that re-directs users back to Qualtrics (work in progress)
"""
from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import cross_origin
from . import newsapp, db, recommender
from .database import Exposures, Selections, Reads, Users, Positions
from datetime import datetime
import random

"""
Homepage
"""


@newsapp.route('/')
def home():
    return "does this work?"


"""
Recommendation page where article selection takes place

    function that retrieves articles from the backend and logs them in the db "Exposures"
    Input: retrieves user_id and experimental condition from url
    Output: json of articles
"""


@newsapp.route('/recommendations', methods=["GET"])
@cross_origin()
def get_recommendations():
    timestamp = datetime.utcnow()
    user_id = request.args.get('user_id')
    experimental_condition = request.args.get('condition')
    users = [user.user_id for user in Users.query.all()]
    # check if user exists in db; if not:
    if user_id not in users:
        # add user to db
        user = Users(user_id=user_id,
                     timestamp_start=timestamp,
                     experimental_condition=experimental_condition
                     )
        db.session.add(user)
        # retrieve articles from backend
        articles = recommender.get_articles_from_backend(experimental_condition)
        # log article positions
        counter = 0
        for article in articles:
            article_id = article['id']
            position = counter
            counter += 1
            user_id = user_id
            article_position = Positions(article_id=article_id,
                                         user_id=user_id,
                                         position=position,
                                         primary="{}/{}/{}".format(user_id,
                                                                   article_id,
                                                                   position)
                                         )
            db.session.add(article_position)
    # if user already exists in db: retrieve articles in original positions
    else:
        articles = []
        ids = [positions.article_id for positions in Positions.query.filter_by(user_id=user_id)]
        all_articles = recommender.get_articles_from_backend(experimental_condition)
        for id in ids:
            for article in all_articles:
                if article['id'] == id:
                    article = article
                    break
            articles.append(article)
    # log exposure
    exposures = Exposures(user_id=user_id,
                          timestamp_exposures=timestamp,
                          exposure_id="{}/{}".format(user_id,
                                                     str(timestamp)))
    db.session.add(exposures)
    # log reads
    selections = [selection.__dict__ for selection in Selections.query.filter_by(user_id=user_id)]
    if not selections:
        db.session.commit()
    else:
        last_read = selections[-1]
        article_id = last_read['article_id']
        title = last_read['title']
        condition = last_read['condition']
        read = Reads(article_id=article_id,
                     user_id=user_id,
                     timestamp_reads=timestamp,
                     read_title=title,
                     read_condition=condition,
                     primary="{}/{}/{}/{}".format(user_id,
                                                  article_id,
                                                  condition,
                                                  str(timestamp)))
        db.session.add(read)
        db.session.commit()
    return jsonify(articles)


"""
Article page where users can read and rate articles

    function that retrieves a selected article from the backend and logs it in the db "Selections"
    Input: retrieves user_id, article_id, title, and condition from url
    Output: json of single article
"""


@newsapp.route('/article', methods=["GET"])
@cross_origin()
def show_article():
    # request article id and throw warning if none is given
    article_id = request.args.get('article_id')
    if not article_id:
        raise Exception("No article id given")
    # request user id and throw warning if none is given
    user_id = request.args.get('user_id')
    if not user_id:
        raise Exception("No user id given")
    # determine article positions
    positions = [position.__dict__ for position in Positions.query.filter_by(user_id=user_id)]
    position = 101
    for position in positions:
        if position['article_id'] == article_id:
            position = position['position']
            break
    # request title amd condition and determine timestamp
    title = request.args.get('title')
    condition = request.args.get('condition')
    timestamp = datetime.utcnow()
    # log article selection
    article_seen = Selections(article_id=article_id,
                              position=position,
                              user_id=user_id,
                              timestamp_selections=timestamp,
                              title=title,
                              condition=condition,
                              primary="{}/{}/{}/{}".format(user_id,
                                                           article_id,
                                                           position,
                                                           str(timestamp)))
    db.session.add(article_seen)
    db.session.commit()
    # retrieve article from backend
    return jsonify(recommender.get_article_from_backend(user_id, article_id))

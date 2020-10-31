
from flask import Blueprint, request, render_template, url_for, redirect, session

import movie.adapters.repository as repo
from movie.authentication.authentication import login_required
from movie.reviews import services
from movie.reviews.review_form import MovieReviewForm
from movie.util.constants import REVIEW_BP, REVIEW_ENDPOINT, REMOVE_REVIEW_ENDPOINT, MOVIE_BP, MOVIE_DETAILS_ENDPOINT

review_blueprint = Blueprint(REVIEW_BP, __name__)


@review_blueprint.route('/' + REVIEW_ENDPOINT, methods=['GET', 'POST'])
@login_required
def add_review():
    form = MovieReviewForm()
    movie_id = request.args.get('movie_id')
    movie_title = request.args.get('movie_title')

    if form.validate_on_submit():
        rating = int(form.rating.data)
        comment = form.review_text.data
        username = session.get('username')
        services.add_review(movie_id, username, comment, rating, repo.repo_instance)

        movie_info_url = url_for(MOVIE_BP + '.' + MOVIE_DETAILS_ENDPOINT, movie_id=movie_id)
        return redirect(movie_info_url)

    return render_template(
        'review/add_review.html',
        form=form,
        movie_id=movie_id,
        movie_title=movie_title
    )


@review_blueprint.route('/' + REMOVE_REVIEW_ENDPOINT, methods=['GET'])
@login_required
def remove_review():
    movie_id = request.args.get('movie_id')
    review_id = request.args.get('review_id')
    services.remove_review(review_id, movie_id, repo.repo_instance)
    movie_info_url = url_for(MOVIE_BP + '.' + MOVIE_DETAILS_ENDPOINT, movie_id=movie_id)
    return redirect(movie_info_url)
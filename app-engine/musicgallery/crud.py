# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for


crud = Blueprint('crud', __name__)


# [START list]
@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    albums, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        albums=albums,
        next_page_token=next_page_token)
# [END list]


@crud.route('/<id>')
def view(id):
    album = get_model().read(id)
    return render_template("view.html", album=album)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        album = get_model().create(data)

        return redirect(url_for('.view', id=album['id']))

    return render_template("form.html", action="Add", album={})
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    album = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        album = get_model().update(data, id)

        return redirect(url_for('.view', id=album['id']))

    return render_template("form.html", action="Edit", album=album)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))
